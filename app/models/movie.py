# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:29
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime

class Movie(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="电影主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="电影名字")
    show_time = db.Column(db.Date, nullable=False, comment="上映时间")
    film_length = db.Column(db.Integer, nullable=False, comment="片长(分)")
    bill_link = db.Column(db.String(500), nullable=True, comment="海报链接")
    is_watched = db.Column(db.Boolean, nullable=True, comment="是否观看")
    watch_time = db.Column(db.Date, nullable=True, index=True, comment="观看时间")
    description = db.Column(db.Text(16777216), nullable=False, comment="电影简介")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")
    cinema_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("movie_cinema.id"), comment="电影院主键")


class MovieCinema(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="电影院主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="电影院名字")
    address = db.Column(db.String(100), nullable=False, unique=True, comment="电影院地址")

    movies = db.relationship("Movie", backref="cinema", lazy='dynamic')