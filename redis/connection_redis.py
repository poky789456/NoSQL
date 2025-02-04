import redis
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)

r1 = redis.Redis(connection_pool=pool)
r2 = redis.Redis(connection_pool=pool)
