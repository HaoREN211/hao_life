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
from app.management.e_echart import e_chart_line, e_chart_calendar, data_form_generator


# 体重
@bp.route('/weights', methods=['GET', 'POST'])
def weights():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)

    e_chart_line_weight = e_chart_weight(start_date, end_date)
    start_date_form, end_date_form = data_form_generator(e_chart_line_weight, start_date, end_date)

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
                           e_chart_line=e_chart_line_weight, e_chart_calendar_weight=e_chart_calendar_weight())

# 日历图所需数据
def e_chart_calendar_weight():
    return e_chart_calendar("weight")

# 生成e_chart体重折线图的必须数据
def e_chart_weight(start_date=None, end_date=None):
    return e_chart_line("weight", start_date, end_date)

