# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/9 9:55
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT

class Enterprise(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="企业主键")
    name = db.Column(db.String(100), unique=True, nullable=True, comment="企业名称")
    short_name = db.Column(db.String(100), unique=True, nullable=True, comment="企业简称")
    founded_time = db.Column(db.Date, nullable=False, comment="创立时间")
    president_id = db.Column("person_id", BIGINT(unsigned=True), db.ForeignKey("person.id"), nullable=True, comment="总裁主键")
    headquarter_id = db.Column("district_id", BIGINT(unsigned=True), db.ForeignKey("district.id"), nullable=True, comment="总部主键")

    president = db.ForeignKey("Person", backref="enterprises", foreign_keys=[president_id])
    headquarter = db.ForeignKey("District", backref="enterprises", foreign_keys=[headquarter_id])