# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 9:39
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app import db
from app.management import bp
from app.management.forms.location.province import ProvinceCreateForm, ProvinceModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.movie import flash_form_errors
from app.models.country import Province


# 消费列表
@bp.route('/provinces', methods=['GET', 'POST'])
def provinces():
    page = request.args.get('page', 1, type=int)
    items = Province.query.order_by().paginate(page, 10, False)

    add_form = ProvinceCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = ProvinceModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return add_province(add_form)
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_province(temp_modify_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Province.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.provinces"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.provinces"))

    modify_form = modify_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.provinces', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.provinces', page=items.prev_num) if items.has_prev else None

    return render_template("general/country/province.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


def add_province(add_form):
    to_add = Province(name=str(add_form.name.data).strip())
    to_add.country_id = int(add_form.country_id.data) if int(add_form.country_id.data)>0 else None
    db.session.add(to_add)
    flash("成功添加《"+str(add_form.name.data).strip()+"》")
    return redirect(url_for("management.provinces"))


def modify_province(temp_modify_form):
    target = Province.query.filter_by(id=int(temp_modify_form.id.data)).first()
    modified_name = temp_modify_form.name.data if ((not temp_modify_form.name.data is None) and (len(str(temp_modify_form.name.data).strip())>0)) else None
    is_modified = False
    if modified_name != target.name:
        is_modified = True
        target.name = modified_name

    target_number = int(temp_modify_form.country_id.data) if int(temp_modify_form.country_id.data)>0 else None
    if target_number != target.country_id:
        is_modified = True
        target.update_country(target_number)

    if is_modified:
        flash("修改成功")
    else:
        flash("毫无任何修改")
    return redirect(url_for("management.provinces"))


# 重新构造修改的表单
def modify_form_constructor(items):
    modify_form = {}

    for current_item in items.items:
        temp_form = ProvinceModifyForm()
        temp_form.id.data = current_item.id
        temp_form.name.data = current_item.name
        temp_form.country_id.data= 0 if current_item.country_id is None else current_item.country_id
        modify_form[current_item.id] = temp_form
    return modify_form
