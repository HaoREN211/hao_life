# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/10/21 18:20
# IDE：PyCharm

from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT

class Account(db.Model):
    __table_args__ = {'comment': '账号列表'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="账号主键")
    name = db.Column(db.String(50), unique=True, nullable=False, comment="名称")
    account = db.Column(db.String(30), unique=False, nullable=False, comment="账号")
    password = db.Column(db.String(30), unique=False, nullable=True, comment="密码")
    url = db.Column(db.String(500), unique=False, nullable=True, comment="链接")
    comment = db.Column(db.String(100), unique=False, nullable=True, comment="注释")

    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="用户主键")
    user = db.relationship("User", backref="accounts", foreign_keys=[user_id])

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")