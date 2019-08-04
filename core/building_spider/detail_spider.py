import requests, time
from lxml import etree
import threading, random
from queue import Queue

from utils.http import get_request_headers
from core.building_spider.project_spider import ProjectProcuder, CodeProcuder

class DetailProcuder(threading.Thread):

    def __init__(self, project_queue, detail_queue, proxy_queue, *args, **kwargs):
        super(DetailProcuder, self).__init__(*args, **kwargs)
        self.project_queue = project_queue
        self.detail_queue = detail_queue
        self.proxy_queue = proxy_queue
        self.url = 'http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/'
        self.proxies = {'http': self.proxy_queue.get()}

    def __get_page_from_html(self, project):
        url = self.url + project.url
        try:
            response = requests.get(url, headers=get_request_headers(), proxies=self.proxies, timeout=5)
            if response.status_code == 200:
                return response.content
            else:
                self.project_queue.put(project)
                self.proxies = self.proxy_queue.get()
                self.proxies = {'http': self.proxy_queue.get()}
                print("detail_spider错误url：", response.status_code)
        except Exception as e:
            self.project_queue.put(project)
            self.proxies = {'http': self.proxy_queue.get()}
            print("detail_spider错误url：",e)


    def __get_ele_from_page(self, page):
        return etree.HTML(page)

    def __get_nums_from_ele(self, ele):
        ztb =  ele.xpath('//a[@data-contentid="tab_ztb"]/span/em/text()')[0]
        sgtsc =  ele.xpath('//a[@data-contentid="tab_sgtsc"]/span/em/text()')[0]
        htba =  ele.xpath('//a[@data-contentid="tab_htba"]/span/em/text()')[0]
        sgxk =  ele.xpath('//a[@data-contentid="tab_sgxk"]/span/em/text()')[0]
        jgysba =  ele.xpath('//a[@data-contentid="tab_jgysba"]/span/em/text()')[0]
        return (ztb, sgtsc, htba, sgxk, jgysba)


    def _get_a_content(self, contents):
        lis = []
        for t4 in contents:
            result = t4.xpath('string(.)').strip()
            lis.append(result)
        return lis


    def __get_ztb_from_ele(self, ele):
        ztbs = '//div[@id="tab_ztb"]/table/tbody/tr'
        t1 = ele.xpath(ztbs + '/td[@data-header="序号"]/text()')
        t2 = ele.xpath(ztbs + '/td[2]/text()')
        t3 = ele.xpath(ztbs + '/td[3]/text()')
        t4 = self._get_a_content(ele.xpath(ztbs + '/td[4]'))
        t5 = self._get_a_content(ele.xpath(ztbs + '/td[5]'))
        t6 = ele.xpath(ztbs + '/td[6]/text()')
        t7 = ele.xpath(ztbs + '/td[9]/a/@data-url')
        tab_ztb = (t1, t2, t3, t4, t5, t6, t7)
        return tab_ztb

    def __get_sgtsc_from_ele(self, ele):
        s1 = ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[1]/text()')   # 序号
        s2 = self._get_a_content(ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[@data-header="勘察单位名称"]'))    # 勘察单位名称
        s3 = self._get_a_content(ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[@data-header="设计单位名称"]'))  # 设计单位名称
        s4 = ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[@data-header="施工图审查机构名称"]/text()')  # 施工图审查机构名称
        s5 = ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[@data-header="审查完成日期"]/text()')  # 审查完成日期
        s6 = ele.xpath('//*[@id="tab_sgtsc"]/table/tbody/tr/td[@data-header="查看"]/a/@data-url')  # 施工图审查URL
        sgtsc_tab = (s1, s2, s3, s4, s5, s6)
        return sgtsc_tab


    def __get_htba_from_ele(self, ele):
        htbas = '//*[@id="tab_htba"]/table/tbody/tr'
        s1 = ele.xpath(htbas + '/td[1]/text()')   # 序号
        s2 = ele.xpath(htbas + '/td[2]//text()')  # 合同类别
        s3 = ele.xpath(htbas + '/td[5]//text()')  # 合同金额(万元)
        s4 = ele.xpath(htbas + '/td[6]//text()')  # 合同签订日期
        s5 = ele.xpath(htbas + '/td[7]/a/@data-url')  # 合同备案URL
        htba_tab = (s1, s2, s3, s4, s5)
        return htba_tab

    def __get_sgxk_from_ele(self, ele):
        s1 = ele.xpath('//*[@id="tab_sgxk"]/table/tbody/tr/td[1]/text()')   # 序号
        s2 = ele.xpath('//*[@id="tab_sgxk"]/table/tbody/tr/td[@data-header="合同金额（万元）"]/text()')   # 合同金额(万元）
        s3 = ele.xpath('//*[@id="tab_sgxk"]/table/tbody/tr/td[@data-header="面积（平方米）"]/text()')      # 面积(平方米)
        s4 = ele.xpath('//*[@id="tab_sgxk"]/table/tbody/tr/td[@data-header="发证日期"]/text()')  # 发证日期
        s5 = ele.xpath('//*[@id="tab_sgxk"]/table/tbody/tr/td[@data-header="查看"]/a/@data-url')  # 施工许可URL
        sgxk_tab = (s1, s2, s3, s4, s5)
        return sgxk_tab

    def __get_jgysba_from_ele(self, ele):
        jgysbas = '//div[@id="tab_jgysba"]/table/tbody/tr'
        t1 = ele.xpath(jgysbas + '/td[1]/text()')
        t2 = ele.xpath(jgysbas + '/td[4]/text()')
        t3 = ele.xpath(jgysbas + '/td[5]/text()')
        t4 = ele.xpath(jgysbas + '/td[6]/text()')
        t5 = ele.xpath(jgysbas + '/td[7]/text()')
        t6 = ele.xpath(jgysbas + '/td/a/@data-url')
        jgysba_tab = (t1, t2, t3, t4, t5, t6)
        return jgysba_tab

    def __get_others_from_ele(self, ele, project):
        project.use =       ele.xpath('//dl/dd[8]/text()')[0] if len(ele.xpath('//dl/dd[8]/text()')) > 0 else ''
        project.all_money = ele.xpath('//dl/dd[9]/text()')[0] if len(ele.xpath('//dl/dd[9]/text()')) > 0 else ''
        project.all_area =  ele.xpath('//dl/dd[10]/text()')[0] if len(ele.xpath('//dl/dd[10]/text()')) > 0 else ''
        project.url = self.url + project.url

    def __get_detail_for_project(self, page, project):
        ele = self.__get_ele_from_page(page)
        ztb, sgtsc, htba, sgxk, jgysba = self.__get_nums_from_ele(ele)
        self.__get_others_from_ele(ele, project)
        if int(ztb) > 0:
            project.ztb = self.__get_ztb_from_ele(ele)
        if int(sgtsc) > 0:
            project.sgtsc = self.__get_sgtsc_from_ele(ele)
        if int(htba) > 0:
            project.htba = self.__get_htba_from_ele(ele)
        if int(sgxk) > 0:
            project.sgxk = self.__get_sgxk_from_ele(ele)
        if int(jgysba) > 0:
            project.jgysba = self.__get_jgysba_from_ele(ele)
        return project

    def run(self):
        while True:
            project = self.project_queue.get()
            page = self.__get_page_from_html(project)
            if page:
                pro = self.__get_detail_for_project(page, project)
                print(pro)
                self.detail_queue.put(pro)
            self.project_queue.task_done()

if __name__ == '__main__':
    s= time.time()
    company_queue = Queue()
    company_code_queue = Queue()
    proxy_queue = Queue()
    post_proxy_queue = Queue()
    project_queue = Queue()
    detail_queue = Queue()
    with open('result', 'r') as f1:
        for data in f1.readlines():
            company_queue.put(data.strip())

    with open('proxy', 'r') as f1:
        for data in f1.readlines():
            proxy_queue.put(data.strip())

    with open('post_proxy', 'r') as f1:
        for data in f1.readlines():
            post_proxy_queue.put(data.strip())

    code_procuders = list()
    for _ in range(3):
        code_procuders.append(CodeProcuder(company_queue, company_code_queue, proxy_queue))
        code_procuders.append(ProjectProcuder(company_code_queue, project_queue, proxy_queue, post_proxy_queue))
    for _ in range(10):
        code_procuders.append(DetailProcuder(project_queue, detail_queue, proxy_queue))

    for t in code_procuders:
        t.setDaemon(True)
        t.start()
    company_queue.join()
    company_code_queue.join()
    project_queue.join()
    print(round(time.time()-s, 2))




