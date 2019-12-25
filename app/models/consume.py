# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 14:24
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT


# 消费平台
class HaoConsumePlate(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费平台名字	")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费种类
class HaoConsumeType(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费种类名字	")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费方式
class HaoConsumeWay(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费方式名字	")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费商家
class HaoConsumeShop(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费方式名字	")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费者
class HaoConsumeUser(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费者名字")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费者
class HaoConsumeDescription(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费说明")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")


# 消费
class HaoConsume(object):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    time = db.Column(db.DateTime, comment="消费时间")
    amount = db.Column(db.DECIMAL(15,2), comment="消费金额")
    plate = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_plate.id"), comment="消费平台")
    type = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_type.id"), comment="消费种类")
    way = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_way.id"), comment="消费方式")
    shop = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_shop.id"), comment="消费商家	")
    user = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_user.id"), comment="	消费者")
    description = db.Column(BIGINT(unsigned=True), db.ForeignKey("hao_consume_description.id"), comment="消费说明")