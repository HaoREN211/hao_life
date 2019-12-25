# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 20:49
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('data', __name__)

from app.data.routes import consume