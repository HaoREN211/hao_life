# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/29 20:15
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.work.clock_in import ClockInCreateForm, ClockInModifyForm, ClockIn
from app.management.e_echart import e_chart_line, e_chart_calendar, data_form_generator

@bp.route('/clock_ins', methods=['GET', 'POST'])
def clock_ins():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)

    items = ClockIn.query.order_by(ClockIn.date.desc()).paginate(page, 10, False)

    e_chart_line_clock_in_data = e_chart_line_clock_in(start_date, end_date)

    start_date_form, end_date_form = data_form_generator(e_chart_line_clock_in_data, start_date, end_date)

    add_form = ClockInCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = ClockInModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, ClockIn(), "management.clock_ins")
                    ClockIn.query.order_by(ClockIn.id.desc()).first().update_duration()
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, ClockIn, "management.clock_ins", has_update=True)
                    ClockIn.query.filter_by(id=int(temp_modify_form.id.data)).first().update_duration()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = ClockIn.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.clock_ins"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.clock_ins"))
    modify_form = modify_form_constructor(items, "ClockInModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.clock_ins', page=items.next_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_next else None
    prev_url = url_for('management.clock_ins', page=items.prev_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if items.has_prev else None
    curr_url = url_for('management.clock_ins', page=page)

    return render_template("work/clock_in.html", items=items.items,
                           next_url=next_url, prev_url=prev_url, curr_url=curr_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form,
                           e_chart_line = e_chart_line_clock_in_data,
                           start_date_form=start_date_form, end_date_form=end_date_form,
                           e_chart_calendar = e_chart_calendar_clock_in())

# 日历图所需数据
def e_chart_calendar_clock_in():
    return e_chart_calendar("clock_in")


# 生成e_chart体重折线图的必须数据
def e_chart_line_clock_in(start_date=None, end_date=None):
    return e_chart_line("clock_in", start_date, end_date)
