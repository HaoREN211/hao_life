# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 14:03
# IDE：PyCharm

from app.main import bp
from flask import render_template
from config import PageConfig
from app.management.routes.financial_management import echarts_financial_management

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    echarts_data = echarts_financial_management()
    return render_template("index.html", title=PageConfig.TITLE, echarts_financial_management=echarts_data)