# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/8 17:58
# IDE：PyCharm

from flask import render_template, request, url_for, redirect, flash
from app.management import bp
from flask_login import current_user
from app import db
from app.models.diary import WorkDiary, WorkDiaryDetail
from app.models.salary import WorkExperience
import datetime as dt
from sqlalchemy import func
from app.management.forms.work.work_diary import WorkDiaryDetailCreateForm, WorkDiaryDetailModifyForm, WorkDiaryDetailDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms import modify_form_constructor
import datetime as dt


# 日记列表
@bp.route('/work_diary/<id>', methods=['GET', 'POST'])
def work_diary(id):
    page = request.args.get('page', 1, type=int)

    data_work_diary = WorkDiary.query.filter_by(id=id).first()
    data_work_diary_details = WorkDiaryDetail.query.filter_by(work_diary_id=id).order_by(WorkDiaryDetail.order).paginate(page, 10, False)
    detail_create_form = WorkDiaryDetailCreateForm()
    detail_modify_form = WorkDiaryDetailModifyForm()
    detail_error_form = None
    detail_delete_form = WorkDiaryDetailDeleteForm()


    # 只有超级管理员能修改或添加日记，而且只接受post请求
    if current_user.is_authenticated and current_user.is_admin and request.method == "POST":
        # 新增日记要求
        if detail_create_form.is_submitted() and detail_create_form.create_submit.data:
            # 填写的新增日记格式有错的话则显示错误
            if not detail_create_form.validate():
                flash_form_errors(detail_create_form)
            else:
                db.session.add(WorkDiaryDetail(
                    order = (1 if WorkDiaryDetail.query.filter_by(work_diary_id=id).count()==0
                             else int(db.session.query(WorkDiaryDetail.order).filter_by(work_diary_id=id).order_by(WorkDiaryDetail.order.desc()).first()[0])+1),
                    content = detail_create_form.content.data,
                    work_diary_id = id,
                    work_project_id = int(detail_create_form.work_project_id.data),
                    create_time = dt.datetime.now(),
                    update_time = dt.datetime.now()
                ))
                return redirect(url_for("management.work_diary", id=id))

        # 修改日记要求
        if detail_modify_form.is_submitted() and detail_modify_form.modify_submit.data:
            if not detail_modify_form.validate():
                detail_error_form = detail_modify_form
                flash_form_errors(detail_modify_form)
            else:
                current_work_diary_detail = WorkDiaryDetail.query.filter_by(id=int(detail_modify_form.id.data)).first()
                # 判断当前用户是否修改了数据
                has_modify = False
                if current_work_diary_detail.work_project_id != int(detail_modify_form.work_project_id.data):
                    current_work_diary_detail.work_project_id = int(detail_modify_form.work_project_id.data)
                    has_modify = True
                if current_work_diary_detail.content != detail_modify_form.content.data:
                    current_work_diary_detail.content = detail_modify_form.content.data
                    has_modify = True
                if has_modify:
                    current_work_diary_detail.update_time = dt.datetime.now()
                    flash("修改成功")
                else:
                    flash("毫无任何修改")
                return redirect(url_for("management.work_diary", id=id))

        # 删除日记要求
        if detail_delete_form.validate_on_submit() and detail_delete_form.delete_submit.data:
            current_work_diary_detail = WorkDiaryDetail.query.filter_by(id=int(detail_delete_form.id.data)).first()
            list_to_modify = WorkDiaryDetail.query.filter(WorkDiaryDetail.work_diary_id==id,
                WorkDiaryDetail.order>current_work_diary_detail.order).order_by(WorkDiaryDetail.order.asc()).all()
            db.session.delete(current_work_diary_detail)
            db.session.commit()
            for current_to_modify in list_to_modify:
                current_to_modify.order = current_to_modify.order-1
            flash("删除成功")
            return redirect(url_for("management.work_diary", id=id))

    # 快速生成修改表单
    modify_form = modify_form_constructor(data_work_diary_details, "WorkDiaryDetailModifyForm")

    # 如果修改的时候出错，保留用户的修改，但不修改数据库
    if not detail_error_form is None:
        modify_form[int(detail_error_form.id.data)] = detail_error_form

    return render_template("work/work_diary.html", work_diary=data_work_diary,
                           work_diary_details=data_work_diary_details.items, create_form=detail_create_form,
                           modify_form=modify_form, delete_form=detail_delete_form)


# 房源列表
@bp.route('/work_diaries', methods=['GET', 'POST'])
def work_diaries():
    page = request.args.get('page', 1, type=int)
    items = WorkDiary.query.order_by(WorkDiary.date.desc()).paginate(page, 10, False)

    # 如果今天还没写过日志，则添加一条可以写的日志。
    if WorkDiary.query.filter_by(date=dt.datetime.now().date()).count() == 0:
        db.session.add(WorkDiary(date = dt.datetime.now().date(),
                work_experience_id = db.session.query(func.max(WorkExperience.id)).first()[0],
                create_time = dt.datetime.now()))
        return redirect(url_for("management.work_diaries"))

    next_url = url_for('management.work_diaries', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.work_diaries', page=items.prev_num) if items.has_prev else None

    return render_template("work/work_diaries.html", items=items.items,
                           next_url=next_url, prev_url=prev_url)
