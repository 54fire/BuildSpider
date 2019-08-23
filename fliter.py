import os
from get_post import save_file_to_excel
from setting import KEYWORDS
from core.building_spider.filter_project import keywords_juste
import xlsxwriter
import time

file_path = 'files/'
lis = os.listdir(file_path)

for li in lis:
    with open('files/'+li, 'r') as f:
        datas = f.readlines()
    for data in datas[1:]:
        pro = eval(data.strip())
        title = pro['title']
        if keywords_juste(title):
            with open('filter_files/'+li, 'a') as f:
                f.write(data)

'''
workbook = xlsxwriter.Workbook('fire.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
for li in lis:
    content = open('files/'+li,'r').readlines()[1:]
    save_file_to_excel(workbook, li, content)
workbook.close()

file_path = 'filter_files/'
lis = os.listdir(file_path)
workbook = xlsxwriter.Workbook('54fire.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
for li in lis:
    content = open(file_path+li,'r').readlines()
    save_file_to_excel(workbook, li, content)
workbook.close()
'''

# with open('config/result', 'r') as f:
#     datas = f.readlines()
# for data in datas:
#     if data.strip() not in lis:
#         print(data)

# with open('wenjian', 'r') as f:
#     projects = f.readlines()
# 
# for project in projects:
#     files = []
#     pro = eval(project)
#     filename = pro['company']
#     with open('files/'+filename, 'a') as fl:
#         fl.write(project)