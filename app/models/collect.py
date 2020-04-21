# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/21 16:01
# IDE：PyCharm

# 链接收藏

from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from sqlalchemy.sql import func

class Collect(db.Model):
    __table_args__ = {'comment': '链接收藏'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="链接收藏主键")
    name = db.Column(db.String(100), unique=False, nullable=False, comment="链接收藏名称")
    link = db.Column(db.String(200), unique=True, nullable=False, comment="链接收藏地址")

    web_site_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("web_site.id"), nullable=True, comment="网站主键")
    web_site = db.relationship("WebSite", backref="collects", foreign_keys=[web_site_id])

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    # 每次link更新的时候执行的操作
    def upgrade_link(self):
        print(self.link)

class WebSite(db.Model):
    __table_args__ = {'comment': '网址地址'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="网站主键")
    name = db.Column(db.String(100), unique=False, nullable=True, comment="网站名称")
    link = db.Column(db.String(200), unique=True, nullable=False, comment="网站地址")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    @hybrid_property
    def collect_cnt(self):
        return len(self.collects)

    @collect_cnt.expression
    def collect_cnt(cls):
        return (select([func.count(Collect.id)])
                .where(Collect.web_site_id == cls.id))
