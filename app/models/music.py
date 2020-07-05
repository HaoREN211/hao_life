# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/20 9:59
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from sqlalchemy.sql import func

class Music(db.Model):
    __table_args__ = {'comment': '音乐信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="音乐")
    name = db.Column(db.String(100), nullable=False, comment="歌曲名")
    issue_date = db.Column(db.Date, nullable=True, comment="发行时间")

    lyrics_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("person.id"), comment="作词人")
    composer_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("person.id"), comment="作曲人")
    singer_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("person.id"), comment="演唱人")
    album_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("album.id"), comment="专辑")
    music_type_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("music_type.id"), comment="音乐类型")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="创建人")
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    singer = db.relationship("Person", backref="sing_musics", foreign_keys=[singer_id])
    type = db.relationship("MusicType", backref="musics", foreign_keys=[music_type_id])
    album = db.relationship("Album", backref="musics", foreign_keys=[album_id])


class Album(db.Model):
    __table_args__ = {'comment': '专辑信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="音乐")
    name = db.Column(db.String(100), nullable=False, comment="专辑名")
    singer_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("person.id"), comment="演唱人")
    issue_date = db.Column(db.Date, nullable=True, comment="发行时间")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="创建人")
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    singer = db.relationship("Person", backref="albums", foreign_keys=[singer_id])

    @hybrid_property
    def music_cnt(self):
        return len(self.musics)

    @music_cnt.expression
    def music_cnt(cls):
        return (select([func.count(Music.id)])
                .where(Music.album_id == cls.id))

class MusicType(db.Model):
    __table_args__ = {'comment': '音乐类型信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="音乐类型ID")
    name = db.Column(db.String(100), nullable=False, comment="音乐类型")

    create_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="创建人")
    create_time = db.Column(db.DateTime, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), comment="更新时间")

    @hybrid_property
    def music_cnt(self):
        return len(self.musics)

    @music_cnt.expression
    def music_cnt(cls):
        return (select([func.count(Music.id)])
                .where(Music.music_type_id == cls.id))