# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/9 10:21
# IDE：PyCharm

import datetime

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms.general.enterprise import EnterpriseCreateForm, EnterpriseModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.enterprise import Enterprise


# 消费列表
@bp.route('/consume/enterprises', methods=['GET', 'POST'])
def enterprises():
    page = request.args.get('page', 1, type=int)
    items = Enterprise.query.order_by(Enterprise.rank_2019.asc()).paginate(page, 10, False)

    add_form = EnterpriseCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = EnterpriseModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return add_enterprise(add_form)
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_enterprise(temp_modify_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Enterprise.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.enterprises"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.consumes"))

    modify_form = modify_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.enterprises', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.enterprises', page=items.prev_num) if items.has_prev else None

    return render_template("general/enterprise.html", items=items.items,
                    next_url=next_url, prev_url=prev_url,
                    create_label="添加公司",
                    add_form=add_form, delete_form=delete_form, modify_form=modify_form)


def add_enterprise(add_form):
    to_add = Enterprise(name=str(add_form.name.data).strip())

    to_add.short_name = str(add_form.short_name.data).strip() if ((not add_form.short_name.data is None) and (len(str(add_form.short_name.data).strip())>0)) else None
    to_add.founded_time = add_form.founded_time.data if (
    (not add_form.founded_time.data is None) and (len(str(add_form.founded_time.data).strip()) > 0)) else None
    to_add.president_id = add_form.president_id.data if int(add_form.president_id.data)>0 else None
    to_add.headquarter_id = add_form.headquarter_id.data if int(add_form.headquarter_id.data)>0 else None

    db.session.add(to_add)
    flash("成功添加《"+str(add_form.name.data).strip()+"》")
    return redirect(url_for("management.enterprises"))


def modify_enterprise(temp_modify_form):
    target = Enterprise.query.filter_by(id=int(temp_modify_form.id.data)).first()
    modified_name = temp_modify_form.name.data if ((not temp_modify_form.name.data is None) and (len(str(temp_modify_form.name.data).strip())>0)) else None
    is_modified = False
    if modified_name != target.name:
        is_modified = True
        target.name = modified_name

    rank_2019 = int(temp_modify_form.rank_2019.data)
    if rank_2019 != target.rank_2019:
        target.rank_2019 = rank_2019
        is_modified = True

    modified_name = temp_modify_form.short_name.data if (
    (not temp_modify_form.short_name.data is None) and (len(str(temp_modify_form.short_name.data).strip()) > 0)) else None
    if modified_name != target.name:
        is_modified = True
        target.short_name = modified_name

    form_time = datetime.datetime.strptime(temp_modify_form.founded_time.data, "%Y-%m-%d")
    if target.founded_time != form_time:
        is_modified = True
        target.founded_time = form_time

    target_number = int(temp_modify_form.president_id.data) if int(temp_modify_form.president_id.data) > 0 else None
    if target_number != target.president_id:
        target.president_id = target_number
        is_modified = True

    target_number = int(temp_modify_form.headquarter_id.data) if int(temp_modify_form.headquarter_id.data) > 0 else None
    if target_number != target.headquarter_id:
        target.headquarter_id = target_number
        is_modified = True

    if is_modified:
        flash("修改成功!!!")
    else:
        flash("毫无任何修改")
    return redirect(url_for("management.enterprises"))


# 重新构造修改的表单
def modify_form_constructor(items):
    modify_form = {}

    for current_item in items.items:
        temp_form = EnterpriseModifyForm()
        temp_form.id.data = current_item.id
        temp_form.name.data = current_item.name
        temp_form.short_name.data = current_item.short_name
        temp_form.founded_time.data = current_item.founded_time
        temp_form.president_id.data = 0 if current_item.president_id is None else current_item.president_id
        temp_form.headquarter_id.data = 0 if current_item.headquarter_id is None else current_item.headquarter_id
        temp_form.rank_2019.data = current_item.rank_2019
        modify_form[current_item.id] = temp_form
    return modify_form
