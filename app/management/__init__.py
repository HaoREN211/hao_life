# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:17
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('management', __name__)

from app.management.routes import financial_management, movie, estate
from app.management.routes.consume import consume, consume_way, consume_type, consume_plate, consume_description
from app.management.routes.general import constellation, person, shop, enterprise
from app.management.routes.location import province, country, city, dristrict
