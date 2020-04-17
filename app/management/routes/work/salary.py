# @Time    : 2020/1/10 20:43
# @Author  : REN Hao
# @FileName: salary.py
# @Software: PyCharm

from operator import and_
from datetime import datetime as dt
from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app.management.forms.pattern import DateForm
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.forms.work.salary import SalaryCreateForm, SalaryModifyForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.salary import Salary
from app.management.forms.financial_management import HaoFinancialManagementDate
from math import floor


@bp.route('/salaries', methods=['GET', 'POST'])
def salaries():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)
    items = Salary.query.order_by(Salary.date.desc()).paginate(page, 10, False)

    add_form = SalaryCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = SalaryModifyForm()

    echarts_data = e_chart_salary(start_date, end_date)

    # e_chart折线图的默认开始时间和终止时间
    start_date_form = DateForm()
    end_date_form = DateForm()
    start_date_form.date.data = start_date if start_date is not None else min(echarts_data.date)
    end_date_form.date.data = end_date if end_date is not None else max(echarts_data.date)

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    info_add = create_db_row(add_form, Salary(), "management.salaries")
                    current_row = Salary.query.filter(
                        and_(Salary.work_experience_id == int(add_form.work_experience_id.data),
                             Salary.date == add_form.date.data)
                    ).first()
                    current_row.update_info()
                    return info_add
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Salary, 'management.salaries')
                    current_row = Salary.query.filter(
                        and_(Salary.work_experience_id == int(temp_modify_form.work_experience_id.data),
                             Salary.date == temp_modify_form.date.data)
                    ).first()
                    current_row.update_info()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Salary.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.salaries"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.salaries"))
    modify_form = modify_form_constructor(items, "SalaryModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.salaries', page=items.next_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_next else None
    prev_url = url_for('management.salaries', page=items.prev_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_prev else None
    curr_url = url_for('management.salaries', page=page)

    return render_template("work/salary.html", items=items.items,
                           next_url=next_url, prev_url=prev_url, curr_url=curr_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form,
                           start_date_form=start_date_form, end_date_form=end_date_form,
                           e_chart_salary=echarts_data)

def e_chart_salary(start_date=None, end_date=None):
    if (start_date is None) and (end_date is None):
        salaries = Salary.query.order_by(Salary.date).all()
    elif end_date is None:
        salaries = Salary.query.filter(Salary.date>=dt.strptime(start_date, "%Y-%m-%d")).order_by(Salary.date).all()
    elif start_date is None:
        salaries = Salary.query.filter(Salary.date <= dt.strptime(end_date, "%Y-%m-%d")).order_by(Salary.date).all()
    else:
        salaries = Salary.query.filter(and_(
            Salary.date>=dt.strptime(start_date, "%Y-%m-%d"),
            Salary.date<=dt.strptime(end_date, "%Y-%m-%d")
        )).order_by(Salary.date).all()
    list_date, list_data = list([]), list([])
    for salary in salaries:
        list_date.append(salary.date)
        list_data.append(salary.salary_after_tax)
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
