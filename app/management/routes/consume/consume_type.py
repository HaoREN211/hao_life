# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 16:57
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app import db
from app.management import bp
from app.models.consume import ConsumeType
from app.management.routes.movie import flash_form_errors
from app.management.forms.consume import ConsumeTypeCreateForm, ConsumeTypeModifyForm
from app.management.forms.movie import MovieDeleteForm
from sqlalchemy import desc

# 消费列表
@bp.route('/consume/types', methods=['GET', 'POST'])
def consume_types():
    page = request.args.get('page', 1, type=int)
    items = ConsumeType.query.order_by(desc(ConsumeType.consume_cnt)).paginate(page, 10, False)

    add_form = ConsumeTypeCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = ConsumeTypeModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return add_consume_type(add_form)
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_consume_type(temp_modify_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = ConsumeType.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.consume_types"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.consumes"))

    modify_form = modify_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.consume_types', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.consume_types', page=items.prev_num) if items.has_prev else None

    return render_template("financial_management/consume/relative.html", items=items.items,
                    next_url=next_url, prev_url=prev_url,
                    add_form=add_form, delete_form=delete_form, modify_form=modify_form)


def add_consume_type(add_form):
    to_add = ConsumeType(name=str(add_form.name.data).strip())
    db.session.add(to_add)
    flash("成功添加《"+str(add_form.name.data).strip()+"》")
    return redirect(url_for("management.consume_types"))


def modify_consume_type(temp_modify_form):
    target = ConsumeType.query.filter_by(id=int(temp_modify_form.id.data)).first()
    modified_name = temp_modify_form.name.data if ((not temp_modify_form.name.data is None) and (len(str(temp_modify_form.name.data).strip())>0)) else None
    original_name = target.name
    is_modified = False
    if modified_name != target.name:
        is_modified = True
        target.name = modified_name
    if is_modified:
        flash("成功将《"+original_name+"》修改为《"+modified_name+"》")
    else:
        flash("毫无任何修改")
    return redirect(url_for("management.consume_types"))


# 重新构造修改的表单
def modify_form_constructor(items):
    modify_form = {}

    for current_item in items.items:
        temp_form = ConsumeTypeModifyForm()
        temp_form.id.data = current_item.id
        temp_form.name.data = current_item.name
        modify_form[current_item.id] = temp_form
    return modify_form
