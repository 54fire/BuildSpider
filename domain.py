
class Building(object):

    def __init__(self, company='', title='', cls='', use='', url='', all_money='', all_area='', ztb=[], sgtsc=[], htba=[], sgxk=[], jgysba=[]):
        # 公司名字
        self.company = company
        # 项目名字
        self.title = title
        # 项目类别
        self.cls = cls
        # 项目url
        self.url = url
        # 项目用途
        self.use = use
        # 项目总投资
        self.all_money = all_money
        # 项目总面积
        self.all_area = all_area
        # 项目招投标信息
        self.ztb  = ztb
        # 项目施工图审查
        self.sgtsc = sgtsc
        # 项目合同备案
        self.htba = htba
        # 项目施工许可
        self.sgxk = sgxk
        # 项目竣工验收备案信息
        self.jgysba = jgysba


    def __str__(self):
        # 返回一个字符串
        return str(self.__dict__)