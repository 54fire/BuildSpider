import redis, json
from domain import Building

class BulidRedis(object):

    def __init__(self, key):
        self.client = redis.StrictRedis()
        self.key = key

    def qsize(self):
        return self.client.llen(self.key)

    def put(self, value):
        self.client.rpush(self.key, value)

    def get(self):
        return self.client.lpop(self.key).decode()

data = {'company': '上海宝冶集团有限公司', 'title': '国家雪车雪橇中心', 'cls': '其他', 'url': 'http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/1100001712189906', 'use': '', 'all_money': '136569.2（万元）', 'all_area': '125937（平方米）', 'ztb': (['1'], ['施工'], ['公开招标'], ['上海宝冶集团有限公司'], ['2017-12-18'], ['136569.2'], ['/dataservice/query/project/tenderInfo/4068179']), 'sgtsc': [], 'htba': (['1'], ['施工总包'], ['136569.2'], ['2017-12-18'], ['/dataservice/query/project/contractInfo/2318001']), 'sgxk': [], 'jgysba': []}
data = Building(**data)
print(type(data), data)
build_redis = BulidRedis('company_queue')
build_redis.put(data)
print(build_redis.qsize())
val = eval(build_redis.get())
print(type(val), val)