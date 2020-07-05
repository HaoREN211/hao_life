# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 10:38
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms.location.district import DistrictCreateForm, DistrictModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.country import District


# 消费列表
@bp.route('/districts', methods=['GET', 'POST'])
def districts():
    page = request.args.get('page', 1, type=int)
    items = District.query.order_by().paginate(page, 10, False)

    add_form = DistrictCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = DistrictModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return add_district(add_form)
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_district(temp_modify_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = District.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.districts"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.districts"))

    modify_form = modify_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.districts', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.districts', page=items.prev_num) if items.has_prev else None

    return render_template("general/country/district.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


def add_district(add_form):
    form_name = str(add_form.name.data).strip()
    to_add = District(name=form_name)

    form_city_id = int(add_form.city_id.data)
    to_add.city_id = form_city_id if form_city_id>0 else None
    db.session.add(to_add)

    added_district = District.query.filter_by(name=form_name).first()
    added_district.update_province_id()

    flash("成功添加《"+str(add_form.name.data).strip()+"》")
    return redirect(url_for("management.districts"))


def modify_district(temp_modify_form):
    target = District.query.filter_by(id=int(temp_modify_form.id.data)).first()

    is_modified = False
    is_modified = (is_modified or target.update_name(temp_modify_form.name.data))
    is_modified = (is_modified or target.update_city_id(temp_modify_form.city_id.data))

    if is_modified:
        flash("修改成功")
    else:
        flash("毫无任何修改")
    return redirect(url_for("management.districts"))


# 重新构造修改的表单
def modify_form_constructor(items):
    modify_form = {}

    for current_item in items.items:
        temp_form = DistrictModifyForm()
        temp_form.id.data = current_item.id
        temp_form.name.data = current_item.name
        temp_form.city_id.data= 0 if current_item.city_id is None else current_item.city_id
        modify_form[current_item.id] = temp_form
    return modify_form
