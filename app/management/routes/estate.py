# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 11:15
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app import db
from app.management import bp
from app.management.forms.estate import (EstateCreateForm, EstateModifyForm, BuildingTypeCreateForm,
                                         BuildingTypeModifyForm, BuildingPropertyCreateForm, BuildingPropertyModifyForm,
                                         BuildingCreateForm, BuildingModifyForm)
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.movie import flash_form_errors
from app.models.estate import Estate, BuildingType, BuildingProperty, Building
from app.management.forms import modify_form_constructor, modify_db, create_db_row


# 小区列表
@bp.route('/estates', methods=['GET', 'POST'])
def estates():
    page = request.args.get('page', 1, type=int)
    items = Estate.query.order_by().paginate(page, 10, False)

    add_form = EstateCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = EstateModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, Estate(), "management.estates")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Estate, 'management.estates')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Estate.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.estates"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.estates"))
    modify_form = modify_form_constructor(items, "EstateModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.estates', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.estates', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/estate.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)

# 户型列表
@bp.route('/building_types', methods=['GET', 'POST'])
def building_types():
    page = request.args.get('page', 1, type=int)
    items = BuildingType.query.order_by().paginate(page, 10, False)

    add_form = BuildingTypeCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = BuildingTypeModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, BuildingType(), "management.building_types")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, BuildingType, "management.building_types")
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = BuildingType.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.building_types"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.building_types"))
    modify_form = modify_form_constructor(items, "BuildingTypeModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.building_types', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.building_types', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/building_type.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


# 小区列表
@bp.route('/building_properties', methods=['GET', 'POST'])
def building_properties():
    page = request.args.get('page', 1, type=int)
    items = BuildingProperty.query.order_by().paginate(page, 10, False)

    add_form = BuildingPropertyCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = BuildingPropertyModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, BuildingProperty(), "management.building_properties")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, BuildingProperty, 'management.building_properties')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = BuildingProperty.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.building_properties"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.building_properties"))
    modify_form = modify_form_constructor(items, "BuildingPropertyModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.building_properties', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.building_properties', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/building_property.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


# 房源列表
@bp.route('/buildings', methods=['GET', 'POST'])
def buildings():
    page = request.args.get('page', 1, type=int)
    items = Building.query.order_by().paginate(page, 10, False)

    add_form = BuildingCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = BuildingModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, Building(), "management.buildings")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Building, 'management.buildings')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Building.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.buildings"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.buildings"))
    modify_form = modify_form_constructor(items, "BuildingModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.buildings', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.buildings', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/building.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)