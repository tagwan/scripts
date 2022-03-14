import redis


class RedisOpt:
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        r = redis.StrictRedis(host='192.168.189.4', port=50000, db=0, password="ssdtest")
        r.set('foo', 'bar')


if __name__ == '__main__':
    RedisOpt().run()
