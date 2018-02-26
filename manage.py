# -*- coding: utf-8 -*-

import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# 如果需要使用migrate创建表，需要在此导入
from backend.apps.example.models import * # noqa

from backend.backend import create_backend
from backend.client import db

backend = create_backend()
dsn = backend.config['SQLALCHEMY_DATABASE_URI']
if not ('127.0.0.1' in dsn or 'localhost' in dsn):
    print("you are not doing this on your own computer")
    print("线上数据库变更联系sa")
    sys.exit()

db.init_app(backend)

migrate = Migrate(backend, db)

manager = Manager(backend)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
