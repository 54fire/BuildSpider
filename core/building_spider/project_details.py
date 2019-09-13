import requests, time
from lxml import etree
import threading, random
from queue import Queue

from utils.http import get_request_headers
from core.building_spider.project_spider import ProjectProcuder, CodeProcuder
from setting import TIMEOUT

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
            response = requests.get(url, headers=get_request_headers(), proxies=self.proxies, timeout=TIMEOUT)
            # response = requests.get(url, headers=get_request_headers(), timeout=5)
            if response.status_code == 200:
                return response.content
            else:
                self.project_queue.put(project)
                print("detail_spider错误url：", response.status_code)
                if self.proxy_queue.qsize() > 0:
                    self.proxies = {'http': self.proxy_queue.get()}
                else:
                    print("The proxy_queue is empty!\n")
                    with open('./config/proxy', 'r', encoding='utf-8') as f1:
                        for data in f1.readlines():
                            self.proxy_queue.put(data.strip())
                self.proxies = {'http': self.proxy_queue.get()}

        except Exception as e:
            self.project_queue.put(project)
            print("detail_spider错误url：",e)
            if self.proxy_queue.qsize() > 0:
                self.proxies = {'http': self.proxy_queue.get()}
            else:
                print("The proxy_queue is empty!\n")
                with open('./config/proxy', 'r', encoding='utf-8') as f1:
                    for data in f1.readlines():
                        self.proxy_queue.put(data.strip())
                self.proxies = {'http': self.proxy_queue.get()}




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
        return contents.xpath('string(.)').strip()


    def __get_ztb_from_ele(self, ele):
        ztb_xpath = '//div[@id="tab_ztb"]/table/tbody/tr'
        trs = ele.xpath(ztb_xpath)
        tab_ztb = []
        for tr in trs:
            ztb = {}
            ztb['序号'] = tr.xpath('./td[@data-header="序号"]/text()')[0]
            # t2 = ele.xpath(ztbs + '/td[2]/text()')
            # t3 = ele.xpath(ztbs + '/td[3]/text()')
            # t4 = self._get_a_content(ele.xpath(ztbs + '/td[4]'))
            ztb['日期'] = self._get_a_content(tr.xpath('./td[5]')[0])
            ztb['金额'] = tr.xpath('./td[6]/text()')[0]
            ztb['url查看'] = tr.xpath('./td[9]/a/@data-url')[0]
            tab_ztb.append(ztb)
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
        htba_xpath = '//*[@id="tab_htba"]/table/tbody/tr'
        trs = ele.xpath(htba_xpath)
        htba_tab = []
        for tr in trs:
            htba = {}
            htba['序号'] = tr.xpath('./td[1]/text()')[0]   # 序号
            htba['合同类别'] = tr.xpath('./td[2]//text()')[0]  # 合同类别
            htba['金额'] = tr.xpath('./td[5]//text()')[0]  # 合同金额(万元)
            htba['日期'] = tr.xpath('./td[6]//text()')[0]  # 合同签订日期
            htba['url查看'] = tr.xpath('./td[7]/a/@data-url')[0]  # 合同备案URL
            htba_tab.append(htba)
        return htba_tab

    def __get_sgxk_from_ele(self, ele):
        sgxk_xpath = '//*[@id="tab_sgxk"]/table/tbody/tr'
        trs = ele.xpath(sgxk_xpath)
        sgxk_tab = []
        for tr in trs:
            sgxk = {}
            sgxk['序号'] = tr.xpath('./td[1]/text()')[0]   # 序号
            sgxk['金额'] = tr.xpath('./td[@data-header="合同金额（万元）"]/text()')[0]   # 合同金额(万元）
            sgxk['面积'] = tr.xpath('./td[@data-header="面积（平方米）"]/text()')[0]      # 面积(平方米)
            sgxk['日期'] = tr.xpath('./td[@data-header="发证日期"]/text()')[0]  # 发证日期
            sgxk['url查看'] = tr.xpath('./td[@data-header="查看"]/a/@data-url')[0]  # 施工许可URL
            sgxk_tab.append(sgxk)
        return sgxk_tab

    def __get_jgysba_from_ele(self, ele):
        jgysbas_xpath = '//div[@id="tab_jgysba"]/table/tbody/tr'
        trs = ele.xpath(jgysbas_xpath)
        jgysba_tab = []
        for tr in trs:
            jgysba = {}
            jgysba['序号'] = tr.xpath('./td[1]/text()')[0]
            jgysba['金额'] = tr.xpath('./td[4]/text()')[0]
            jgysba['面积'] = tr.xpath('./td[5]/text()')[0]
            jgysba['实际开工日期'] = tr.xpath('./td[6]/text()')[0]
            jgysba['实际竣工日期'] = tr.xpath('./td[7]/text()')[0]
            jgysba['url查看'] = tr.xpath('./td/a/@data-url')[0]
            jgysba_tab.append(jgysba)
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
        # 是否获取招投标
        project.ztb = self.__get_ztb_from_ele(ele) if int(ztb) > 0 else []
        # 是否获取施工图审查
        # project.sgtsc = self.__get_sgtsc_from_ele(ele) if int(sgtsc) > 0 else []

        project.htba = self.__get_htba_from_ele(ele) if int(htba) > 0 else []

        project.sgxk = self.__get_sgxk_from_ele(ele) if int(sgxk) > 0 else []

        project.jgysba = self.__get_jgysba_from_ele(ele) if int(jgysba) > 0 else []

        return project

    def run(self):
        while True:
            project = self.project_queue.get()
            page = self.__get_page_from_html(project)
            if page:
                pro = self.__get_detail_for_project(page, project)
                print(pro)
                with open('fire/'+pro.company, 'a') as f:
                    pros = str(pro)
                    f.write(pros + '\n')
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
    with open('../../config/result', 'r') as f1:
        for data in f1.readlines():
            company_queue.put(data.strip())

    with open('../../config/proxy', 'r') as f1:
        for data in f1.readlines():
            proxy_queue.put(data.strip())

    with open('../../config/post_proxy', 'r') as f1:
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




