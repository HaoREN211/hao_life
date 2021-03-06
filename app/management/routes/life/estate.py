# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 11:15
# IDE：PyCharm

from os import remove
from os.path import exists

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from sqlalchemy import desc

from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row, upload_form_constructor, \
    modify_upload
from app.management.forms.estate import (EstateCreateForm, EstateModifyForm, BuildingTypeCreateForm,
                                         BuildingTypeModifyForm, BuildingPropertyCreateForm, BuildingPropertyModifyForm,
                                         BuildingCreateForm, BuildingModifyForm, BuildingOwnerCreateForm,
                                         BuildingOwnerModifyForm, DistrictTimesCreateForm, DistrictTimesModifyForm,
                                         ApartmentCreateForm, ApartmentModifyForm, ListDistrictTimes)
from app.management.forms.general.upload import FileForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.estate import Estate, BuildingType, BuildingProperty, Building, BuildingOwner, DistrictTimes, Apartment


# 小区列表
@bp.route('/estates', methods=['GET', 'POST'])
def estates():
    page = request.args.get('page', 1, type=int)
    items = Estate.query.order_by(desc(Estate.building_cnt)).paginate(page, 10, False)

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
    items = BuildingType.query.order_by(desc(BuildingType.building_cnt)).paginate(page, 10, False)

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
    items = BuildingProperty.query.order_by(desc(BuildingProperty.building_cnt)).paginate(page, 10, False)

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
    items = Building.query.order_by(Building.lottery_time.desc()).paginate(page, 10, False)

    add_form = BuildingCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = BuildingModifyForm()
    temp_upload_form = FileForm()


    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    info_create = create_db_row(add_form, Building(), "management.buildings")
                    added_building = Building.query.order_by(Building.id.desc()).first()
                    added_building.upgrade_unit_price()
                    return info_create
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    info_modify = modify_db(temp_modify_form, Building, 'management.buildings')
                    modified_building = Building.query.filter_by(id=int(temp_modify_form.id.data)).first()
                    modified_building.upgrade_unit_price()
                    return info_modify
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Building.query.filter_by(id=int(delete_form.id.data)).first()
                to_delete_file = to_delete.image
                if to_delete_file is not None and len(str(to_delete_file).strip())>0:
                    to_delete_file = "/root/hao_life/app/"+to_delete_file
                    if exists(to_delete_file):
                        remove(to_delete_file)
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.buildings"))
            if temp_upload_form.file_submit.data and temp_upload_form.validate_on_submit():
                current_file = request.files['file_select']
                saved_path = modify_upload(current_file, temp_upload_form, "building")
                current_building = Building.query.filter_by(id=int(temp_upload_form.id.data)).first()
                current_building.image = saved_path
                flash("上传成功")
                return redirect(url_for("management.buildings"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.buildings"))

    modify_form = modify_form_constructor(items, "BuildingModifyForm")
    upload_image_form = upload_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form


    next_url = url_for('management.buildings', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.buildings', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/building.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form, upload_image_form=upload_image_form)


# 小区列表
@bp.route('/building_owners', methods=['GET', 'POST'])
def building_owners():
    page = request.args.get('page', 1, type=int)
    items = BuildingOwner.query.order_by(desc(BuildingOwner.building_cnt)).paginate(page, 10, False)

    add_form = BuildingOwnerCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = BuildingOwnerModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, BuildingOwner(), "management.building_owners")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, BuildingOwner, 'management.building_owners')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = BuildingOwner.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.building_owners"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.building_owners"))
    modify_form = modify_form_constructor(items, "BuildingOwnerModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.building_owners', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.building_owners', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/building_owner.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


# 楼盘列表
@bp.route('/district_times', methods=['GET', 'POST'])
def district_times():
    page = request.args.get('page', 1, type=int)
    items = DistrictTimes.query.paginate(page, 10, False)

    add_form = DistrictTimesCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = DistrictTimesModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, DistrictTimes(), "management.district_times")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, DistrictTimes, "management.district_times")
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = DistrictTimes.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.district_times"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.district_times"))
    modify_form = modify_form_constructor(items, "DistrictTimesModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.district_times', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.district_times', page=items.prev_num) if items.has_prev else None

    return render_template("general/building/district_times.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


# 户型列表
@bp.route('/apartment', methods=['GET', 'POST'])
def apartment():
    page = request.args.get('page', 1, type=int)
    district_times_id = request.args.get('district_times_id', 0, type=int)
    list_district_times = ListDistrictTimes()

    if district_times_id > 0:
        items = Apartment.query.filter_by(district_times_id=district_times_id).order_by(Apartment.order).paginate(page, 10, False)
        list_district_times.list_district_times_id.data = district_times_id
    else:
        items = Apartment.query.order_by(Apartment.order).paginate(page, 10, False)

    add_form = ApartmentCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = ApartmentModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    db_info = create_db_row(add_form, Apartment(), "management.apartment")
                    last_apartment = Apartment.query.order_by(desc(Apartment.id)).first()
                    last_apartment.upgrade_name()
                    return db_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    db_info = modify_db(temp_modify_form, Apartment, "management.apartment")
                    upgraded_apartment = Apartment.query.filter_by(id=int(temp_modify_form.id.data)).first()
                    upgraded_apartment.upgrade_name()
                    return db_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Apartment.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.apartment"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.apartment"))
    modify_form = modify_form_constructor(items, "ApartmentModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.apartment', page=items.next_num, district_times_id=district_times_id) if items.has_next else None
    prev_url = url_for('management.apartment', page=items.prev_num, district_times_id=district_times_id) if items.has_prev else None

    return render_template("general/building/apartment.html", items=items.items,
                           list_district_times = list_district_times,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)