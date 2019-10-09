#!/usr/bin/env python
import time

def background_task(param):
    delay = 2
    print('Entering background_task', flush=True)
    print('param = ', param, flush=True)
    type = param['type']
    if type != 'SAVE' and type != 'LOAD':
        return 1, 'Task type is not supported'

    print("Task running", flush=True)
    print(f"Simulating {delay} second delay", flush=True)

    time.sleep(delay)

    print("Task complete, leaving background_task", flush=True)

    if type == 'SAVE':
        return 0, 'Data Saved into the Database'
    if type == 'LOAD':
        return 0, 'Data Loaded from the Database'

    return 1, 'Error'
