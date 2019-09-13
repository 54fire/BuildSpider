import redis, json

from domain import Building

class RedisClinet(object):

    def __init__(self, type, website):
        self.db = redis.StrictRedis()
        self.type = type
        self.website = website

    def __name(self):
        '''
        获取Hash的名称
        :return: Hash的名称
        '''
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        '''
        设置键值对
        :param username: 公司名称
        :param value: 公司的code
        :return:
        '''
        return self.db.hset(self.__name(), username, value)

    def get(self, username):
        return self.db.hget(self.__name(), username)

    def exist(self, username):
        return self.db.hexists(self.__name(), username)

    def delete(self, username):
        return self.db.hdel(self.__name(), username)

    def usernames(self):
        return self.db.hkeys(self.__name())

    def count(self):
        return self.db.hlen(self.__name())

if __name__ == '__main__':
    company = RedisClinet("company", 'code')
    vals = company.db.hgetall("company:code")
    for k, v in vals.items():
        if v.decode() == 'None':
            print(k.decode())
    ls = company.count()
    print(ls)
