import threading, time

from core.building_spider.detail_spider import CodeProcuder,DetailProcuder,ProjectProcuder
from core.building_spider.filter_project import FilterProject
from core.building_spider.save import save_file
from setting import company_code_queue, company_queue, post_proxy_queue, project_queue, detail_queue, proxy_queue, yes_queue, no_queue
from setting import YES_FILE, NO_FILE

with open('./config/result', 'r') as f1:
    for data in f1.readlines():
        company_queue.put(data.strip())

with open('./config/proxy', 'r') as f1:
    for data in f1.readlines():
        proxy_queue.put(data.strip())

with open('./config/post_proxy', 'r') as f1:
    for data in f1.readlines():
        post_proxy_queue.put(data.strip())

def run():
    procuders = list()
    for _ in range(3):
        procuders.append(CodeProcuder(company_queue, company_code_queue, proxy_queue))
        procuders.append(ProjectProcuder(company_code_queue, project_queue, proxy_queue, post_proxy_queue))
        procuders.append(FilterProject(project_queue, yes_queue, no_queue, 'yes'))
    for _ in range(10):
        # 1. 需要查询的队列，2. 用来保存的队列，3. 代理ip队列
        procuders.append(DetailProcuder(yes_queue, detail_queue, proxy_queue))

    for t in procuders:
        t.setDaemon(True)
        t.start()
    company_queue.join()
    company_code_queue.join()
    project_queue.join()
    yes_queue.join()

    save_file(YES_FILE, detail_queue)
    save_file(NO_FILE, no_queue)


if __name__ == '__main__':
    s = time.time()
    run()
    print(time.time()-s)


