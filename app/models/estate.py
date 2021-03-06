# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 11:11
# IDE：PyCharm

from app import db
import datetime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from sqlalchemy.sql import func


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

    enterprise = db.relationship("Enterprise", backref="estates", foreign_keys=[enterprise_id])
    district = db.relationship("District", backref="estates", foreign_keys=[district_id])

    @hybrid_property
    def building_cnt(self):
        return len(self.buildings)

    @building_cnt.expression
    def building_cnt(cls):
        return (select([func.count(Building.id)])
                .where(Building.estate_id == cls.id))


class DistrictTimes(db.Model):
    __table_args__ = (db.UniqueConstraint("estate_id", "times"), )
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="楼盘期数主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="楼盘名称")
    estate_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("estate.id"), nullable=False, comment="楼盘主键")
    times = db.Column(db.Integer, nullable=False, comment="楼盘期数")
    start_register_time = db.Column(db.Date, nullable=True, comment="登记开始时间")
    end_register_time = db.Column(db.Date, nullable=True, comment="登记结束时间")
    lotto_date = db.Column(db.Date, nullable=True, comment="摇号时间")
    pick_date = db.Column(db.Date, nullable=True, comment="选房时间")

    estate = db.relationship("Estate", backref="district_times", foreign_keys=[estate_id])


class Apartment(db.Model):
    __table_args__ = (db.UniqueConstraint("district_times_id", "order"),
                      db.UniqueConstraint("district_times_id", "building_number", "floor", "number"),
                      {"comment": "一户一价明细"})
    name = db.Column(db.String(100), unique=True, nullable=True, comment="一户一价名称")
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="一户一价主键")
    district_times_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("district_times.id"), nullable=False, comment="楼盘主键")
    order = db.Column(db.Integer, nullable=True, comment="当前楼盘顺序")
    building_number = db.Column(db.Integer, nullable=True, comment="栋数")
    floor = db.Column(db.Integer, nullable=True, comment="楼层")
    number = db.Column(db.Integer, nullable=True, comment="号数")
    size = db.Column(db.DECIMAL(6, 2), nullable=True, comment="建筑面积(平方米)")
    unique_price = db.Column(db.DECIMAL(8, 2), nullable=True, comment="单价(元)")
    total_price = db.Column(db.DECIMAL(6, 2), nullable=True, comment="总价(万元)")

    district_times = db.relationship("DistrictTimes", backref="apartments", foreign_keys=[district_times_id])

    def upgrade_name(self):
        tmp_name = ""
        if self.district_times is not None:
            tmp_name = self.district_times.name
        if self.building_number is not None:
            tmp_name += str(self.building_number)+"栋"
        if self.floor is not None:
            tmp_name += str(self.floor) + "层"
        if self.number is not None:
            tmp_name += str(self.number) + "号"
        self.name = tmp_name


class Building(db.Model):
    __table_args__ = {'comment': '房屋信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房产主键")
    surface = db.Column(db.DECIMAL(6, 2), nullable=False, comment="房屋面积")
    unit_price = db.Column(db.DECIMAL(8, 2), nullable=True, comment="单价")
    total_price = db.Column(db.DECIMAL(6, 2), nullable=False, comment="总价")
    total_level = db.Column(db.Integer, nullable=True, comment="总楼层")
    has_elevator = db.Column(db.Boolean, nullable=True, comment="是否有电梯")
    build_time = db.Column(db.Date, nullable=True, comment="建造时间")
    lottery_time = db.Column(db.Date, nullable=True, comment="摇号时间")
    type_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("building_type.id"), nullable=True, comment="户型主键")
    property_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("building_property.id"), nullable=True, comment="产权主键")
    estate_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("estate.id"), nullable=True, comment="房屋小区")
    owner_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("building_owner.id"), nullable=True, comment="房屋属性：二手房或新房")
    link = db.Column(db.String(500), nullable=True, comment="网页链接")
    image = db.Column(db.String(100), nullable=True, comment="图片链接")

    estate = db.relationship("Estate", backref="buildings", foreign_keys=[estate_id])
    type = db.relationship("BuildingType", backref="buildings", foreign_keys=[type_id])
    property = db.relationship("BuildingProperty", backref="buildings", foreign_keys=[property_id])
    owner = db.relationship("BuildingOwner", backref="buildings", foreign_keys=[owner_id])

    # 更新房屋单价
    def upgrade_unit_price(self):
        self.unit_price = float(self.total_price)*float(10000)/float(self.surface)

class BuildingType(db.Model):
    __table_args__ = {'comment': '房屋户型'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="户型主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="户型名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="更新时间")

    @hybrid_property
    def building_cnt(self):
        return len(self.buildings)

    @building_cnt.expression
    def building_cnt(cls):
        return (select([func.count(Building.id)])
                .where(Building.type_id == cls.id))

class BuildingProperty(db.Model):
    __table_args__ = {'comment': '房屋产权属性'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="产权属性主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="产权属性名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="更新时间")

    @hybrid_property
    def building_cnt(self):
        return len(self.buildings)

    @building_cnt.expression
    def building_cnt(cls):
        return (select([func.count(Building.id)])
                .where(Building.property_id == cls.id))


class BuildingOwner(db.Model):
    __table_args__ = {'comment': '二手房或新房'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="二手房或新房主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="二手房或新房名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="更新时间")

    @hybrid_property
    def building_cnt(self):
        return len(self.buildings)

    @building_cnt.expression
    def building_cnt(cls):
        return (select([func.count(Building.id)])
                .where(Building.owner_id == cls.id))
