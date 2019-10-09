import redis
from rq import Connection, Worker

def run_worker():
    #redis_url = app.config['REDIS_URL']
    redis_url = 'redis://redis:6379/0'
    #redis_url = 'redis://localhost:6379/0'
    redis_connection = redis.from_url(redis_url)
    '''
    with Connection(redis_connection):
        #worker = Worker(app.config['QUEUES'])
        worker = Worker(['async_db_svc'])
        worker.work()
    '''
    worker = Worker(['async_db_svc'],
                    connection=redis_connection)
    worker.work()

if __name__ == '__main__':
    run_worker()
