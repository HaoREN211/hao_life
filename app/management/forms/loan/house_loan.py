# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/9 16:05
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class HouseLoanPlanCreateForm(RenderForm):
    duration = StringField("还款年限(年)", default=30, validators=[DataRequired()],
                           render_kw={"type":"number", "step":"10"})
    start_date = StringField("开始还款日", validators=[DataRequired()], render_kw={"type": "date"})
    end_date = StringField("还款结束日", render_kw={"type": "date"})
    amount_commercial_principal = StringField("商贷本金", default=0, validators=[DataRequired()],
                                              render_kw={"type":"number", "step":"0.01"})
    amount_commercial_tax = StringField("商贷利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_principal = StringField("公积金本金", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_tax = StringField("公积金利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})

    create_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

class HouseLoanPlanModifyForm(RenderForm):
    id = HiddenField("主键")
    duration = StringField("还款年限(年)", default=30, validators=[DataRequired()],
                           render_kw={"type":"number", "step":"10"})
    start_date = StringField("开始还款日", validators=[DataRequired()], render_kw={"type": "date"})
    end_date = StringField("还款结束日", render_kw={"type": "date"})
    amount_commercial_principal = StringField("商贷本金", default=0, validators=[DataRequired()],
                                              render_kw={"type":"number", "step":"0.01"})
    amount_commercial_tax = StringField("商贷利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_principal = StringField("公积金本金", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_tax = StringField("公积金利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})

    create_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

class HouseLoanDetailCreateForm(RenderForm):
    date = StringField("还款日", validators=[DataRequired()], render_kw={"type": "date"})
    term = StringField("还款日", validators=[DataRequired()], render_kw={"type": "number", "step":1})

    commercial_time_hour = StringField("商贷还款",
                                       validators=[DataRequired(), NumberRange(0,23,message="小时数在0-23之间")],
                                       render_kw={"type": "number", "step":1})
    commercial_time_minute = StringField("商贷还款",
                                       validators=[DataRequired(), NumberRange(0, 59, message="分钟数在0-59之间")],
                                       render_kw={"type": "number", "step": 1})
    commercial_time_second = StringField("商贷还款",
                                         validators=[DataRequired(), NumberRange(0, 59, message="秒数在0-59之间")],
                                         render_kw={"type": "number", "step": 1})

    fund_time_hour = StringField("公积金还款",
                                   validators=[DataRequired(), NumberRange(0, 23, message="小时数在0-23之间")],
                                   render_kw={"type": "number", "step": 1})
    fund_time_minute = StringField("公积金还款",
                                     validators=[DataRequired(), NumberRange(0, 59, message="分钟数在0-59之间")],
                                     render_kw={"type": "number", "step": 1})
    fund_time_second = StringField("公积金还款",
                                     validators=[DataRequired(), NumberRange(0, 59, message="秒数在0-59之间")],
                                     render_kw={"type": "number", "step": 1})

    amount_commercial_principal = StringField("商贷本金", default=0, validators=[DataRequired()],
                                              render_kw={"type":"number", "step":"0.01"})
    amount_commercial_tax = StringField("商贷利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_principal = StringField("公积金本金", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})
    amount_fund_tax = StringField("公积金利息", default=0, validators=[DataRequired()],
                                              render_kw={"type": "number", "step": "0.01"})

    create_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})