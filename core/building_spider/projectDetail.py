import requests, os, time
from lxml import etree
from utils.http import get_request_headers

def get_html(url, proxy={}):
    time.sleep(0.5)
    if not proxy:
        res = requests.get(url, headers=get_request_headers())
        if res.status_code == 200:
            return res.text
    else:
        res = requests.get(url, headers=get_request_headers(), proxies=proxy)
        if res.status_code == 200:
            return res.text

def get_tenderInfo(url):
    html = get_html(url)
    if html:
        ele = etree.HTML(html)
        results = ele.xpath("/html/body/div[1]/div/div/table/tbody/tr[11]/td/text()")
        return results[0]

def get_contractInfo(url):
    html = get_html(url)
    if html:
        ele = etree.HTML(html)
        results = ele.xpath("/html/body/div[1]/div/div/table/tbody/tr[11]/td/text()")
        return results[0]

def get_buildliseInfo(url):
    html = get_html(url)
    if html:
        ele = etree.HTML(html)
        results = ele.xpath("/html/body/div[1]/div[1]/div/table/tbody/tr[12]/td[1]/text()")
        return results[0]

def get_bafinishInfo(url):
    html = get_html(url)
    if html:
        ele = etree.HTML(html)
        results = ele.xpath("/html/body/div[1]/div[1]/div/table/tbody/tr[10]/td/text()")
        return results[0]

def __get_detail(index, project):
    detail = project[index]
    detail_lists = []
    if detail:
        detail_urls = detail[-1]
        if index == 'ztb':
            detail_lists = [get_tenderInfo(main_url+detail_url) for detail_url in detail_urls]
            return detail_lists
        elif index == 'htba':
            detail_lists = [get_contractInfo(main_url+detail_url) for detail_url in detail_urls]
            return detail_lists
        elif index == 'sgxk':
            detail_lists = [get_buildliseInfo(main_url+detail_url) for detail_url in detail_urls]
            return detail_lists
        elif index == 'jgysba':
            detail_lists = [get_bafinishInfo(main_url+detail_url) for detail_url in detail_urls]
            return detail_lists
        else:
            print("your input is error!")
    else:
        return detail_lists

companys = os.listdir('../../files')
company_finally = os.listdir('../../filter_files')
os.chdir('../../files')
main_url = "http://jzsc.mohurd.gov.cn"

for company in companys:
    if company not in company_finally:
        with open(company, 'r') as f:
            projects = f.readlines()
        for pro in projects:
            project = eval(pro.strip())
            print(project)
            detail = {}
            # 1. 获取招投标的细节信息
            ztb = __get_detail('ztb', project)
            # 2. 获取合同备案细节信息
            htba = __get_detail('htba', project)
            # 3. 获取施工许可细节信息
            sgxk = __get_detail('sgxk', project)
            # 4. 获取验收备案细节信息
            jgysba = __get_detail('jgysba', project)
            # project["ztb"] =
            detail['company'] = project['company']
            detail['title'] = project['title']
            detail['ztb'] = ztb
            detail['htba'] = htba
            detail['sgxk'] = sgxk
            detail['jgysba'] = jgysba
            with open('../filter_files/'+company, 'a') as f:
                f.write(str(detail) + '\n')
            # print(ztb, htba, sgxk, jgysba)
