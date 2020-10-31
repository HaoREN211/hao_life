# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2019/12/21 8:04
# IDE：PyCharm

import os
from config_db import ConfigDb

CURRENT_WORK_EXPERIENCE_ID = 3

class Config(object):
    # 分页功能，每页显示的个数
    POSTS_PER_PAGE = 10

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-hao-guess'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = ConfigDb.USERNAME
    PASSWORD = ConfigDb.PASSWORD
    HOST = ConfigDb.HOST
    PORT = ConfigDb.PORT
    DATABASE = ConfigDb.DATABASE
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    # 设置是否在每次连接结束后自动提交数据库中的变动。
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库连接池的大小。默认是引擎默认值（通常 是 5 ）
    SQLALCHEMY_POOL_SIZE = 10

    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接使用后回收到连接池后将会被断开和抛弃。
    # 保证连接池只有设置的大小；
    SQLALCHEMY_MAX_OVERFLOW = 5

    # 设定连接池的连接超时时间。默认是 10 。
    SQLALCHEMY_POOL_TIMEOUT = 10

    # 设置多少秒后回收连接，在使用 MySQL 时是必须设置的。
    SQLALCHEMY_POOL_RECYCLE = 30

    BOOTSTRAP_SERVE_LOCAL = True

class PageConfig(object):
    TITLE = "任皓的数据统计"
