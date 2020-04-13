# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/10 11:45
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app.models.diary import WorkProject
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.work.work_diary import WorkProjectCreateForm, WorkProjectModifyForm


# 户型列表
@bp.route('/work_projects', methods=['GET', 'POST'])
def work_projects():
    page = request.args.get('page', 1, type=int)
    items = WorkProject.query.order_by(WorkProject.start_date.desc()).paginate(page, 10, False)

    add_form = WorkProjectCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = WorkProjectModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, WorkProject(), "management.work_projects")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, WorkProject, "management.work_projects", has_update=True)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = WorkProject.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.work_projects"))
        else:
            flash("您不是超级管理员，无法进行项目数据的管理")
            return redirect(url_for("management.work_projects"))
    modify_form = modify_form_constructor(items, "WorkProjectModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.work_projects', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.work_projects', page=items.prev_num) if items.has_prev else None

    item_details = {}
    for current_item in items.items:
        current_details = []
        for current_item_details in sorted(current_item.details, key=lambda x: x.work_diary.date, reverse=True):
            current_details.append({
                "date": current_item_details.work_diary.date,
                "content": current_item_details.content
            })
        item_details[current_item.id] = current_details
    return render_template("work/work_projects.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form, details=item_details)