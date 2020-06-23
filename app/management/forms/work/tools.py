# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/23 16:12
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class TimestampForm(RenderForm):
    timestamp = StringField("时间戳", validators=[DataRequired(), Length(min=13,max=13,message="时间戳的长度为13位")],
                            render_kw={"type": "number", "step": "1"})
    create_submit = SubmitField("转换", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

class EncryptionForm(RenderForm):
    type_id = SelectField("加密方式", coerce=int, choices=[(1, "MD5"),(2, "SHA256"),(3, "BASE64")], default=1,
        render_kw={"class": "select-control"})
    content = StringField("加密内容", validators=[DataRequired()])
    create_submit = SubmitField("加密", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})