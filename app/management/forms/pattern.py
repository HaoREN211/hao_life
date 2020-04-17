# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/17 14:36
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField

class DateForm(RenderForm):
    date = StringField("日期", render_kw={"type":"date", "class":"form-control"})
