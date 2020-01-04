# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 21:18
# IDE：PyCharm

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.management import bp
from app.models.country import Country
from app.management.forms.country import CountryForm


# 国家列表
@bp.route('/countries', methods=['GET'])
def countries():
    page = request.args.get('page', 1, type=int)
    countries = Country.query.paginate(page, 15, False)
    next_url = url_for('management.counties', page=countries.next_num) if countries.has_next else None
    prev_url = url_for('management.counties', page=countries.prev_num) if countries.has_prev else None
    return render_template("general/country/countries.html", countries=countries.items, next_url=next_url, prev_url=prev_url)


# 添加国家
@bp.route('/country/add', methods=['GET', 'POST'])
@login_required
def country_add():
    if not current_user.is_admin:
        flash("您不是超级管理员，无法进行国家数据的管理")
        return redirect(url_for("management.countries"))
    country_form = CountryForm()
    if country_form.is_submitted():
        if country_form.validate():
            to_add = Country(
                name = str(country_form.name.data).strip()
            )
            db.session.add(to_add)
            flash("成功添加国家《"+country_form.name.data+"》")
            return redirect(url_for("management.countries"))
        else:
            first_key = list(country_form.errors.keys())[0]
            flash(country_form.errors[first_key])
    return render_template("general/country/country_add.html", country_form=country_form)