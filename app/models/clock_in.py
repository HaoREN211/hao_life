# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/28 15:35
# IDE：PyCharm

from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT
from config import CURRENT_WORK_EXPERIENCE_ID

class ClockIn(db.Model):
    __table_args__ = {'comment': '签到时间信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="签到时间主键")

    date = db.Column(db.Date, unique=True, nullable=False, comment="日期")

    clock_in_time = db.Column(db.DateTime, nullable=False, comment="签到时间")
    clock_out_time = db.Column(db.DateTime, nullable=False, comment="签退时间")

    duration = db.Column(db.DECIMAL(3,1), nullable=True, comment="持续时间")
    work_experience_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_experience.id"), nullable=False,
                                   comment="经历主键", default=CURRENT_WORK_EXPERIENCE_ID)

    work_experience = db.relationship("WorkExperience", backref="clock_ins", foreign_keys=[work_experience_id])

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")


    # 根据签到时间和签退时间计算今天的工时
    def update_duration(self):
        tmp_clock_out_time = self.clock_out_time if isinstance(self.clock_out_time, datetime) else datetime.strptime(self.clock_out_time, "%Y-%m-%dT%H:%M")
        tmp_clock_in_time = self.clock_in_time if isinstance(self.clock_in_time, datetime) else datetime.strptime(self.clock_in_time, "%Y-%m-%dT%H:%M")
        duration_time = tmp_clock_out_time - tmp_clock_in_time
        self.duration = int(duration_time.seconds/3600) + (int(duration_time.seconds / 60 % 60)*1.0/60.0)
