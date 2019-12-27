# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/27 9:00
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField

class TimeInterval(FlaskForm):
    start_time = DateField("起始时间")
    end_time = DateField("结束时间")
    submit = SubmitField("确认")