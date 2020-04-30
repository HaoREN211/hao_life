# @Time    : 2020/1/10 20:24
# @Author  : REN Hao
# @FileName: salary.py
# @Software: PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from config import CURRENT_WORK_EXPERIENCE_ID


class Position(db.Model):
    __table_args__ = {'comment': '岗位信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="岗位主键")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="岗位名字")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")


class WorkExperience(db.Model):
    __table_args__ = {'comment': '工作经验信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="工作经历主键")
    employee_no = db.Column(db.String(20), comment="员工号")
    enterprise_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("enterprise.id"), nullable=False, comment="公司主键")
    position_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("position.id"), nullable=False, comment="岗位主键")

    start_date = db.Column(db.Date, nullable=False, comment="开始时间")
    end_date = db.Column(db.Date, nullable=True, comment="结束时间")

    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")

    enterprise = db.relation("Enterprise", backref="work_experiences", foreign_keys=[enterprise_id])
    position = db.relation("Position", backref="work_experiences", foreign_keys=[position_id])

    @hybrid_property
    def salary_cnt(self):
        return len(self.salaries)


class Salary(db.Model):
    __table_args__ = {'comment': '工资信息'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="工资主键")
    date = db.Column(db.DateTime, nullable=False, comment="领工资时间")
    work_experience_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("work_experience.id"),
                                   nullable=False, comment="工作经历主键", default=CURRENT_WORK_EXPERIENCE_ID)
    basic_salary = db.Column(db.DECIMAL(10, 2), nullable=False, comment="基本工资")
    personal_endowment = db.Column(db.DECIMAL(10, 2), nullable=False, comment="个人养老保险")
    personal_medical = db.Column(db.DECIMAL(10, 2), nullable=False, comment="个人医疗保险")
    personal_unemployment = db.Column(db.DECIMAL(10, 2), nullable=False, comment="个人失业保险保险")
    personal_provident_fund = db.Column(db.DECIMAL(10, 2), nullable=False, comment="个人公积金部分")
    personal_tax = db.Column(db.DECIMAL(10, 2), nullable=False, comment="个人所得税")
    personal_total = db.Column(db.DECIMAL(10, 2), nullable=True, comment="个人所得税")
    salary_after_tax = db.Column(db.DECIMAL(10, 2), nullable=True, comment="税后薪资")
    enterprise_endowment = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳养老保险")
    enterprise_medical = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳医疗保险")
    enterprise_supplementary_medical = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳补充医疗保险")
    enterprise_maternity = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳生育保险")
    enterprise_occupational = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳工伤保险")
    enterprise_unemployment = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳失业保险")
    enterprise_provident_fund = db.Column(db.DECIMAL(10, 2), nullable=False, comment="公司缴纳公积金")
    enterprise_total = db.Column(db.DECIMAL(10, 2), nullable=True, comment="公司缴纳总和")

    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="修改时间")

    db.UniqueConstraint('date', 'work_experience_id', name='salary_date_work_experience_unique')

    work_experience = db.relation("WorkExperience", backref="salaries", foreign_keys=[work_experience_id])

    def update_info(self):
        self.update_personal_total()
        self.update_enterprise_total()
        self.update_salary_after_tax()

    # 更新个人所交总和
    def update_personal_total(self):
        self.personal_total = (self.personal_endowment + self.personal_medical + self.personal_unemployment +
                               self.personal_provident_fund + self.personal_tax)

    # 更新税后工资
    def update_salary_after_tax(self):
        self.salary_after_tax = (self.basic_salary - self.personal_total)

    # 更新企业所交总和
    def update_enterprise_total(self):
        self.enterprise_total = (
                self.enterprise_endowment + self.enterprise_medical + self.enterprise_supplementary_medical +
                self.enterprise_maternity + self.enterprise_occupational + self.enterprise_unemployment +
                self.enterprise_provident_fund)
