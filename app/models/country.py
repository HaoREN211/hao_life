# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 21:19
# IDE：PyCharm

from app import db
import datetime
from sqlalchemy.dialects.mysql import BIGINT
from app.models.movie import Movie
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from sqlalchemy.sql import func
from app.tools import get_standard_name

class Country(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="国家主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="国家名称")
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    movies = db.relationship("Movie", backref="country", lazy='dynamic')
    persons = db.relationship("Person", backref="nationality", lazy='dynamic')

    @hybrid_property
    def movie_cnt(self):
        return self.movies.count()

    @movie_cnt.expression
    def movie_cnt(cls):
        return (select([func.count(Movie.id)])
                .where(Movie.country_id == cls.id))

class Province(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="省份主键")
    country_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), nullable=True, comment="国家主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="省份名称")

    country = db.relationship("Country", backref="provinces", foreign_keys=[country_id])


    # 更新省份的国家id
    def update_country(self, country_id):
        self.country_id = int(country_id)
        self.update_cities_country()


    # 更新关联城市的国家信息
    def update_cities_country(self):
        for current_city in self.cities:
            current_city.country_id=self.country_id

class City(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="城市主键")
    country_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), nullable=True, comment="国家主键")
    province_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("province.id"), nullable=True, comment="省份主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="城市名称")

    province = db.relationship("Province", backref="cities", foreign_keys=[province_id])
    country = db.relationship("Country", backref="cities", foreign_keys=[country_id])

    # 更新城市的名称
    def update_name(self, new_name):
        new_name_standard = get_standard_name(new_name)
        if new_name_standard != self.name:
            self.name = new_name_standard
            return True
        return False

    # 更新省份的id
    def update_province_id(self, province_id):
        province_id_standard = None if int(province_id)==0 else int(province_id)
        if province_id_standard != self.province_id:
            self.province_id = province_id_standard
            self.update_country_id()
            return True
        return False

    # 根据省份更新城市的国家id
    def update_country_id(self):
        if not self.province_id is None:
            target_province = Province.query.filter_by(id=int(self.province_id)).first()
            self.country_id = target_province.country_id


class District(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="区主键")
    country_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), nullable=True, comment="国家主键")
    province_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("province.id"), nullable=True, comment="省份主键")
    city_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("city.id"), nullable=True, comment="城市主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="区名称")

    city = db.relationship("City", backref="districts", foreign_keys=[city_id])
    province = db.relationship("Province", backref="districts", foreign_keys=[province_id])
    country = db.relationship("Country", backref="districts", foreign_keys=[country_id])

    # 更新区域的名称
    def update_name(self, new_name):
        new_name_standard = get_standard_name(new_name)
        if new_name_standard != self.name:
            self.name = new_name_standard
            return True
        return False

    # 更新城市id
    def update_city_id(self, city_id):
        city_id_standard = int(city_id) if int(city_id)>0 else None
        if city_id_standard != self.city_id:
            self.city_id=city_id_standard
            self.update_province_id()
            return True
        return False


    # 根据区域所属城市更新区域的省份id
    def update_province_id(self):
        if not self.city is None:
            self.province_id = self.city.province_id
            self.update_country_id()

    # 根据区域所属省份id更新国家id
    def update_country_id(self):
        if not self.province is None:
            self.country_id = self.province.country_id


class Constellation(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="星座主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="星座名称")
    english_name = db.Column(db.String(100), unique=True, nullable=True, comment="星座英文名称")
    french_name = db.Column(db.String(100), unique=True, nullable=True, comment="星座发文名称")
    start_time = db.Column(db.Date, nullable=False, comment="开始时间")
    end_time = db.Column(db.Date, nullable=False, comment="结束时间")

    persons = db.relationship("Person", backref="constellation", lazy='dynamic')


class BloodGroup(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="血型主键")
    name = db.Column(db.String(5), unique=True, nullable=False, comment="血型名称")

    persons = db.relationship("Person", backref="blood_group", lazy='dynamic')