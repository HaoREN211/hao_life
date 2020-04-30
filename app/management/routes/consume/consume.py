# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 10:50
# IDE：PyCharm

from datetime import datetime

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms.consume import ConsumeCreateForm, ConsumeModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.consume import Consume
from app.tools import reform_datetime_local_with_datetime
from app.management.e_echart import e_chart_line, data_form_generator

# 消费列表
@bp.route('/consumes', methods=['GET', 'POST'])
def consumes():
    add_form = ConsumeCreateForm()
    temp_modify_form = ConsumeModifyForm()
    delete_form = MovieDeleteForm()

    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)

    e_chart_line_consume_data = e_chart_line_consume(start_date, end_date)
    start_date_form, end_date_form = data_form_generator(e_chart_line_consume_data, start_date, end_date)
    list_consumes = Consume.query.order_by(Consume.time.desc()).paginate(page, 10, False)

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.consume_create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return add_consume(add_form)
            if temp_modify_form.consume_modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_consume(temp_modify_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Consume.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.consumes"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.consumes"))

    modify_form = modify_form_constructor(list_consumes)

    next_url = url_for('management.consumes', page=list_consumes.next_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if list_consumes.has_next else None
    prev_url = url_for('management.consumes', page=list_consumes.prev_num, start_date=start_date_form.date.data, end_date=end_date_form.date.data) if list_consumes.has_prev else None
    curr_url = url_for('management.consumes', page=page)

    return render_template("financial_management/consume/consume.html", items = list_consumes.items,
                            next_url=next_url, prev_url=prev_url, curr_url=curr_url,
                           e_chart_line_consume = e_chart_line_consume_data,
                           start_date_form=start_date_form, end_date_form=end_date_form,
                           add_form=add_form, modify_form=modify_form, delete_form=delete_form)


def e_chart_line_consume(start_date=None, end_date=None):
    return e_chart_line("consume", start_date, end_date)


# 添加消费
def add_consume(add_form):
    to_add = Consume(
        time=add_form.time.data,
        amount=add_form.amount.data,
        user_id=current_user.id
    )

    if int(add_form.plate_id.data) > 0:
        to_add.plate_id = int(add_form.plate_id.data)
    if int(add_form.type_id.data) > 0:
        to_add.type_id = int(add_form.type_id.data)
    if int(add_form.way_id.data) > 0:
        to_add.way_id = int(add_form.way_id.data)
    if int(add_form.shop_id.data) > 0:
        to_add.shop_id = int(add_form.shop_id.data)
    if int(add_form.description_id.data) > 0:
        to_add.description_id = int(add_form.description_id.data)
    db.session.add(to_add)
    flash("添加成功！！！")
    return redirect(url_for("management.consumes"))

# 根据新表单temp_modify_form修改消费的内容
def modify_consume(temp_modify_form):
    db_consume = Consume.query.filter_by(id=int(temp_modify_form.id.data)).first()
    is_modified = False

    consume_time = datetime.strptime(temp_modify_form.time.data, "%Y-%m-%dT%H:%M")
    if consumes != db_consume:
        is_modified = True
        db_consume.time = consume_time

    consume_plate_id = int(temp_modify_form.plate_id.data) if int(temp_modify_form.plate_id.data) > 0 else None
    if consume_plate_id != db_consume.plate_id:
        is_modified = True
        db_consume.plate_id = consume_plate_id

    consume_type_id = int(temp_modify_form.type_id.data) if int(temp_modify_form.type_id.data) > 0 else None
    if consume_type_id != db_consume.type_id:
        is_modified = True
        db_consume.type_id = consume_type_id

    consume_way_id = int(temp_modify_form.way_id.data) if int(temp_modify_form.way_id.data) > 0 else None
    if consume_way_id != db_consume.way_id:
        is_modified = True
        db_consume.way_id = consume_way_id

    consume_shop_id = int(temp_modify_form.shop_id.data) if int(temp_modify_form.shop_id.data) > 0 else None
    if consume_shop_id != db_consume.shop_id:
        is_modified = True
        db_consume.shop_id = consume_shop_id

    consume_description_id = int(temp_modify_form.description_id.data) if int(
        temp_modify_form.description_id.data) > 0 else None
    if consume_description_id != db_consume.description_id:
        is_modified = True
        db_consume.description_id = consume_description_id

    if is_modified:
        flash("修改成功！！！")
    else:
        flash("毫无任何修改")

    return redirect(url_for("management.consumes"))

# 重新构造修改的表单
def modify_form_constructor(list_consumes):
    modify_form = {}

    for current_consume in list_consumes.items:
        temp_form = ConsumeModifyForm()
        temp_form.id.data = current_consume.id
        temp_form.time.data = reform_datetime_local_with_datetime(current_consume.time)
        temp_form.amount.data = current_consume.amount
        temp_form.plate_id.data = current_consume.plate_id if current_consume.plate_id is not None else 0
        temp_form.type_id.data = current_consume.type_id if current_consume.type_id is not None else 0
        temp_form.way_id.data = current_consume.way_id if current_consume.way_id is not None else 0
        temp_form.shop_id.data = current_consume.shop_id if current_consume.shop_id is not None else 0
        temp_form.description_id.data = current_consume.description_id if current_consume.description_id is not None else 0

        modify_form[current_consume.id] = temp_form
    return modify_form

