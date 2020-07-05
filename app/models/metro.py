# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/3/9 17:03
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT

metro_station_order = db.Table("metro_station_order",
    db.Column("metro_station_id",
        BIGINT(unsigned=True),
        db.ForeignKey('metro_station.id'),
        comment='地铁站'),
    db.Column("metro_order_id",
        BIGINT(unsigned=True),
        db.ForeignKey('metro_order.id'),
        comment='地铁顺序'),
    db.UniqueConstraint("metro_station_id", "metro_order_id", name="metro_station_order_unique")
)

metro_station_issue = db.Table("metro_station_issue",
    db.Column("metro_station_id",
        BIGINT(unsigned=True),
        db.ForeignKey('metro_station.id'),
        comment='地铁站'),
    db.Column("metro_issue_id",
        BIGINT(unsigned=True),
        db.ForeignKey('metro_issue.id'),
        comment='地铁期数'),
    db.UniqueConstraint("metro_station_id", "metro_issue_id", name="metro_station_issue_unique")
)

class Metro(db.Model):
    __table_args__ = {'comment': '地铁轨道交通'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="地铁主键")
    city_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("movie.id"), comment="城市主键", unique=True)
    name = db.Column(db.String(20), nullable=True, unique=True, comment="轨道交通名称")

class MetroStation(db.Model):
    __table_args__ = {'comment': '地铁站信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="地铁站主键")
    metro_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("metro.id"), comment="地铁主键")
    name = db.Column(db.String(20), nullable=False, unique=True, comment="地铁站名")
    address = db.Column(db.String(100), nullable=True, unique=True, comment="地铁站地址")

    station_order = db.relationship('StationOrder', secondary=metro_station_order)
    station_issue = db.relationship('StationIssue', secondary=metro_station_issue)

class MetroLine(db.Model):
    __table_args__ = {'comment': '地铁线路信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="地铁线路主键")
    numeric_name = db.Column(db.Integer, nullable=False, unique=True, comment="地铁几号线")
    name = db.Column(db.String(20), nullable=False, unique=True, comment="地铁几号线")

class MetroOrder(db.Model):
    __table_args__ = (db.UniqueConstraint("metro_line_id", "order", name="metro_line_order_unique"), )
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="地铁顺序主键")
    order = db.Column(db.Interval, nullable=False, comment="地铁站在该线路上的顺序")
    metro_line_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("metro_line.id"), comment="地铁线路主键")

class MetroIssue(db.Model):
    __table_args__ = (db.UniqueConstraint("metro_line_id", "issue", name="metro_line_order_unique"),)
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="地铁期数主键")
    issue = db.Column(db.Interval, nullable=False, comment="地铁线路期数")
    metro_line_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("metro_line.id"), comment="地铁线路主键")
