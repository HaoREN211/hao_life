# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:18
# IDE：PyCharm

from flask import render_template, redirect, url_for, flash
from app.management import bp
from app import db
from app.management.forms.financial_management import HaoFinancialManagementForm
from app.models.financial_management import HaoFinancialManagement
import datetime


@bp.route('/financial_management', methods=['GET', 'POST'])
def financial_management():
    return "666"


@bp.route('/financial_management/add', methods=['GET', 'POST'])
def financial_management_add():
    form = HaoFinancialManagementForm()
    if form.validate_on_submit():
        statistic_data = form.statistic_data.data
        daily_interest = form.daily_interest.data
        # statistic_date当天是否设置了数据
        if HaoFinancialManagement.has_set_data(statistic_data):
            _, daily_interest, _ = HaoFinancialManagement.get_today_data(statistic_data)
            flash(str(statistic_data)+"这天已经设置了利息"+str(daily_interest)+"，请重新设置")
            return render_template('financial_management/add.html', form=form)
        # statistic_date前一天是否设置了数据
        if not HaoFinancialManagement.has_set_previous_day_data(statistic_data):
            previous_day = statistic_data - datetime.timedelta(days=1)
            flash(str(statistic_data) + "前一天"+str(previous_day)+"还未设置了金额，请重新设置")
            return render_template('financial_management/add.html', form=form)
        # 新增数据
        HaoFinancialManagement.add_new_record(statistic_data, daily_interest)
        return redirect(url_for('management.financial_management_add'))
    return render_template('financial_management/add.html', form=form)