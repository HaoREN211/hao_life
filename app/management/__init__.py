# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:17
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('management', __name__)

from app.management.routes import financial_management
from app.management.routes.entertainment import movie, music
from app.management.routes.life import estate, marathon, train, metro
from app.management.routes.consume import consume, consume_way, consume_type, consume_plate, consume_description,house_loan
from app.management.routes.general import constellation, person, shop, enterprise, collect
from app.management.routes.location import province, country, city, dristrict
from app.management.routes.work import salary, work_diaries, work_project, clock_in
from app.management.routes.life.character import weights
