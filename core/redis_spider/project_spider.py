from queue import Queue
import requests
import re, time, threading

from utils.http import get_request_headers
from domain import Building
from core.building_spider.building_spider import CodeProcuder
from setting import TIMEOUT
from core.building_spider.filter_project import keywords_juste

class ProjectProcuder(threading.Thread):

    def __init__(self, company_code_queue, project_queue, proxy_queue, post_proxy_queue, *args, **kwargs):
        super(ProjectProcuder, self).__init__(*args, **kwargs)
        self.proxy_queue = proxy_queue
        self.company_code_queue = company_code_queue
        self.project_queue = project_queue
        self.post_proxy_queue = post_proxy_queue
        # 新建一个队列，用于储存post请求的数据
        self.data_queue = Queue()
        self.url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/"
        self.proxies = {'http': self.proxy_queue.get()}

    def __get_page_from_html(self, company_code):
        url = self.url + company_code[1]
        try:
            response = requests.get(url, headers=get_request_headers(), proxies=self.proxies, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.content.decode()
            else:
                self.company_code_queue.put(company_code)
                self.proxies = {'http': self.proxy_queue.get()}
        except:
            self.company_code_queue.put(company_code)
            self.proxies = {'http': self.proxy_queue.get()}

    def __get_title_and_url_from_page(self, html, company):
        pattarn = re.compile(r'<tr>.*?<td data-header="项目名称".*?(\d+).*?>(.*?)</a></td>.*?<td data-header="项目类别">(.*?)</td>.*?</tr>', re.S)
        title_and_urls = re.findall(pattarn, html)
        for title_and_url in title_and_urls:
            project = Building(company, title_and_url[1],cls=title_and_url[2],url=title_and_url[0])
            yield project

    def __get_project_tt_and_pc(self, page):
        tt_and_pp_pattarn = r'.*?{pg.*?tt:(\d+),pn.*?pc:(\d+),.*?'
        code = re.findall(tt_and_pp_pattarn, page)
        if code:
            return code[0]  # tt:  pc:
        return None

    def __get_post_page_from_html(self, data, company_code):
        url = self.url + company_code[1]
        proxy = self.post_proxy_queue.get()
        proxies = {'http': proxy}
        try:
            response = requests.post(url, headers=get_request_headers(), data=data, proxies=proxies, timeout=TIMEOUT)
            if response.status_code == 200:
                self.post_proxy_queue.put(proxy)
                print(data)
                return response.content.decode()
            else:
                result = (company_code, data)
                self.data_queue.put(result)
                print("post请求错误page", data, url, proxies)
        except Exception as e:
            result = (company_code, data)
            self.data_queue.put(result)
            print("post请求错误page", data, url, proxies)
            print(e)

    def __post_one(self):
        while True:
            res = self.data_queue.get()
            print(res)
            company_code = res[0]
            data = res[1]
            html = self.__get_post_page_from_html(data, company_code)
            if html:
                for project in self.__get_title_and_url_from_page(html, company_code[0]):
                    if keywords_juste(project.title):
                        self.project_queue.put(project)
            self.data_queue.task_done()

    def __get_post_project(self, tt_pc, company_code):
        tt, pc = tt_pc
        tt = int(tt)
        pc = int(pc)
        for i in range(2, pc+1):
            data = {"$total": tt, "$reload": 0, "$pg": i, "$pgsz": 25}
            company_data = (company_code,data)
            self.data_queue.put(company_data)
        data_lists = list()
        for _ in range(5):
            data_lists.append(threading.Thread(target=self.__post_one))
        for t in data_lists:
            t.setDaemon(True)
            t.start()
        self.data_queue.join()

    def run(self):
        while True:
            company_code = self.company_code_queue.get()
            page = self.__get_page_from_html(company_code)
            if page:
                for project in self.__get_title_and_url_from_page(page, company_code[0]):
                    if keywords_juste(project.title):
                        self.project_queue.put(project)
                tt_pc = self.__get_project_tt_and_pc(page)
                # 是否有多个页面
                if tt_pc:
                    with open('files/'+company_code[0], 'a') as f:
                        f.write(tt_pc[0]+'\n')
                    self.__get_post_project(tt_pc, company_code)
            self.company_code_queue.task_done()

if __name__ == '__main__':
    s= time.time()
    company_queue = Queue()
    company_code_queue = Queue()
    proxy_queue = Queue()
    project_queue = Queue()
    post_proxy_queue = Queue()
    with open('result', 'r') as f1:
        for data in f1.readlines():
            company_queue.put(data.strip())

    with open('proxy', 'r') as f1:
        for data in f1.readlines():
            proxy_queue.put(data.strip())

    code_procuders = list()
    project_procuders = list()
    for _ in range(3):
        code_procuders.append(CodeProcuder(company_queue, company_code_queue, proxy_queue))
        code_procuders.append(ProjectProcuder(company_code_queue, project_queue, proxy_queue, post_proxy_queue))
    for t in code_procuders:
        t.setDaemon(True)
        t.start()
    company_queue.join()
    company_code_queue.join()
    print(round(time.time()-s, 2))
