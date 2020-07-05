# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/21 15:58
# IDE：PyCharm

from flask import render_template, flash, request, url_for, redirect
from flask_login import current_user
from app import db
from app.management import bp
from sqlalchemy import desc
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.movie import MovieDeleteForm
from app.models.collect import Collect, WebSite
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.general.collect import CollectCreateForm, CollectModifyForm, WebSiteModifyForm, CollectNamesForm
import re
from datetime import datetime


@bp.route('/web_sites', methods=['GET', 'POST'])
def web_sites():
    page = request.args.get('page', 1, type=int)
    items = WebSite.query.order_by(desc(WebSite.collect_cnt)).paginate(page, 10, False)

    temp_error_form = None
    temp_modify_form = WebSiteModifyForm()
    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, WebSite, "management.web_sites", has_update=True)
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.web_sites"))
    modify_form = modify_form_constructor(items, "WebSiteModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.web_sites', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.web_sites', page=items.prev_num) if items.has_prev else None

    return render_template("general/web_sites.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           modify_form=modify_form)


# 收藏链接
@bp.route('/collects', methods=['GET', 'POST'])
def collects():
    page = request.args.get('page', 1, type=int)
    collect_id = request.args.get('collect_id', 0, type=int)

    items = Collect.query.order_by().paginate(page, 10, False) if collect_id==0 else Collect.query.filter_by(id=collect_id).paginate(page, 10, False)

    add_form = CollectCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = CollectModifyForm()
    collect_names_form = CollectNamesForm()

    collect_names_form.name.data = collect_id if collect_id>0 else 0

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    # 找到链接中的网站地址
                    pattern = re.compile("(http[s]?://(www)?[^/]+)")
                    result = pattern.findall(add_form.link.data)
                    web_site_id = find_web_site_id(result[0][0])
                    create_info = create_db_row(add_form, Collect(), "management.collects")
                    # 更新链接中的网站地址
                    last_collect = Collect.query.order_by(desc(Collect.id)).first()
                    last_collect.web_site_id=web_site_id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    return modify_db(temp_modify_form, Collect, "management.collects", has_update=True)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Collect.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.collects"))
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.collects"))
    modify_form = modify_form_constructor(items, "CollectModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.collects', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.collects', page=items.prev_num) if items.has_prev else None

    return render_template("general/collects.html", items=items.items,
                           next_url=next_url, prev_url=prev_url, collect_names_form=collect_names_form,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)

# 找到web_site在表中的主键，如果不存在，则新建一条数据再返回它的主键
def find_web_site_id(web_site):
    if WebSite.query.filter_by(link=web_site).count()==0:
        db.session.add(WebSite(link= web_site,
                 create_time= datetime.now(),
                 update_time= datetime.now()))
        db.session.commit()
    return WebSite.query.filter_by(link=web_site).first().id
