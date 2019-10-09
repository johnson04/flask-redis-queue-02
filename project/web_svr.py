#!/usr/bin/env python
from flask import Flask, request, render_template, jsonify
import redis
from rq import Queue
from jobs import background_task

app = Flask(__name__)

#r = redis.Redis()
#url = 'redis://localhost:6379/0'
url = 'redis://redis:6379/0'
r = redis.from_url(url)

'''
class Queue(object):
    job_class = Job
    DEFAULT_TIMEOUT = 180 # Default timeout seconds.
    redis_queue_namespace_prefix = 'rq:queue:'
    redis_queues_keys = 'rq:queues'

    def __init__(self,
                 name            = 'default',
                 default_timeout = None,
                 connection      = None,
                 is_async        = True,
                 job_class       = None,
                 **kwargs):
        self.connection = resolve_connection(connection)
        prefix = self.redis_queue_namespace_prefix
        self.name = name
        self._key = '{0}{1}'.format(prefix, name)
        self._default_timeout = parse_timeout(default_timeout) or self.DEFAULT_TIMEOUT
        self._is_async = is_async
        if 'async' in kwargs:
            self._is_async = kwargs['async']
            warnings.warn('The `async` keyword is deprecated. User `is_async` instead',
                          DeprecationWarning)
        # override class attribute job_class if one was passed
        if job_class is not None:
            if isinstance(job_class, string_types):
                job_class = import_attribute(job_class)
            self.job_class = job_class
'''
q = Queue(name            = 'async_db_svc',
          default_timeout = None,
          connection      = r,
          is_async        = True,
          job_class       = None)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/tasks", methods=['POST'])
def add_task():
    # param = request.args.get("type")
    param = request.get_json()
    #param = request.form['type']
    print("add_task is called", flush=True)
    print('param = ', param, flush=True)
    if param:
        print(param, flush=True)
        try:
            # q_len = len(q)
            # print('q_len0 = ', q_len, flush=True)
            job = q.enqueue(background_task, param)
            # q_len = len(q)
            # print('q_len1 = ', q_len, flush=True)
            response_object = {
                'status': 'success',
                'data': {
                    'task_id': job.get_id()
                }
            }
            print('res = ', response_object, flush=True)
            return jsonify(response_object), 202
            # return f"Task {job.id} added to queue at {job.enqueued_at}, {q_len} tasks in the queue"
        except Exception as e:
            response_object = {
                'status': 'failed',
                'data': {
                    'error': str(e)
                }
            }
            print('res = ', response_object, flush=True)
            return jsonify(response_object), 400
            # return "q.enqueue() failed"
    return jsonify({}), 200

@app.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    print('Entering get_status', flush=True)
    print('task_id = ', task_id, flush=True)
    if q:
        task = q.fetch_job(task_id)
        print('task.get_id() = ', task.get_id(), flush=True)
        print('task.get_status() = ', task.get_status(), flush=True)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id':     task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    print('res = ', response_object, flush=True)
    return jsonify(response_object)

if __name__ == "__main__":
    app.run()

