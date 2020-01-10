# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 11:11
# IDE：PyCharm

from app import db
import datetime
from sqlalchemy.dialects.mysql import BIGINT


class Estate(db.Model):
    __table_args__ = {'comment': '房屋小区信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房产主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="房产名称")
    address = db.Column(db.String(100), nullable=True, comment="门牌号码")
    district_id = db.Column("district_id", BIGINT(unsigned=True), db.ForeignKey("district.id"), nullable=True,
                               comment="区域所在")
    enterprise_id = db.Column("enterprise_id", BIGINT(unsigned=True), db.ForeignKey("enterprise.id"), nullable=True,
                            comment="承包公司")
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Building(db.Model):
    __table_args__ = {'comment': '房屋信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房产主键")
    surface = db.Column(db.DECIMAL(6, 2), nullable=False, comment="房屋面积")
    unit_price = db.Column(db.DECIMAL(6, 2), nullable=True, comment="单价")
    total_price = db.Column(db.DECIMAL(6, 2), nullable=False, comment="总价")
    has_elevator = db.Column(db.Boolean, nullable=True, comment="是否有电梯")
    build_time = db.Column(db.Date, nullable=True, comment="建造时间")
    lottery_time = db.Column(db.Date, nullable=True, comment="摇号时间")
    type_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("building_type.id"), nullable=True, comment="户型主键")
    property_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("building_property.id"), nullable=True, comment="产权主键")
    estate_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("estate.id"), nullable=True, comment="房屋小区")

    estate = db.relationship("Estate", backref="buildings", foreign_keys=[estate_id])
    type = db.relationship("BuildingType", backref="buildings", foreign_keys=[type_id])
    property = db.relationship("BuildingProperty", backref="buildings", foreign_keys=[property_id])

class BuildingType(db.Model):
    __table_args__ = {'comment': '房屋户型'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="户型主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="户型名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="更新时间")

class BuildingProperty(db.Model):
    __table_args__ = {'comment': '房屋产权属性'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="产权属性主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="产权属性名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="更新时间")
