# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/23 20:35
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from sqlalchemy.sql import func

class Train(db.Model):
    __table_args__ = {'comment': '火车票信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="火车票主键")

    cost = db.Column(db.DECIMAL(10, 2), nullable=True, comment="票价花费")

    time_from = db.Column(db.DateTime, nullable=True, comment="乘坐时间", unique=True)
    time_to = db.Column(db.DateTime, nullable=True, comment="到站时间", unique=True)

    city_from_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), comment="乘坐地主键")
    city_to_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), comment="终点站主键")

    train_number_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("train_number.id"), comment="火车班次主键")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="创建者主键")
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    train_number = db.relationship("TrainNumber", backref="trains", foreign_keys=[train_number_id])

    city_from = db.relationship("City", backref="train_from_cities", foreign_keys=[city_from_id])
    city_to = db.relationship("City", backref="train_to_cities", foreign_keys=[city_to_id])

# 班次信息
class TrainNumber(db.Model):
    __table_args__ = {'comment': '火车班次信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="火车班次主键")

    name = db.Column(db.String(100), nullable=True, comment="班次名字", unique=True)
    city_from_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), comment="始发地主键")
    city_to_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), comment="终点站主键")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="创建者主键")
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    city_from = db.relationship("City", backref="train_number_from_cities", foreign_keys=[city_from_id])
    city_to = db.relationship("City", backref="train_number_to_cities", foreign_keys=[city_to_id])

    # 关联的出行次数
    @hybrid_property
    def train_cnt(self):
        return len(self.trains)

    @train_cnt.expression
    def train_cnt(cls):
        return select([func.count(Train.id)]).where(Train.train_number_id == cls.id)