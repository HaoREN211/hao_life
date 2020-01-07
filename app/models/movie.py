# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:29
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import select
from app.models.person import Person


movie_movie_type = db.Table('movie_movie_type',
    db.Column("id", BIGINT(unsigned=True), primary_key=True, comment="电影类型匹配主键"),
    db.Column("movie_id", BIGINT(unsigned=True), db.ForeignKey("movie.id"), comment="电影主键"),
    db.Column("type_id", BIGINT(unsigned=True), db.ForeignKey("movie_type.id"), comment="类型主键"),
    db.Column('create_time', db.TIMESTAMP, comment='创建时间', default=datetime.utcnow()),
    db.UniqueConstraint('movie_id', 'type_id', name='movie_movie_type_match_unique')
)

movie_movie_actor = db.Table(
    'movie_movie_actor',
    db.Column("id", BIGINT(unsigned=True), primary_key=True, comment="电影演员匹配主键"),
    db.Column("movie_id", BIGINT(unsigned=True), db.ForeignKey("movie.id"), comment="电影主键"),
    db.Column("person_id", BIGINT(unsigned=True), db.ForeignKey("person.id"), comment="演员主键"),
    db.Column('create_time', db.TIMESTAMP, comment='创建时间', default=datetime.utcnow()),
    db.UniqueConstraint('movie_id', 'person_id', name='movie_movie_actor_match_unique')
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
    actors = db.relationship('Person', backref="acted_movies", secondary=movie_movie_actor, lazy='dynamic')

    # 获取电影演员的名字字符串列表
    def actor_name_list(self):
        if self.actors.count() == 0:
            return ""
        return "、".join([str(x.name) for x in self.actors])

    def update_actor_by_list_actor_id(self, list_actor_id):
        info = ""
        result = self.delete_actor_by_list_actor_id(list_actor_id)
        if result:
            info += "成功删除电影演员：" + result + "。"
        result = self.add_actor_by_list_actor_id(list_actor_id)
        if result:
            info += "成功添加电影演员：" + result + "。"
        return info

    # 删除没有在list_actor_id中的电影演员
    def delete_actor_by_list_actor_id(self, list_actor_id):
        list_has_actor_id = [int(x.id) for x in self.actors]
        list_has_actor_id = [int(x) for x in list_has_actor_id]
        list_element_delete = list([])
        for current_has_actor_id in list_has_actor_id:
            if not current_has_actor_id in list_actor_id:
                current_actor = Person.query.filter_by(id=int(current_has_actor_id)).first()
                list_element_delete.append(current_actor.name)
                self.actors.remove(current_actor)
        return ",".join(list_element_delete)

    # 新增list_actor_id里所有的actor
    def add_actor_by_list_actor_id(self, list_actor_id):
        list_element_add = list([])
        for current_actor_id in list_actor_id:
            current_actor = Person.query.filter_by(id=int(current_actor_id)).first()
            current_result = self.add_actor(current_actor)
            if current_result:
                list_element_add.append(current_result)
        return ",".join(list_element_add)

    # 电影是否有movie_actor的演员
    def has_actor(self, movie_actor):
        return self.actors.filter(movie_movie_actor.c.person_id == int(movie_actor.id)).count() > 0

    # 电影添加movie_actor的类型
    def add_actor(self, movie_actor):
        if not self.has_actor(movie_actor):
            self.actors.append(movie_actor)
            return movie_actor.name

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

    @hybrid_property
    def movie_cnt(self):
        return self.movies.count()

    @movie_cnt.expression
    def movie_cnt(cls):
        return (select([func.count(Movie.id)])
                .where(Movie.cinema_id == cls.id))


class MovieType(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="电影类型主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="电影类型名字")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")

    movies = db.relationship('Movie', secondary=movie_movie_type, lazy='dynamic')

    # it can be used to filter and order like a normal column.
    @hybrid_property
    def movie_cnt(self):
        return self.movies.count()

    # https://stackoverflow.com/questions/25836076/sqlalchemy-order-by-hybrid-property-that-references-relationship
    @movie_cnt.expression
    def movie_cnt(cls):
        return (select([func.count(movie_movie_type.c.movie_id)])
            .where(movie_movie_type.c.type_id == cls.id))