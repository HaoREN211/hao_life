# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/13 18:10
# IDE：PyCharm

from app import db
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user
from app.management import bp
from app.models.marathon import Marathon
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.movie import flash_form_errors
from app.management.forms.life.marathon import MarathonCreateForm, MarathonModifyForm

# 小区列表
@bp.route('/marathons', methods=['GET', 'POST'])
def marathons():
    page = request.args.get('page', 1, type=int)
    items = Marathon.query.order_by().paginate(page, 10, False)

    add_form = MarathonCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = MarathonModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, Marathon(), "management.marathons")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Marathon, 'management.marathons')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Marathon.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.marathons"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.marathons"))
    modify_form = modify_form_constructor(items, "MarathonModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.marathons', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.marathons', page=items.prev_num) if items.has_prev else None

    return render_template("life/marathons.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)
