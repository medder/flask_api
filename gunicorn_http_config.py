# -*- coding: utf-8 -*-
import multiprocessing

import gevent.monkey
from smart_getenv import getenv

gevent.monkey.patch_all()

bind = getenv('BIND', default='0.0.0.0:5000')

worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1

max_requests = 10000

debug = False

log_level = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'  # noqa
accesslog = getenv('ACCESSLOG', default='access.log')
errorlog = getenv('ERRORLOG', default='error.log')
