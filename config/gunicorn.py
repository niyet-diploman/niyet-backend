import multiprocessing
import os

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
name = 'niyet'

worker_class = 'sync'
if os.environ.get('CONTAINER_ENVIRONMENT') in ['local']:
    reload = True
    workers = 2
else:
    preload = True
