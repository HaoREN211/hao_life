# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:29
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime


movie_movie_type = db.Table('movie_movie_type',
    db.Column("id", BIGINT(unsigned=True), primary_key=True, comment="电影类型匹配主键"),
    db.Column("movie_id", BIGINT(unsigned=True), db.ForeignKey("movie.id"), comment="电影主键"),
    db.Column("type_id", BIGINT(unsigned=True), db.ForeignKey("movie_type.id"), comment="类型主键"),
    db.Column('create_time', db.TIMESTAMP, comment='创建时间', default=datetime.utcnow())
)


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
    country_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("country.id"), comment="拍摄国家主键")

    types = db.relationship('MovieType', secondary = movie_movie_type, lazy='dynamic')

    # 获取电影类型的字符串
    def type_name_list(self):
        if self.types.count() == 0:
            return ""
        return "、".join([str(x.name) for x in self.types])

    # 更新电影的类型
    def update_type_by_list_type_id(self, list_type_id):
        info = ""
        result = self.delete_type_by_list_type_id(list_type_id)
        if result:
            info += "成功删除电影类型："+result+"。"
        result = self.add_type_by_list_type_id(list_type_id)
        if result:
            info += "成功添加电影类型："+result+"。"
        return info

    # 删除没有在list_type_id中的电影类型
    def delete_type_by_list_type_id(self, list_type_id):
        list_typed_id = [int(x.id) for x in self.types]
        list_type_id = [int(x) for x in list_type_id]
        list_element_delete = list([])
        for current_list_typed_id in list_typed_id:
            if not current_list_typed_id in list_type_id:
                current_type = MovieType.query.filter_by(id=int(current_list_typed_id)).first()
                list_element_delete.append(current_type.name)
                self.types.remove(current_type)
        return ",".join(list_element_delete)

    # 新增list_type_id里所有的type
    def add_type_by_list_type_id(self, list_type_id):
        list_element_add = list([])
        for current_type_id in list_type_id:
            current_type = MovieType.query.filter_by(id=int(current_type_id)).first()
            current_result = self.add_type(current_type)
            if current_result:
                list_element_add.append(current_result)
        return ",".join(list_element_add)

    # 电影是否有movie_type的类型
    def has_type(self, movie_type):
        return self.types.filter(movie_movie_type.c.type_id == int(movie_type.id)).count() > 0

    # 电影添加movie_type的类型
    def add_type(self, movie_type):
        if not self.has_type(movie_type):
            self.types.append(movie_type)
            return movie_type.name
        return ""

class MovieCinema(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="电影院主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="电影院名字")
    address = db.Column(db.String(100), nullable=False, unique=True, comment="电影院地址")

    movies = db.relationship("Movie", backref="cinema", lazy='dynamic')


class MovieType(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="电影类型主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="电影类型名字")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")
