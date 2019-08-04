import requests
import re
from lxml import etree
import json
from queue import Queue

from domain import Building
from utils.http import get_request_headers



class DetailSpider(object):

    def __init__(self, project, proxy):
        self.url = 'http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/' + project.url
        self.project = project
        self.project.url = self.url
        self.proxies = {
            'http': proxy
        }

    def __get_page_from_html(self):
        try:
            response = requests.get(self.url, headers=get_request_headers(), proxies=self.proxies, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print("detail_spider错误url：", response.status_code, self.url, self.project, self.proxies)
        except Exception as e:
            print("detail_spider错误url：",self.url, self.project, self.proxies)
            print(e)

    # 获取招投标、施工图审查、合同备案、施工许可、竣工验收备案的个数
    def _get_nums_from_ele(self, page):
        all_num = re.findall(r'.*?招投标<em class="datas_num">(\d+)</em>'
                         r'.*?施工图审查<em class="datas_num">(\d+)</em>'
                         r'.*?合同备案<em class="datas_num">(\d+)</em>'
                         r'.*?施工许可<em class="datas_num">(\d+)</em>'
                         r'.*?竣工验收备案<em class="datas_num">(\d+)</em>', page, re.S)
        for num in all_num[0]:
            yield int(num)

    def _get_big_class_from_page(self, page):
        ztb = re.findall(r'id="tab_ztb"(.*?)'
                         r'<div id="tab_sgtsc(.*?)'
                         r'<div id="tab_htba(.*?)'
                         r'<div id="tab_sgxk(.*?)'
                         r'<div id="tab_jgysba(.*?)', page, re.S)
        for html in ztb[0]:
            yield html

    def _get_ztb(self, ztb_str):
        numbers = re.findall('<td data-header="序号">(\d+)</td>', ztb_str, re.S)
        tools = re.findall('<td data-header="招标类型">(.*?)</td>', ztb_str, re.S)
        tar_com = re.findall('<td data-header="中标单位名称">(.*?)</td>', ztb_str, re.S)
        tar_com = re.sub('\s<a.*?">|</a>','',tar_com[0],re.S).strip()
        print(tar_com)

    def __get_sgtsc_from_ele(self, ele):
        pass


    def __get_htba_from_ele(self, ele):
        pass

    def __get_sgxk_from_ele(self, ele):
        pass

    def __get_jgysba_from_ele(self, ele):
        pass

    def __get_others_from_ele(self, ele):
        pass

    def get_project(self):
        page = self.__get_page_from_html()
        if page:
            ztb, sgtsc, htba, sgxk, jgysba = self._get_nums_from_ele(page)
            ztb_str, sgtsc_str, htba_str, sgxk_str, jgysba_str = self._get_big_class_from_page(page)
            if ztb:
                self._get_ztb(ztb_str)


if __name__ == '__main__':
        project = {'company': '中国建筑第四工程局有限公司', 'title': '佛禅（挂）2009-013宗地4、5#地块公建项目（小学、幼儿园、社区医院、垃圾收集站、公共厕所）', 'cls': '房屋建筑工程','url': '4401121612300101', 'use': ''}
        project = Building(**project)
        proxy = 'http://119.180.142.217:8060'
        try:
            DetailSpider(project,proxy).get_project()
        except Exception as e:
            print("错误：",project,e)





