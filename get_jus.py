from core.building_spider.building_spider import CodeProcuder
from core.building_spider.project_spider import ProjectProcuder
import os, re, requests
from utils.http import get_request_headers

'''
code_url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
pattarn = (r'.*?/compDetail/(\d+)">.*?')
names = os.listdir('files/')
base_project_url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/"
tt_and_pp_pattarn = r'.*?{pg.*?tt:(\d+),pn.*?pc:(\d+),.*?'

jus = []
with open('./config/result', 'r', encoding='utf-8') as f1:
    companys = f1.readlines()
    for company in companys:
        company = company.strip()
        jus.append(company)

for name in names:
    if name in jus:
        data = {"complexname": name}
        response = requests.post(code_url, headers=get_request_headers(), data=data)
        if response.status_code == 200:
            page = response.text
            code = re.findall(pattarn, page)
            project_url = base_project_url + code[0]
            response = requests.get(project_url, headers=get_request_headers())
            if response.status_code == 200:
                page = response.text
                tt_pc = re.findall(tt_and_pp_pattarn, page)
                if tt_pc:
                    tt, pc = tt_pc[0]
                    print(tt, pc)
                    with open('files/'+name, 'r') as f:
                        contents = f.readlines()
                        num = len(contents)
                        print(num)
                        if str(num) == tt:
                            print("yes" + name)
                        else:
                            os.remove('files/'+name)
                            print("no" + name)
                else:
                    print("没有tt和pc" + name)
'''
ls = [1,'ks3',4,[1,2], 5]
for i in ls:
    if i[1]:
        ls.remove(i)
print(ls)


