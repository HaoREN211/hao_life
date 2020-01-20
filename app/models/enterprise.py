# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/9 9:55
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.hybrid import hybrid_property

class Enterprise(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="企业主键")
    name = db.Column(db.String(100), unique=True, nullable=True, comment="企业名称")
    short_name = db.Column(db.String(100), unique=True, nullable=True, comment="企业简称")
    founded_time = db.Column(db.Date, nullable=False, comment="创立时间")
    president_id = db.Column("person_id", BIGINT(unsigned=True), db.ForeignKey("person.id"), nullable=True, comment="总裁主键")
    headquarter_id = db.Column("district_id", BIGINT(unsigned=True), db.ForeignKey("district.id"), nullable=True, comment="总部主键")
    rank_2019 = db.Column("rank_2019", INTEGER(unsigned=True), unique=True, nullable=True, comment="公司2019排名")

    president = db.relationship("Person", backref="enterprises", foreign_keys=[president_id])
    headquarter = db.relationship("District", backref="enterprises", foreign_keys=[headquarter_id])

    @hybrid_property
    def work_experience_cnt(self):
        return len(self.work_experiences)

    @hybrid_property
    def salary_cnt(self):
        list_salary_cnt_of_work_experience = [x.salary_cnt for x in self.work_experiences]
        if list_salary_cnt_of_work_experience:
            return sum(list_salary_cnt_of_work_experience)
        return 0

    @hybrid_property
    def estate_cnt(self):
        return len(self.estates)

    @hybrid_property
    def building_cnt(self):
        list_building_cnt_of_estate = [x.building_cnt for x in self.estates]
        if list_building_cnt_of_estate:
            return sum(list_building_cnt_of_estate)
        return 0