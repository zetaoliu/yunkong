import redis


class RedisTool:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)

    def set(self, key, val):
        self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)

    def decr(self, key, amount=1):
        self.r.decr(key, amount)

    def delKey(self, key):
        self.r.delete(key)

    # 模糊删除
    def delLikeKeys(self, key):
        keys = self.r.keys(f'{key}*')
        for key in keys:
            self.delKey(key)
