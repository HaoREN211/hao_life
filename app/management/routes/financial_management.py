# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:18
# IDE：PyCharm

from flask import render_template, redirect, url_for, flash
from app.management import bp
from app.management.forms.financial_management import HaoFinancialManagementForm, HaoFinancialManagementDate
from app.models.financial_management import HaoFinancialManagement
import datetime
from math import floor


@bp.route('/financial_management', methods=['GET', 'POST'])
def financial_management():
    echarts_data = echarts_financial_management()
    return render_template('financial_management/index.html', echarts_data=echarts_data)


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


# 画每日利息折线图时所需要的的数据
def echarts_financial_management():
    datas = HaoFinancialManagement.query.filter(HaoFinancialManagement.statistic_data>'2019-10-23').order_by(HaoFinancialManagement.statistic_data).all()
    list_date, list_data = list([]), list([])
    for current_data in datas:
        list_data.append(current_data.daily_interest)
        list_date.append(current_data.statistic_data)
    list_data = [float(x) for x in list_data]
    list_date = [x.strftime("%Y-%m-%d") for x in list_date]
    data_max = max(list_data)
    data_min = min(list_data)
    interval = floor(float(data_max-data_min)/float(5))+1

    return HaoFinancialManagementDate(
        date=list_date,
        data=list_data,
        data_max=data_max,
        data_min=data_min,
        interval=interval
    )