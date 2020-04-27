# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/27 8:51
# IDE：PyCharm


from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app.management.forms.pattern import DateForm
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.life.character import WeightCreateForm, WeightModifyForm, Weight
from math import floor
import datetime as dt
from operator import and_
from app.management.forms.financial_management import HaoFinancialManagementDate

# 体重
@bp.route('/weights', methods=['GET', 'POST'])
def weights():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)

    e_chart_line = e_chart_weight(start_date, end_date)

    start_date_form = DateForm()
    start_date_form.date.data = min(e_chart_line.date) if ((start_date is None) or (start_date=="")) else start_date
    end_date_form = DateForm()
    end_date_form.date.data = max(e_chart_line.date) if ((end_date is None) or (end_date=="")) else end_date

    items = Weight.query.order_by(Weight.date.desc()).paginate(page, 10, False)

    add_form = WeightCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = WeightModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, Weight(), "management.weights")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Weight, "management.weights", has_update=True)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Weight.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.weights"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.weights"))
    modify_form = modify_form_constructor(items, "WeightModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.weights', page=items.next_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_next else None
    prev_url = url_for('management.weights', page=items.prev_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_prev else None
    curr_url = url_for('management.weights', page=page)

    return render_template("life/weights.html", items=items.items,
                           next_url=next_url, prev_url=prev_url, curr_url=curr_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form,
                           start_date_form=start_date_form, end_date_form=end_date_form,
                           e_chart_line=e_chart_line, e_chart_calendar_weight=e_chart_calendar_weight())

# 日历图所需数据
def e_chart_calendar_weight():
    date_now = dt.datetime.now().date()
    year = str(date_now.year)
    month = str(date_now).split("-")[1]
    first_day = dt.datetime.strptime(year+"-"+month+"-"+"01", "%Y-%m-%d").date()
    last_day = first_day+dt.timedelta(days=31)

    list_weights= [str(x[0]).split(" ")[0] for x in db.session.query(Weight.date).filter(and_(
        Weight.date>=first_day, Weight.date<=last_day)).all()]

    list_result = []
    for i in range(31):
        current_date = first_day+dt.timedelta(days=i)
        if int(month)!=current_date.month:
            break
        current_result = [str(current_date), str(1) if str(current_date) in list_weights else ""]
        list_result.append(current_result)
    return {"range": year + "-" + month, "data":list_result}

# 生成e_chart体重折线图的必须数据
def e_chart_weight(start_date=None, end_date=None):
    date_start_date = "1900-01-01" if ((start_date is None) or (start_date=="")) else dt.datetime.strptime(start_date, "%Y-%m-%d")
    date_end_date = dt.datetime.now().date() if ((end_date is None) or (end_date == "")) else dt.datetime.strptime(end_date, "%Y-%m-%d")
    datas = Weight.query.filter(and_(
        Weight.date>=date_start_date,
        Weight.date<=date_end_date
    )).order_by(Weight.date).all()
    list_date, list_data = list([]), list([])
    for date in datas:
        list_date.append(date.date)
        list_data.append(date.weight)
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

