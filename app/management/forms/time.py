# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 10:04
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

class SingleTimeForm(RenderForm):
    date_field = DateField("查询时间", validators=[DataRequired()],
                           default=datetime.now(),
                           render_kw={"type":"date"})
    date_submit = SubmitField("确认", render_kw={"class":"btn btn-xs btn-success"})