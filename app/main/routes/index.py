# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 14:03
# IDE：PyCharm

from app import db
from app.main import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user
from config import PageConfig
from app.management.routes.financial_management import echarts_financial_management
from app.management.routes.work.salary import e_chart_salary
from app.models.user import User
from app.main.forms.user import UserForm, LoginForm
from werkzeug.urls import url_parse

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    echarts_data = echarts_financial_management()
    echarts_salary = e_chart_salary()
    return render_template("index.html", title=PageConfig.TITLE, echarts_financial_management=echarts_data,
                           e_chart_salary=echarts_salary)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    user_form = UserForm()
    if user_form.validate_on_submit():
        user = User(username=user_form.username.data)
        user.set_password(user_form.password.data)
        db.session.add(user)
    return render_template("register.html", user_form=user_form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('management.financial_management'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=login_form.remember_me.data)

        # 原始URL设置了next查询字符串参数后，应用就可以在登录后使用它来重定向。
        # 装饰器将拦截请求并以重定向到*/login来响应，
        # 但是它会添加一个查询字符串参数来丰富这个URL，如/login?next=/index*。
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("login.html", login_form=login_form)


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))