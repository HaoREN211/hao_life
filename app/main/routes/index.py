# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 14:03
# IDE：PyCharm

from app.main import bp
from flask import render_template
from config import PageConfig

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title=PageConfig.TITLE)