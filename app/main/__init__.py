# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 13:55
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main.routes import index