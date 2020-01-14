# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/13 17:45
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT

class Marathon(db.Model):
    __table_args__ = {'comment': '马拉松信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房产主键")
    name = db.Column(db.String(100), nullable=False, comment="马拉松名称")

    distance = db.Column(db.DECIMAL(8, 2), nullable=True, comment="距离")
    address = db.Column(db.String(100), nullable=True, comment="门牌号码")
    district_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("district.id"), nullable=True,
                            comment="区域所在")
    plate_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("consume_plate.id"),
                         nullable=True, comment="报名平台")

    apply_start_time = db.Column(db.DateTime, nullable=True, comment="报名开始时间")
    apply_end_time = db.Column(db.DateTime, nullable=True, comment="报名结束时间")
    match_start_time = db.Column(db.DateTime, nullable=True, comment="比赛开始时间")
    match_end_time = db.Column(db.DateTime, nullable=True, comment="比赛结束时间")

    is_finished = db.Column(db.Boolean, nullable=True, comment="是否完赛")
