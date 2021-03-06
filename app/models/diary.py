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
from config import CURRENT_WORK_EXPERIENCE_ID

# 工作日志
class WorkDiary(db.Model):
    __table_args__ = (db.UniqueConstraint("work_experience_id", "date", name="work_diary_date_unique"),)
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记主键", autoincrement=True)
    date = db.Column(db.Date, nullable=False, comment="日期")
    work_experience_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_experience.id"), nullable=False,
                                   comment="经历主键", default=CURRENT_WORK_EXPERIENCE_ID)
    work_experience = db.relationship("WorkExperience", backref="details", foreign_keys=[work_experience_id])
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

    @hybrid_property
    def details_cnt(self):
        return len(self.details)

    @details_cnt.expression
    def details_cnt(cls):
        return (select([func.count(WorkDiaryDetail.id)])
                .where(WorkDiaryDetail.work_diary_id == cls.id))

class WorkProjectType(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记项目类型主键", autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment="项目类型名称")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    @hybrid_property
    def projects_cnt(self):
        return len(self.projects)

    @projects_cnt.expression
    def projects_cnt(cls):
        return (select([func.count(WorkProject.id)])
                .where(WorkProject.project_type_id == cls.id))

class WorkProject(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记项目主键", autoincrement=True)
    project_type_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_project_type.id"), nullable=True, comment="项目分类")
    name = db.Column(db.String(50), nullable=False, comment="项目名称")
    start_date = db.Column(db.Date, nullable=True, comment="项目开始时间")
    end_date = db.Column(db.Date, nullable=True, comment="项目结束时间")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")
    project_type = db.relationship("WorkProjectType", backref="projects", foreign_keys=[project_type_id])

    @hybrid_property
    def details_cnt(self):
        return len(self.details)

    @details_cnt.expression
    def details_cnt(cls):
        return (select([func.count(WorkDiaryDetail.id)])
                .where(WorkDiaryDetail.work_diary_id == cls.id))


class WorkDiaryDetail(db.Model):
    __table_args__ = (db.UniqueConstraint("work_diary_id", "order", name="work_diary_order_unique"),)
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="日记详细主键", autoincrement=True)
    order = db.Column(db.Integer, nullable=False, comment="当日顺序")
    content = db.Column(db.Text(16777216), nullable=True, comment="日记内容")
    work_diary_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_diary.id"), nullable=False, comment="日记主键")
    work_project_id =  db.Column(BIGINT(unsigned=True), db.ForeignKey("work_project.id"), nullable=False, comment="日记主键")

    work_diary = db.relationship("WorkDiary", backref="details", foreign_keys=[work_diary_id])
    work_project = db.relationship("WorkProject", backref="details", foreign_keys=[work_project_id])

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    # 根据项目关联的最新和最老的日记创建时间更新项目的结束和开始的日期
    def update_project_time(self):
        project_details_times = [x.create_time.date() for x in self.work_project.details]
        self.work_project.start_date = min(project_details_times)
        self.work_project.end_date = max(project_details_times)

