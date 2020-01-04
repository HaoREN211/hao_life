# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:29
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models.movie import Movie


# 定义一个方法，方法的名字规则是：`validate_字段名(self,字段名)`。
def validate_name(form, field):
    list_movie = Movie.query.filter_by(name=str(field.data).strip()).all()
    if len(list_movie) > 0:
        raise ValidationError("电影《" + str(field.data).strip() + "》已经存在")

class MovieForm(FlaskForm):
    name = StringField("电影名字", validators=[DataRequired(), validate_name])
    show_time = DateField("上映时间", validators=[DataRequired()])
    film_length = IntegerField("片长(分)", validators=[DataRequired()])
    bill_link = StringField("海报链接")
    is_watched = BooleanField("是否观看")
    watch_time = DateField("观看时间")
    description = TextAreaField("电影简介", validators=[DataRequired()])
    submit = SubmitField("添加")
