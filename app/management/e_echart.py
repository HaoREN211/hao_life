# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/30 13:44
# IDE：PyCharm

import datetime as dt
from operator import and_
from app.management.forms.financial_management import HaoFinancialManagementDate
from math import floor
from app.models.clock_in import ClockIn
from app.management.forms.life.character import Weight
from app import db
from app.management.forms.pattern import DateForm
from app.models.consume import Consume


# 根据data里面的时间列表，生成最早时间和最晚时间的表单
def data_form_generator(data, start_date, end_date):
    start_date_form = DateForm()
    start_date_form.date.data = min(data.date) if (
        (start_date is None) or (start_date == "")) else start_date
    end_date_form = DateForm()
    end_date_form.date.data = max(data.date) if (
        (end_date is None) or (end_date == "")) else end_date
    return start_date_form, end_date_form


# 生成e_chart折线图的必须数据
def e_chart_line(model, start_date=None, end_date=None):
    date_start_date = "1900-01-01" if ((start_date is None) or (start_date=="")) else dt.datetime.strptime(start_date, "%Y-%m-%d")
    date_end_date = dt.datetime.now().date() if ((end_date is None) or (end_date == "")) else dt.datetime.strptime(end_date, "%Y-%m-%d")
    datas = []
    attribute = ""
    attribute_time = ""

    if model == "clock_in":
        datas = ClockIn.query.filter(and_(
            ClockIn.date>=date_start_date,
            ClockIn.date<=date_end_date
        )).order_by(ClockIn.date).all()
        attribute = "duration"
        attribute_time = "date"
    elif model == "weight":
        datas = Weight.query.filter(and_(
            Weight.date >= date_start_date,
            Weight.date <= date_end_date
        )).order_by(Weight.date).all()
        attribute = "weight"
        attribute_time = "date"
    elif model == "consume":
        datas = Consume.query.filter(and_(
            Consume.time >= date_start_date,
            Consume.time <= date_end_date
        )).order_by(Consume.time).all()
        attribute = "amount"
        attribute_time = "time"

    list_date, list_data = list([]), list([])
    for date in datas:
        list_date.append(date.__getattribute__(attribute_time))
        list_data.append(date.__getattribute__(attribute))
    list_data = [float(x) for x in list_data]
    list_date = [x.strftime("%Y-%m-%d") for x in list_date]
    data_max = max(list_data) if len(list_data) > 0 else 0
    data_min = min(list_data) if len(list_data) > 0 else 0
    interval = int(floor(float(data_max - data_min) / float(5)) + 1)
    return HaoFinancialManagementDate(
        date=list_date,
        data=list_data,
        data_max=data_max,
        data_min=data_min,
        interval=interval
    )

# 日历图所需数据
def e_chart_calendar(model):
    date_now = dt.datetime.now().date()
    year = str(date_now.year)
    month = str(date_now).split("-")[1]
    first_day = dt.datetime.strptime(year+"-"+month+"-"+"01", "%Y-%m-%d").date()
    last_day = first_day+dt.timedelta(days=31)
    list_data = []

    if model == "clock_in":
        list_data = [str(x[0]).split(" ")[0] for x in db.session.query(ClockIn.date).filter(and_(
            ClockIn.date>=first_day, ClockIn.date<=last_day)).all()]
    elif model == "weight":
        list_data = [str(x[0]).split(" ")[0] for x in db.session.query(Weight.date).filter(and_(
            Weight.date >= first_day, Weight.date <= last_day)).all()]

    list_result = []
    for i in range(31):
        current_date = first_day+dt.timedelta(days=i)
        if int(month)!=current_date.month:
            break
        current_result = [str(current_date), str(1) if str(current_date) in list_data else ""]
        list_result.append(current_result)
    return {"range": year + "-" + month, "data":list_result}


