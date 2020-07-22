# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/7/22 10:39
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app.models.diary import WorkProjectType
from sqlalchemy import desc
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.work.work_diary import WorkProjectTypeCreateForm, WorkProjectTypeModifyForm


# 工作项目类型
@bp.route('/work_project_type', methods=['GET', 'POST'])
def work_project_type():
    page = request.args.get('page', 1, type=int)
    items = WorkProjectType.query.order_by(desc(WorkProjectType.projects_cnt)).paginate(page, 10, False)

    add_form = WorkProjectTypeCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = WorkProjectTypeModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, WorkProjectType(), "management.work_project_type")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, WorkProjectType, "management.work_project_type", has_update=True)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = WorkProjectType.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.work_project_type"))
        else:
            flash("您不是超级管理员，无法进行项目数据的管理")
            return redirect(url_for("management.work_project_type"))
    modify_form = modify_form_constructor(items, "WorkProjectTypeModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.work_project_type', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.work_project_type', page=items.prev_num) if items.has_prev else None

    return render_template("work/work_project_type.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)