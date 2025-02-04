import redis
import threading
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)

def worker():
    r = redis.Redis(connection_pool=pool)
    # Perform Redis operations with 'r'

threads = [threading.Thread(target=worker) for _ in range(5)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()