# -*- coding: utf-8 -*-

import json
from datetime import timedelta

from kazoo.client import KazooClient
from smart_getenv import getenv


def get_mysql_info_from_zk(hosts, path):
    """从 zk 拿数据库信息
    """
    if not all([hosts, path]):
        return None

    zk = KazooClient(hosts=hosts)
    zk.start()
    if not zk.exists(path):
        zk.stop()
        return None

    data, __ = zk.get(path)
    zk.stop()
    DATABASE_URI = ('mysql+pymysql://{user}:{password}@{host}:{port}/'
                    '{database}?charset=utf8mb4')
    return DATABASE_URI.format(**json.loads(data))


DEBUG = getenv('APP_DEBUG', default=False, type=bool)

LOGGER_NAME = 'app'

# mysql
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 0
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2000
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')

# photo 项目相关的数据库
PHOTO_DATABASE_URI = getenv('PHOTO_DATABASE_URI')
SQLALCHEMY_BINDS = {
    'photo': PHOTO_DATABASE_URI,
}

# secret key
SECRET_KEY = getenv('SECRET_KEY', default='test123')

# redis cache
# REDIS_URL = getenv('REDIS_URL', default='redis://localhost:6379/0')

# Photo 项目相关
# 后端更新订单、点赞的 URL
PHOTO_API_HOST = getenv('PHOTO_API_HOST', default='http://qatest.api.ofo.com')

# 是否展现状态为 0 的 Photo
SHOW_PHOTO_STATE_0 = getenv('SHOW_PHOTO_STATE_0', type=bool)

# ES config
ESEARCH_HOST = getenv('ESSEARCH_HOST', type=list)
ESEARCH_PORT = getenv('ESSEARCH_PORT', type=int, default=9200)
ESEARCH_INDEX = getenv('ESSEARCH_INDEX', default='ofo_photo_test')

# JWT config
JWT_AUTH_USERNAME_KEY = 'email'
JWT_EXPIRATION_DELTA = timedelta(hours=8)
JWT_AUTH_URL_RULE = '/api/auth'

# MACHINE_TOKEN
MACHINE_TOKEN = getenv('MACHINE_TOKEN')

# aliyun OSS
ACCESS_KYE_ID = getenv('ACCESS_KYE_ID')
ACCESS_KYE_SECRET = getenv('ACCESS_KYE_SECRET')
END_POINT = getenv('END_POINT')
BUCKET = getenv('BUCKET')
OSS_URL = getenv('OSS_URL')

try:
    from .local_config import *  # noqa
except ImportError:
    pass
