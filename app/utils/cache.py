import redis
import config

def check_execution_type():
    if 'docker' in open('/proc/1/cgroup').read():
        return 'docker'
    else:
        return 'python'

execution_type = check_execution_type()
if execution_type == 'docker':
    redis_host = config.REDIS_HOST
else:
    redis_host = 'localhost'

class CacheService:
    def __init__(self):
        self.redis = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(
                host=redis_host, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True))


cache  = CacheService()