import requests
import re
from queue import Queue
import threading

'''
目的： 输入公司名称、输出公司code
1. 定义一个类 CompanyCode，用来接收公司名称
'''
from utils.http import get_request_headers
from setting import TIMEOUT, IS_PROXY

'''
定义一个 CodeProcuder 类，继承于threading.Thread用来获取公司的code
'''
class CodeProcuder(threading.Thread):

    def __init__(self, company_queue, code_queue, proxy_queue, *args, **kwargs):
        '''
        定义一个 CodeProcuder 类，继承于threading.Thread用来获取公司的code
        :param company_queue: 用来提供公司名称的队列
        :param code_queue: 用来储存公司对于url地址的队列
        :param proxy_queue: 用来提供代理ip的队列
        '''
        super(CodeProcuder, self).__init__(*args, **kwargs)
        self.company_queue = company_queue
        self.company_code_queue = code_queue
        self.proxy_queue = proxy_queue
        self.url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
        if self.proxy_queue.qsize() >0:
            self.proxies = {'http': self.proxy_queue.get()}
        else:
            self.proxies = {}

    def __get_page_from_url(self, company):
        data = {"complexname": company}
        if self.proxies:
            try:
                if IS_PROXY:
                    response = requests.post(self.url, headers=get_request_headers(), data=data, proxies=self.proxies, timeout=TIMEOUT)
                else:
                    response = requests.post(self.url, headers=get_request_headers(), data=data, timeout=TIMEOUT)
                if response.status_code == 200:
                    return response.text
                else:
                    raise requests.HTTPError
            except:
                # 将公司放回队列，更换代理ip
                self.company_queue.put(company)
                if self.proxy_queue.qsize() >0:
                    self.proxies = {'http': self.proxy_queue.get()}
                    print(self.proxies)
                else:
                    self.proxy_queue.join()
                return None


    def __get_code_from_page(self, page, company):
        pattarn = (r'.*?/compDetail/(\d+)">.*?')
        code = re.findall(pattarn, page)
        if code:
            return code[0]
        else:
            print("你查寻的公司没有入库：{}".format(company))

    def run(self):
        while True:
            company = self.company_queue.get()
            page = self.__get_page_from_url(company)
            if page:
                code = self.__get_code_from_page(page, company)
                result = (company, code)
                self.company_code_queue.put(result)
                print(result, self.proxies)
            self.company_queue.task_done()


if __name__ == '__main__':
    company_queue = Queue()
    company_code_queue = Queue()
    proxy_queue = Queue()
    with open('result', 'r') as f1:
        for data in f1.readlines():
            company_queue.put(data.strip())

    with open('proxy', 'r') as f1:
        for data in f1.readlines():
            proxy_queue.put(data.strip())

    code_procuders = list()
    for _ in range(3):
        code_procuders.append(CodeProcuder(company_queue, company_code_queue, proxy_queue))
    for t in code_procuders:
        t.setDaemon(True)
        t.start()
    company_queue.join()
    # company_code_queue.join()



