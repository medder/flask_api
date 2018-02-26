# -*- coding: utf-8 -*-

from smart_getenv import getenv

LOGGER_NAME = 'app'

# mysql
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 0
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2000
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')

# secret key
SECRET_KEY = getenv('SECRET_KEY', default='test123')

try:
    from .local_config import *  # noqa
except ImportError:
    pass
