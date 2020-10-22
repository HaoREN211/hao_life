# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/10/21 18:33
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user, login_required
from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.life.account import AccountCreateForm, AccountModifyForm
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.account import Account


# 账号列表
@bp.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    # 如果不是管理员的话，无法查询账号。跳转到主页面
    if not current_user.is_admin:
        flash("您不是超级管理员，无法查询账户数据")
        return render_template('financial_management/index.html')

    page = request.args.get('page', 1, type=int)
    items = Account.query.filter_by(user_id=current_user.id).paginate(page, 10, False)

    add_form = AccountCreateForm(user_id=current_user.id)
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = AccountModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    return create_db_row(add_form, Account(), "management.accounts")
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Account, 'management.accounts')
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Account.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.accounts"))
        else:
            flash("您不是超级管理员，无法进行账户数据的管理")
            return redirect(url_for("management.accounts"))
    modify_form = modify_form_constructor(items, "AccountModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.accounts', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.accounts', page=items.prev_num) if items.has_prev else None

    return render_template("life/account/account.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)