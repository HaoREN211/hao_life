# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 14:24
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from  sqlalchemy.sql import func


# 消费平台
class ConsumePlate(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费平台名字", unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def consume_cnt(self):
        return len(self.consumes)

    @consume_cnt.expression
    def consume_cnt(cls):
        return (select([func.count(Consume.id)])
                .where(Consume.plate_id == cls.id))


# 消费种类
class ConsumeType(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费种类名字", unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def consume_cnt(self):
        return len(self.consumes)

    @consume_cnt.expression
    def consume_cnt(cls):
        return (select([func.count(Consume.id)])
                .where(Consume.type_id == cls.id))


# 消费方式
class ConsumeWay(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费方式名字", unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def consume_cnt(self):
        return len(self.consumes)

    @consume_cnt.expression
    def consume_cnt(cls):
        return (select([func.count(Consume.id)])
                .where(Consume.way_id == cls.id))

# 消费商家
class Shop(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="商店名字", unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def consume_cnt(self):
        return len(self.consumes)

    @consume_cnt.expression
    def consume_cnt(cls):
        return (select([func.count(Consume.id)])
                .where(Consume.shop_id == cls.id))


# 消费者
class ConsumeDescription(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    name = db.Column(db.String(100), comment="消费说明", unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def consume_cnt(self):
        return len(self.consumes)

    @consume_cnt.expression
    def consume_cnt(cls):
        return (select([func.count(Consume.id)])
                .where(Consume.description_id == cls.id))


# 消费
class Consume(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="消费主键")
    time = db.Column(db.DateTime, comment="消费时间", unique=True)
    amount = db.Column(db.DECIMAL(15,2), comment="消费金额")
    plate_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("consume_plate.id"), comment="消费平台")
    type_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("consume_type.id"), comment="消费种类")
    way_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("consume_way.id"), comment="消费方式")
    shop_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("shop.id"), comment="消费商家	")
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="	消费者")
    description_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("consume_description.id"), comment="消费说明")

    shop = db.relationship("Shop", backref="consumes", foreign_keys=[shop_id])
    way = db.relationship("ConsumeWay", backref="consumes", foreign_keys=[way_id])
    description = db.relationship("ConsumeDescription", backref="consumes", foreign_keys=[description_id])
    plate = db.relationship("ConsumePlate", backref="consumes", foreign_keys=[plate_id])
    type = db.relationship("ConsumeType", backref="consumes", foreign_keys=[type_id])