# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/8 17:58
# IDE：PyCharm

from os import remove
from os.path import exists

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row, upload_form_constructor, \
    modify_upload
from app.management.forms.general.upload import FileForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.diary import WorkDiary
from app.management.forms.work.work_diary import WorkDiaryCreateForm, WorkDiaryModifyForm


# 房源列表
@bp.route('/work_diaries', methods=['GET', 'POST'])
def work_diaries():
    page = request.args.get('page', 1, type=int)
    items = WorkDiary.query.order_by(WorkDiary.lottery_time.desc()).paginate(page, 10, False)

    add_form = WorkDiaryCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = WorkDiaryModifyForm()
    temp_upload_form = FileForm()


    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    info_create = create_db_row(add_form, WorkDiary(), "management.work_diaries")
                    added_work_diaries = WorkDiary.query.order_by(WorkDiary.id.desc()).first()
                    added_work_diaries.upgrade_unit_price()
                    return info_create
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    info_modify = modify_db(temp_modify_form, WorkDiary, 'management.work_diaries')
                    modified_work_diaries = WorkDiary.query.filter_by(id=int(temp_modify_form.id.data)).first()
                    modified_work_diaries.upgrade_unit_price()
                    return info_modify
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = WorkDiary.query.filter_by(id=int(delete_form.id.data)).first()
                to_delete_file = to_delete.image
                if to_delete_file is not None and len(str(to_delete_file).strip())>0:
                    to_delete_file = "/root/hao_life/app/"+to_delete_file
                    if exists(to_delete_file):
                        remove(to_delete_file)
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.work_diaries"))
            if temp_upload_form.file_submit.data and temp_upload_form.validate_on_submit():
                current_file = request.files['file_select']
                saved_path = modify_upload(current_file, temp_upload_form, "work_diaries")
                current_work_diaries = WorkDiary.query.filter_by(id=int(temp_upload_form.id.data)).first()
                current_work_diaries.image = saved_path
                flash("上传成功")
                return redirect(url_for("management.work_diaries"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.work_diaries"))

    modify_form = modify_form_constructor(items, "WorkDiaryModifyForm")
    upload_image_form = upload_form_constructor(items)
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form


    next_url = url_for('management.work_diaries', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.work_diaries', page=items.prev_num) if items.has_prev else None

    return render_template("work/work_diaries.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form, upload_image_form=upload_image_form)

