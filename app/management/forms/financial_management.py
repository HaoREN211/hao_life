# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:12
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class HaoFinancialManagementForm(FlaskForm):
    statistic_data = DateField("统计时间", validators=[DataRequired()])
    daily_interest = DecimalField("当日利息", validators=[DataRequired()])
    submit = SubmitField("确认添加")
