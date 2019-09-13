from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import threading
from queue import Queue
from lxml import etree
import requests
import time

from utils.http import get_request_headers



class CheckIP(object):

    def __init__(self):
        self.url = "http://jzsc.mohurd.gov.cn/asite/jsbpp/index"
        self.queue = Queue()
        self.content_queue = Queue()
        self.coroutine_pool = Pool()

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        # 提供一个 run 方法，用于处理检测代理IP核心逻辑
        # 2.1 从文件中获取所以代理IP
        with open('../config/checkIP', 'r') as f:
            proxies = f.readlines()
        # 2.2 遍历代理IP列表
        for proxy in proxies:
            # self.__check_one_proxy(proxy)
            # 把代理ip添加到队列中
            proxy = proxy.strip()
            self.queue.put(proxy)

        threed_pool = []
        for i in range(0, 1000):
            t = threading.Thread(target=self.__check_one_proxy)
            threed_pool.append(t)
        for i in range(10):
            s = threading.Thread(target=self.__save_proxies)
            threed_pool.append(s)
        for t in threed_pool:
            t.setDaemon(True)
            t.start()
        self.queue.join()
        self.content_queue.join()
            # self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def __check_one_proxy(self):
        ''' 检查一个代理IP的可用性 '''
        while True:
            proxy = self.queue.get()
            proxies = {"http": "http://"+proxy}
            start_time = time.time()
            try:
                headers = get_request_headers()
                data = {"complexname": "中国建筑第五工程局有限公司"}
                res = requests.post(self.url, headers=headers, data=data, proxies=proxies, timeout=10)
                if (res.status_code == 200) and res.text[:3] != 'HTT':
                    ele = etree.HTML(res.text)
                    result = ele.xpath('//font/b/text()')
                    if result:
                        if result[0] == "全国建筑市场监管公共服务平台":
                            t = round(time.time()-start_time, 2)
                            print(t, proxies)
                            if t < 4:
                                self.content_queue.put(proxies)
                    else:
                        print("SB::", proxies)

                else:
                    print("不行的代理:", proxies, res.status_code)
            except:
                print("其他错误：", proxies)
            self.queue.task_done()

    def __save_proxies(self):
        while True:
            proxy = self.content_queue.get()
            with open('../config/building','a') as f:
                proxy = proxy["http"]
                f.write(proxy + '\n')
            self.content_queue.task_done()

if __name__ == '__main__':
    ip = CheckIP()
    ip.run()

