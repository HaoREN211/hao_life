# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/23 16:12
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TimestampForm(RenderForm):
    timestamp = StringField("时间戳", validators=[DataRequired(), Length(min=13,max=13,message="时间戳的长度为13位")],
                            render_kw={"type": "number", "step": "1"})
    create_submit = SubmitField("转换", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})