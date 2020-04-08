# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/8 17:43
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select
from  sqlalchemy.sql import func

# 工作日志
class WorkDiary(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记主键", autoincrement=True)
    date = db.Column(db.Date, nullable=False, comment="日期")
    work_experience_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_experience.id"), nullable=False,
                                   comment="经历主键", default=2)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def details_cnt(self):
        return len(self.details)

    @details_cnt.expression
    def details_cnt(cls):
        return (select([func.count(WordDiaryDetail.id)])
                .where(WordDiaryDetail.work_diary_id == cls.id))


class WordDiaryDetail(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记详细主键", autoincrement=True)
    title = db.Column(db.String, nullable=True, comment="摘要")
    content = db.Column(db.Text(16777216), nullable=True, comment="日记内容")
    work_diary_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_diary.id"), nullable=False, comment="日记主键")

    work_diary = db.relationship("WorkDiary", backref="details", foreign_keys=[work_diary_id])
