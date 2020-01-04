# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 21:19
# IDE：PyCharm

from app import db
import datetime
from sqlalchemy.dialects.mysql import BIGINT

class Country(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="国家主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="国家名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    movies = db.relationship("Movie", backref="country", lazy='dynamic')
