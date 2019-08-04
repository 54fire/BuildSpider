import redis

class Redis(object):

    def __init__(self):
        self.client = redis.StrictRedis(host='127.0.0.1', port=6379)

build_redis = Redis()