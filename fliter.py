import os
from get_post import save_file_to_excel
import xlsxwriter
import time


file_path = 'filter_files/'
lis = os.listdir(file_path)

# for li in lis:
#     with open('files/'+li, 'r') as f:
#         datas = f.readlines()
#     for data in datas[1:]:
#         pro = eval(data.strip())
#         if ('学校' or '技校' or '学院' or '职业' or '小学' or '中学' or '大学 'or '专科' or
#             '院校' or '幼儿' or '师范' or '教学' or '体育' or '初等' or '高等' or '宿舍' or
#             '宿舍' or '食堂' or '图书馆' or '实验' or '高中' or '初中') in pro['title']:
#             print(pro['title'])
#             with open('filter_files/'+li, 'a') as f:
#                 f.write(data)




# print(len(lis))
workbook = xlsxwriter.Workbook('54fire.xlsx', {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
for li in lis:
    content = open('filter_files/'+li,'r').readlines()
    save_file_to_excel(workbook, li, content)
workbook.close()

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