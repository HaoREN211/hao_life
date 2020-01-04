# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 21:22
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.country import Country

# 定义一个方法，方法的名字规则是：`validate_字段名(self,字段名)`。
def validate_name(form, field):
    list_movie = Country.query.filter_by(name=str(field.data).strip()).all()
    if len(list_movie) > 0:
        raise ValidationError("国家《" + str(field.data).strip() + "》已经存在")

class CountryForm(FlaskForm):
    name = StringField("国家名称", validators=[DataRequired(), Length(min=1, max=100), validate_name])
    submit = SubmitField("确认")