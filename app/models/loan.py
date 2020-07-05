# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/9 15:36
# IDE：PyCharm

from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT

class HouseLoanPlan(db.Model):
    __table_args__ = {'comment': '房贷总览表'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房贷总览主键")

    start_date = db.Column(db.Date, nullable=False, comment="开始还款日")
    end_date = db.Column(db.Date, nullable=True, comment="还款结束日")

    duration = db.Column(db.Integer, nullable=False, comment="还款年限(年)")

    amount_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="还款总金额")

    amount_commercial_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="商贷总金额")
    amount_fund_total = db.Column(db.DECIMAL(12, 2), nullable=True, comment="公积金贷款总金额")
    amount_principal_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="本金总金额")
    amount_tax_total = db.Column(db.DECIMAL(12, 2), nullable=True, comment="利息总金额")

    amount_commercial_principal = db.Column(db.DECIMAL(12, 2), nullable=False, comment="商贷本金")
    amount_commercial_tax = db.Column(db.DECIMAL(12, 2), nullable=False, comment="商贷利息")
    amount_fund_principal = db.Column(db.DECIMAL(12, 2), nullable=False, comment="公积金本金")
    amount_fund_tax = db.Column(db.DECIMAL(12, 2), nullable=False, comment="公积金利息")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    def update_amount_commercial_principal(self):
        self.updates_all()
    def update_amount_commercial_tax(self):
        self.updates_all()
    def update_amount_fund_principal(self):
        self.updates_all()
    def update_amount_fund_tax(self):
        self.updates_all()

    def updates_all(self):
        self.amount_tax_total = self.amount_commercial_tax + self.amount_fund_tax
        self.amount_principal_total = self.amount_commercial_principal+self.amount_fund_principal
        self.amount_commercial_total = self.amount_commercial_principal+self.amount_commercial_tax
        self.amount_fund_total = self.amount_fund_principal+self.amount_fund_tax
        self.amount_total = self.amount_commercial_total + self.amount_fund_total


class HouseLoanDetail(db.Model):
    __table_args__ = {'comment': '房贷明细表'}
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="房贷明细主键")
    plain_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("house_loan_plan.id"), comment="房贷计划主键")

    term = db.Column(db.Integer, nullable=False, comment="当前期数")
    date = db.Column(db.Date, nullable=False, comment="还款日")
    commercial_time = db.Column(db.DateTime, nullable=False, comment="商贷还款时间")
    fund_time = db.Column(db.DateTime, nullable=False, comment="公积金还款时间")

    amount_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="还款总金额")

    amount_commercial_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="商贷总金额")
    amount_fund_total = db.Column(db.DECIMAL(12, 2), nullable=True, comment="公积金贷款总金额")
    amount_principal_total = db.Column(db.DECIMAL(12,2), nullable=True, comment="本金总金额")
    amount_tax_total = db.Column(db.DECIMAL(12, 2), nullable=True, comment="利息总金额")

    amount_commercial_principal = db.Column(db.DECIMAL(12, 2), nullable=False, comment="商贷本金")
    amount_commercial_tax = db.Column(db.DECIMAL(12, 2), nullable=False, comment="商贷利息")
    amount_fund_principal = db.Column(db.DECIMAL(12, 2), nullable=False, comment="公积金本金")
    amount_fund_tax = db.Column(db.DECIMAL(12, 2), nullable=False, comment="公积金利息")

    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="最后一次修改时间")

    def update_amount_commercial_principal(self):
        self.updates_all()
    def update_amount_commercial_tax(self):
        self.updates_all()
    def update_amount_fund_principal(self):
        self.updates_all()
    def update_amount_fund_tax(self):
        self.updates_all()

    def updates_all(self):
        self.amount_tax_total = self.amount_commercial_tax + self.amount_fund_tax
        self.amount_principal_total = self.amount_commercial_principal+self.amount_fund_principal
        self.amount_commercial_total = self.amount_commercial_principal+self.amount_commercial_tax
        self.amount_fund_total = self.amount_fund_principal+self.amount_fund_tax
        self.amount_total = self.amount_commercial_total + self.amount_fund_total