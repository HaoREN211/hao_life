# @Time    : 2020/1/10 20:43
# @Author  : REN Hao
# @FileName: salary.py
# @Software: PyCharm

from operator import and_

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.management.forms.work.salary import SalaryCreateForm, SalaryModifyForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.salary import Salary


@bp.route('/salaries', methods=['GET', 'POST'])
def salaries():
    page = request.args.get('page', 1, type=int)
    items = Salary.query.order_by(Salary.date.desc()).paginate(page, 10, False)

    add_form = SalaryCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = SalaryModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    info_add = create_db_row(add_form, Salary(), "management.salaries")
                    current_row = Salary.query.filter(
                        and_(Salary.work_experience_id == int(add_form.work_experience_id.data),
                             Salary.date == add_form.date.data)
                    ).first()
                    current_row.update_info()
                    return info_add
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Salary, 'management.salaries')
                    current_row = Salary.query.filter(
                        and_(Salary.work_experience_id == int(temp_modify_form.work_experience_id.data),
                             Salary.date == temp_modify_form.date.data)
                    ).first()
                    current_row.update_info()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Salary.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.salaries"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.salaries"))
    modify_form = modify_form_constructor(items, "SalaryModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.salaries', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.salaries', page=items.prev_num) if items.has_prev else None

    return render_template("work/salary.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)
