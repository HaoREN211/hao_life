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


class City(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="城市主键")
    country_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), comment="国家主键")
    name = db.Column(db.String(100), unique=True, nullable=False, comment="城市名称")


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