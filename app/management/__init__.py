# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:17
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('management', __name__)

from app.management.routes import financial_management, movie