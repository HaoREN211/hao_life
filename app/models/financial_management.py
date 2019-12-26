# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:07
# IDE：PyCharm

from app import db
import datetime
from flask import flash

class HaoFinancialManagement(db.Model):
    statistic_data = db.Column(db.Date, primary_key=True, comment="统计时间")
    principal = db.Column(db.DECIMAL(10, 2), comment="所有金额")
    daily_interest = db.Column(db.DECIMAL(10, 2), comment="当日利息")
    all_interest = db.Column(db.DECIMAL(10, 2), comment="累计利息")

    # statistic_date当天是否设置了数据
    @staticmethod
    def has_set_data(statistic_date):
        list_result = HaoFinancialManagement.query.filter_by(statistic_data=statistic_date).all()
        return len(list_result) > 0

    # 获取statistic_date前一天
    @staticmethod
    def get_previous_day(statistic_date):
        return statistic_date + datetime.timedelta(days=-1)

    # statistic_date前一天是否设置了数据
    @staticmethod
    def has_set_previous_day_data(statistic_date):
        previous_day = HaoFinancialManagement.get_previous_day(statistic_date)
        return HaoFinancialManagement.has_set_data(previous_day)

    # 获取statistic_date当天的数据
    @staticmethod
    def get_today_data(statistic_date):
        today_interest = HaoFinancialManagement.query.filter_by(statistic_data=statistic_date).first()
        return today_interest.principal, today_interest.daily_interest, today_interest.all_interest

    # 获取statistic_date前一天的数据
    @staticmethod
    def get_previous_day_data(statistic_date):
        previous_day = HaoFinancialManagement.get_previous_day(statistic_date)
        return HaoFinancialManagement.get_today_data(previous_day)

    # 将statistic_date当天的数据添加入数据库
    @staticmethod
    def add_new_record(statistic_data, daily_interest):
        db_principal, _, db_all_interest = HaoFinancialManagement.get_previous_day_data(statistic_data)
        db_principal += daily_interest
        db_all_interest += daily_interest
        new_record = HaoFinancialManagement(
            statistic_data=statistic_data,
            principal=db_principal,
            daily_interest=daily_interest,
            all_interest=db_all_interest
        )
        db.session.add(new_record)
        db.session.commit()
        flash(str(statistic_data)+"的数据添加成功，累计本金:"+str(db_principal)+"，当日利息:"+str(daily_interest)+"，累计利息:"+str(db_all_interest))
        return True