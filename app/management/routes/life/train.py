# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/23 20:32
# IDE：PyCharm

from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user
from datetime import datetime
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.life.train import TrainCreateForm, TrainModifyForm, TrainNumberCreateForm, TrainNumberModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.train import Train, TrainNumber
from sqlalchemy.sql import desc


# 火车列表
@bp.route('/trains', methods=['GET', 'POST'])
def trains():
    page = request.args.get('page', 1, type=int)
    items = Train.query.order_by(Train.time_from.desc()).paginate(page, 10, False)

    add_form = TrainCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = TrainModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, Train(), "management.trains")
                    current_train = Train.query.order_by(Train.id.desc()).first()
                    current_train.create_user_id = current_user.id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Train, 'management.trains')
                    current_train = Train.query.get(int(temp_modify_form.id.data))
                    current_train.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Train.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.trains"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.trains"))
    modify_form = modify_form_constructor(items, "TrainModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.trains', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.trains', page=items.prev_num) if items.has_prev else None

    return render_template("life/trains.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


@bp.route('/train_numbers', methods=['GET', 'POST'])
def train_numbers():
    page = request.args.get('page', 1, type=int)
    items = TrainNumber.query.order_by(desc(TrainNumber.train_cnt)).paginate(page, 10, False)

    add_form = TrainNumberCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = TrainNumberModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, TrainNumber(), "management.train_numbers")
                    current_train_number = TrainNumber.query.filter_by(name=str(add_form.name.data).strip()).first()
                    current_train_number.create_user_id = current_user.id
                    current_train_number.create_time = datetime.now()
                    current_train_number.update_time = datetime.now()
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, TrainNumber, 'management.train_numbers')
                    current_train_number = TrainNumber.query.get(int(temp_modify_form.id.data))
                    current_train_number.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = TrainNumber.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.train_numbers"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.train_numbers"))
    modify_form = modify_form_constructor(items, "TrainNumberModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.train_numbers', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.train_numbers', page=items.prev_num) if items.has_prev else None

    return render_template("life/train_numbers.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)
