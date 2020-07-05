# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/27 8:47
# IDE：PyCharm


from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT

class Weight(db.Model):
    __table_args__ = {'comment': '体重记录'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="体重主键")
    date = db.Column(db.Date, unique=True, nullable=False, comment="上称日期")
    weight = db.Column(db.DECIMAL(3,1), nullable=False, comment="体重")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")