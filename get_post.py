import xlrd
import xlwt
from xlutils.copy import copy
import xlsxwriter

from domain import Building

def save_file_to_excel(workbook, sheetname, contents):
    # workbook = xlsxwriter.Workbook(filename, {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
    work_sheet = workbook.add_worksheet(sheetname)
    main_url = 'http://jzsc.mohurd.gov.cn'

    # 首行格式
    table = workbook.add_format({'border': 1, 'font_size': 16, 'bold': False, 'align': 'center', 'bg_color': 'yellow'})
    align = workbook.add_format({'align': 'center'})
    work_sheet.set_column(0, 1, 20)    # 第一列 公司名称
    work_sheet.set_column(2, 3, 13, None,{'hidden': True})    # 第三列 工程分类（默认隐藏）
    work_sheet.set_column(4, 5, 11)

    # 招投标列格式
    work_sheet.set_column(6, 6, 10, align)
    work_sheet.set_column(7, 9, 15, None, {'hidden': True})
    work_sheet.set_column(10, 11, 15)

    # 施工图审查格式
    work_sheet.set_column(12, 16, 15, None, {'hidden': True})

    # 合同备案格式
    work_sheet.set_column(17, 17, 10, align)
    work_sheet.set_column(18, 18, 13, None, {'hidden': True})
    work_sheet.set_column(19, 20, 15)

    # 施工许可格式
    work_sheet.set_column(21, 21, 10, align)
    work_sheet.set_column(22, 24, 15)

    # 竣工验收备案格式
    work_sheet.set_column(25, 25, 10, align)
    work_sheet.set_column(26, 29, 15)

    tab_title = ['公司名称', '项目名称', '工程分类', '工程用途', '总投资','总面积',       # 0 - 5
                 '招投标序号','招标类型','招标方式','中标单位名称','中标日期', '中标金额（万元）', # 6 - 11
                 '施工图审查序号', '勘察单位名称', '设计单位名称', '施工图审查机构名称', '审查完成日期',  # 12 - 16
                 '合同备案序号', '合同类别', '合同金额（万元）', '合同签订日期',    # 17 - 20
                 '施工许可序号', '合同金额（万元）', '面积（平方米）', '发证日期',   # 21 - 24
                 '竣工验收备案序号','实际造价（万元）', '实际面积（平方米）', '实际开工日期', '实际竣工验收日期',] # 25 - 29
    # for title in range(len(tab_title)):
        # work_sheet.write_string(0,title,tab_title[title],table)
    work_sheet.write_row(0, 0, tab_title, table)
    index = 1

    # 正文写入
    for content in contents:
        content_dict = eval(content)
        print(sheetname)
        project = Building(**content_dict)
        ztb_index, jgysba_index, sgxk_index, sgtsc_index, htba_index = 0, 0, 0, 0, 0
        if project.ztb:
            ztb_index = len(project.ztb[0])  # 获取需要写入数据的行数
            for i in range(1, len(project.ztb)-1):
                work_sheet.write_column(index, 6+i, project.ztb[i])  # 追加写入数据，注意是从i+rows_old行开始写入
            for j in range(ztb_index):
                work_sheet.write_url(index+j, 6, main_url+project.ztb[-1][j], string=project.ztb[0][j])

        if project.sgtsc:
            sgtsc_index = len(project.sgtsc[0])
            for i in range(1, len(project.sgtsc)-1):
                work_sheet.write_column(index, i+12, project.sgtsc[i])
            for j in range(sgtsc_index):
                work_sheet.write_url(index+j, 12, main_url+project.sgtsc[-1][j], string=project.sgtsc[0][j])

        if project.htba:
            htba_index  = len(project.htba[0])
            for i in range(1, len(project.htba)-1):
                work_sheet.write_column(index, i+17, project.htba[i])
            for j in range(htba_index):
                work_sheet.write_url(index+j, 17, main_url+project.htba[-1][j], string=project.htba[0][j])

        if project.sgxk:
            sgxk_index = len(project.sgxk[0])
            for i in range(1, len(project.sgxk)-1):
                work_sheet.write_column(index, i+21, project.sgxk[i])
            for j in range(sgxk_index):
                work_sheet.write_url(index+j, 21, main_url+project.sgxk[-1][j], string=project.sgxk[0][j])

        if project.jgysba:
            jgysba_index = len(project.jgysba[0])  # 获取需要写入数据的行数
            for j in range(1, len(project.jgysba)-1):
                work_sheet.write_column(index, j+25, project.jgysba[j])  # 追加写入数据，注意是从i+rows_old行开始写入
            for j in range(jgysba_index):
                work_sheet.write_url(index+j, 25, main_url+project.jgysba[-1][j], string=project.jgysba[0][j])


        work_sheet.write_string(index, 0, project.company)
        work_sheet.write_url(index, 1, project.url,string=project.title)
        work_sheet.write_string(index, 2, project.cls)
        work_sheet.write_string(index, 3, project.use)
        project.all_money = project.all_money.replace('（万元）','').replace('-', '0')
        project.all_area = project.all_area.replace('（平方米）','').replace('-', '0')
        work_sheet.write(index, 4, project.all_money)
        work_sheet.write(index, 5, project.all_area)

        add = max(ztb_index, sgtsc_index, sgxk_index, htba_index, jgysba_index)
        index = index + add

    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    # Add a format. Green fill with dark green text.
    format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})

    work_sheet.conditional_format(1,11,index,11, {'type': 'cell',
                                                'criteria': '>=',
                                                'value': 19999,
                                                'format': format1})
    work_sheet.conditional_format(1,19,index,19, {'type': 'cell',
                                                  'criteria': '>=',
                                                  'value': 19999,
                                                  'format': format1})
    work_sheet.conditional_format(1,22,index,22, {'type': 'cell',
                                                  'criteria': '>=',
                                                  'value': 19999,
                                                  'format': format1})
    work_sheet.conditional_format(1,26,index,26, {'type': 'cell',
                                                  'criteria': '>=',
                                                  'value': 19999,
                                                  'format': format1})
    '''
    work_sheet.conditional_format(1,5,index,5, {'type': 'cell',
                                                'criteria': '>=',
                                                'value': 100000,
                                                'format': format2})
    '''
    work_sheet.autofilter(0,0,index,25)
    # workbook.close()


def save_onefile_to_excel(filename, sheetname):
    workbook = xlsxwriter.Workbook(filename, {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
    work_sheet = workbook.add_worksheet(sheetname)
    with open('xpf_fin','r') as f:
        contents = f.readlines()

    main_url = 'http://jzsc.mohurd.gov.cn'
    # for c in contents:
    # if c.strip() not in content:
    # print(c.strip())
    # 首行格式
    table = workbook.add_format({'border': 1, 'font_size': 16, 'bold': False, 'align': 'center', 'bg_color': 'yellow'})
    mark = workbook.add_format({'bg_color': 'red', 'bold': True})
    align = workbook.add_format({'align': 'center'})
    work_sheet.set_column(0, 1, 20)    # 第一列 公司名称
    work_sheet.set_column(2, 3, 13, None,{'hidden': True})    # 第三列 工程分类（默认隐藏）
    work_sheet.set_column(4, 5, 11)

    # 招投标列格式
    work_sheet.set_column(6, 6, 10, align)
    work_sheet.set_column(7, 9, 15, None, {'hidden': True})
    work_sheet.set_column(10, 11, 15)

    # 施工图审查格式
    work_sheet.set_column(12, 16, 15, None, {'hidden': True})

    # 合同备案格式
    work_sheet.set_column(17, 17, 10, align)
    work_sheet.set_column(18, 18, 13, None, {'hidden': True})
    work_sheet.set_column(19, 20, 15)

    # 施工许可格式
    work_sheet.set_column(21, 21, 10, align)
    work_sheet.set_column(22, 24, 15)

    # 竣工验收备案格式
    work_sheet.set_column(25, 25, 10, align)
    work_sheet.set_column(26, 29, 15)

    tab_title = ['公司名称', '项目名称', '工程分类', '工程用途', '总投资','总面积',       # 0 - 5
                 '招投标数量','招标类型','招标方式','中标单位名称','中标日期', '中标金额（万元）', # 6 - 11
                 '施工图审查数量', '勘察单位名称', '设计单位名称', '施工图审查机构名称', '审查完成日期',  # 12 - 16
                 '合同备案数量', '合同类别', '合同金额（万元）', '合同签订日期',    # 17 - 20
                 '施工许可数量', '合同金额（万元）', '面积（平方米）', '发证日期',   # 21 - 24
                 '竣工验收备案数量','实际造价（万元）', '实际面积（平方米）', '实际开工日期', '实际竣工验收日期',] # 25 - 29
    # for title in range(len(tab_title)):
    # work_sheet.write_string(0,title,tab_title[title],table)
    work_sheet.write_row(0, 0, tab_title, table)
    index = 1

    # 正文写入
    for content in contents:
        content_dict = eval(content)
        project = Building(**content_dict)
        ztb_index, jgysba_index, sgxk_index, sgtsc_index, htba_index = 0, 0, 0, 0, 0
        if project.ztb:
            ztb_index = len(project.ztb[0])  # 获取需要写入数据的行数
            work_sheet.write(index, 6, ztb_index)  # 追加写入数据，注意是从i+rows_old行开始写入
            for i in range(1, len(project.ztb)-1):
                try:
                    value = max(list(map(float, project.ztb[i])))
                    work_sheet.write(index, 6+i, value)  # 追加写入数据，注意是从i+rows_old行开始写入
                except:
                    work_sheet.write(index, 6+i, max(project.ztb[i]))  # 追加写入数据，注意是从i+rows_old行开始写入

        if project.sgtsc:
            sgtsc_index = len(project.sgtsc[0])
            work_sheet.write(index, 12, sgtsc_index)
            for i in range(1, len(project.sgtsc)-1):
                try:
                    work_sheet.write(index, i+12, max(list(map(float, project.sgtsc[i]))))
                except:
                    work_sheet.write(index, i+12, max(project.sgtsc[i]))

        if project.htba:
            htba_index  = len(project.htba[0])
            work_sheet.write(index, 17, htba_index)
            for i in range(1, len(project.htba)-1):
                try:
                    work_sheet.write(index, i+17, max(list(map(float, project.htba[i]))))
                except:
                    work_sheet.write(index, i+17, max(project.htba[i]))

        if project.sgxk:
            sgxk_index = len(project.sgxk[0])
            work_sheet.write(index, 21, sgxk_index)
            for i in range(1, len(project.sgxk)-1):
                try:
                    work_sheet.write(index, i+21, max(list(map(float, project.sgxk[i]))))
                except:
                    work_sheet.write(index, i+21, max(project.sgxk[i]))

        if project.jgysba:
            jgysba_index = len(project.jgysba[0])  # 获取需要写入数据的行数
            work_sheet.write(index, 25, jgysba_index)
            for j in range(1, len(project.jgysba)-1):
                try:
                    work_sheet.write(index, j+25, max(list(map(float, project.jgysba[j]))))  # 追加写入数据，注意是从i+rows_old行开始写入
                except:
                    work_sheet.write(index, j+25, max(project.jgysba[j]))  # 追加写入数据，注意是从i+rows_old行开始写入


        work_sheet.write_string(index, 0, project.company)
        work_sheet.write_url(index, 1, project.url,string=project.title)
        work_sheet.write_string(index, 2, project.cls)
        work_sheet.write_string(index, 3, project.use)
        all_money = float(project.all_money.replace('（万元）','').replace('-', '0'))
        all_area = float(project.all_area.replace('（平方米）','').replace('-', '0'))
        work_sheet.write(index, 4, all_money)
        work_sheet.write(index, 5, all_area)

        index = index + 1
        # Add a format. Light red fill with dark red text.
        format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})
        # Add a format. Green fill with dark green text.
        format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                       'font_color': '#006100'})
        work_sheet.conditional_format(1,4,index,4, {'type': 'cell',
                                                    'criteria': '>=',
                                                    'value': 50000,
                                                    'format': format1})
        work_sheet.conditional_format(1,5,index,5, {'type': 'cell',
                                                    'criteria': '>=',
                                                    'value': 100000,
                                                    'format': format2})
        work_sheet.autofilter(0,0,index,10)
    workbook.close()


def save_to_excel(filename, sheetname, contents):
    workbook = xlsxwriter.Workbook(filename, {'strings_to_numbers': True, 'default_date_format': 'dd/mm/yy'})
    work_sheet = workbook.add_worksheet(sheetname)

    # 首行格式设置
    table = workbook.add_format({'border': 1, 'font_size': 16, 'bold': False, 'align': 'center', 'bg_color': 'yellow'})
    work_sheet.set_column(0, 0, 25)    # 第一列 公司名称
    work_sheet.set_column(1, 1, 80)
    work_sheet.set_column(2, 5, 20)
    tab_title = ['公司名称', '项目名称', '工程分类', '工程用途', '最大金钱','最大面积']
    work_sheet.write_row(0, 0, tab_title, table)
    index = 1

    # 正文写入
    for content in contents:
        content_dict = eval(content)
        project = Building(**content_dict)

        ztb = project.ztb[5] if project.ztb else []
        htba = project.htba[2] if project.htba else []
        sgxk = project.sgxk[1] if project.sgxk else []
        jgysba = project.jgysba[1] if project.jgysba else []
        sgxk_a = project.sgxk[2] if project.sgxk else []
        jgysba_a = project.jgysba[2] if project.jgysba else []

        max_money_lists = ztb + htba + sgxk + jgysba
        max_areas_lists = sgxk_a + jgysba_a
        all_money = project.all_money.replace('（万元）','').replace('-', '0')
        all_area = project.all_area.replace('（平方米）','').replace('-', '0')
        max_money_lists.append(all_money)
        max_areas_lists.append(all_area)
        max_money_lists = [x.replace('-', '0') for x in max_money_lists]
        max_areas_lists = [x.replace('-', '0') for x in max_areas_lists]

        max_money = max(list(map(float, max_money_lists)))
        max_areas = max(list(map(float, max_areas_lists)))

        work_sheet.write_string(index, 0, project.company)
        work_sheet.write_url(index, 1, project.url,string=project.title)
        work_sheet.write_string(index, 2, project.cls)
        work_sheet.write_string(index, 3, project.use)
        work_sheet.write(index, 4, max_money)
        work_sheet.write(index, 5, max_areas)

        index = index + 1

    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    # Add a format. Green fill with dark green text.
    format2 = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})
    work_sheet.conditional_format(1,4,index,4, {'type': 'cell',
                                                'criteria': '>=',
                                                'value': 50000,
                                                'format': format1})
    work_sheet.conditional_format(1,5,index,5, {'type': 'cell',
                                                'criteria': '>=',
                                                'value': 100000,
                                                'format': format2})
    work_sheet.autofilter(0,4,index,5)
    workbook.close()
