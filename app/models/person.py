# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/6 11:59
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime


class Person(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="人物主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="人物名字")
    bill_link = db.Column(db.String(500), nullable=True, comment="海报链接")
    sex = db.Column(db.Boolean, nullable=True, comment="性别：0男性，1女性")
    foreign_name = db.Column(db.String(100), nullable=True, comment="外语名字")
    birth_day = db.Column(db.Date, nullable=True, comment="出生日期")
    nationality_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), nullable=True, comment="国籍主键")
    birth_city_id =db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), nullable=True, comment="出生城市")
    origin_city_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), nullable=True, comment="籍贯城市")
    constellation_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("constellation.id"), nullable=True, comment="星座主键")
    blood_group_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("blood_group.id"), nullable=True, comment="血型主键")
    height = db.Column(db.DECIMAL(5, 1), nullable=True, comment="身高(CM)")
    weight = db.Column(db.DECIMAL(5, 1), nullable=True, comment="体重(G)")

    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment="修改时间")

    birth_city = db.relationship("City", backref="birth_persons", foreign_keys=[birth_city_id])
    origin_city = db.relationship("City", backref="origin_persons", foreign_keys=[origin_city_id])

    # 出演的电影列表
    def list_acted_movies(self):
        if len(self.acted_movies) == 0:
            return None
        list_name = [x.name for x in self.acted_movies]
        return '、'.join(list_name)
