# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/9 16:05
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

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