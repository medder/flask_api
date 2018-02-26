# -*- coding: utf-8 -*-

import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, exc
from sqlalchemy.pool import Pool

from backend.config import LOGGER_NAME


@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:  # noqa
        raise exc.DisconnectionError()
    try:
        cursor.close()
    except AttributeError:
        pass


# mysql
db = SQLAlchemy()

# redis
# rds = Redis.from_url(REDIS_URL)

FORMAT = ('[%(asctime)s] [%(process)d] [%(levelname)s] '
          '[%(filename)s @ %(lineno)s]: %(message)s')
# logger
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S %z')
logger = logging.getLogger(LOGGER_NAME)
hdlr = logging.FileHandler('/var/tmp/flask_api.log')
formatter = logging.Formatter(FORMAT)
hdlr.setFormatter(formatter)

logger.addHandler(hdlr)
