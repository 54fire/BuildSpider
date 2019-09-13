import os

def money_jus(temp, condition):
    if temp:
        mid_temp = []
        for tmp in temp:
            try:
                money = float(tmp['金额'])
                if money > condition:
                    mid_temp.append(tmp)
            except:
                pass
        return mid_temp
    return []

companys = os.listdir('fire/')
for company in companys:
    with open('fire/'+company, 'r') as f:
        contents = f.readlines()

    for content in contents:
        project = content.strip()
        project = eval(project)
        ztbs = project['ztb']
        htba = project['htba']
        sgxk = project['sgxk']
        jgysba = project['jgysba']

        project['ztb'] = money_jus(ztbs, 3000)
        project['htba'] = money_jus(htba, 3000)
        project['sgxk'] = money_jus(sgxk, 3000)
        project['jgysba'] = money_jus(jgysba, 3000)
        if (project['ztb'] or project['htba'] or project['sgxk'] or project['jgysba']):
            print(project)
            with open(project['company'], 'a') as f:
               f.write(str(project) + '\n')

