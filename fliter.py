import os, time, xlsxwriter

from get_post import save_file_to_excel
from setting import KEYWORDS
from core.building_spider.filter_project import keywords_juste

file_path = 'fire/'
lis = os.listdir(file_path)

workbook = xlsxwriter.Workbook('others.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
for li in lis:
    content = open('fire/'+li,'r').readlines()
    save_file_to_excel(workbook, li, content)
workbook.close()

'''
file_path = 'files/'
lis = os.listdir(file_path)
workbook = xlsxwriter.Workbook('54fire.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
for li in lis:
    content = open(file_path+li,'r').readlines()[1:]
    save_file_to_excel(workbook, li, content)
workbook.close()

file_path = 'files/'
lis = os.listdir(file_path)
with open('54fire', 'w') as fire:
    for li in lis:
        with open(file_path+li, 'r') as f:
            content = f.readlines()
        temp = content[1:]
        fire.writelines(temp)
        f.close()
'''

'''
workbook = xlsxwriter.Workbook('fire.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
content = open('54fire', 'r').readlines()
content2 = open('54fire2', 'r').readlines()
save_file_to_excel(workbook, 'fire', content)
save_file_to_excel(workbook, 'fire2', content2)
workbook.close()

with open('config/result', 'r') as f:
    datas = f.readlines()
ls = os.listdir('fire/')
print(len(ls))

for data in datas:
    data = data.strip()
    if data in ls:
        os.remove('fire/'+data)

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