import time, os

from core.building_spider.project_details import CodeProcuder,DetailProcuder,ProjectProcuder
from setting import company_code_queue, company_queue, post_proxy_queue, project_queue, detail_queue, proxy_queue, yes_queue, no_queue

names = os.listdir('fire/')

with open('./config/result', 'r', encoding='utf-8') as f1:
    for data in f1.readlines():
        if data.strip() not in names:
            company_queue.put(data.strip())

# for _ in range(company_queue.qsize()):
    # print(company_queue.get())


with open('./config/proxy', 'r', encoding='utf-8') as f1:
    for data in f1.readlines():
        proxy_queue.put(data.strip())

with open('./config/proxy', 'r', encoding='utf-8') as f1:
    for data in f1.readlines():
        post_proxy_queue.put(data.strip())

def run():
    procuders = list()
    # 设置寻找公司code的线程数
    for _ in range(1):
        procuders.append(CodeProcuder(company_queue, company_code_queue, proxy_queue))
    # 设置查询项目名称的线程数
    for _ in range(4):
        procuders.append(ProjectProcuder(company_code_queue, project_queue, proxy_queue, post_proxy_queue))
    # 设置获取项目细节的线程数(一般该数值较多)
    for _ in range(15):
        # 1. 需要查询的队列，2. 用来保存的队列，3. 代理ip队列
        procuders.append(DetailProcuder(project_queue, detail_queue, proxy_queue))

    for t in procuders:
        t.setDaemon(True)
        t.start()
    company_queue.join()
    company_code_queue.join()
    project_queue.join()



if __name__ == '__main__':
    s = time.time()
    run()
    print(time.time()-s)


