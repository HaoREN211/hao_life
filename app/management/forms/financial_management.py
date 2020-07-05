# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:12
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length
from app.management.forms.movie import RenderForm

class HaoFinancialManagementForm(FlaskForm):
    statistic_data = DateField("统计时间", validators=[DataRequired()])
    daily_interest = DecimalField("当日利息", validators=[DataRequired()])
    submit = SubmitField("确认添加")


class HaoFinancialManagementDate(object):
    def __init__(self, date=None, data=None, interval=1, data_max=1, data_min=1):
        self.date = date
        self.data = data
        self.interval = interval
        self.data_max = data_max
        self.data_min = data_min


# 纯商贷部分
class HouseLoanCommercialLoanForm(RenderForm):
    amount = StringField("贷款总金额(万元)", validators=[DataRequired(), Length(max=100)], default="0",
                         render_kw={"type": "number", "step": "1", "class": "form-control"})
    duration = SelectField("贷款年限(年)", coerce=int, choices=[(1, "10"), (2, "20"), (3, "30")], default=3,
                                render_kw={"class": "select-control"})
    tax = StringField("贷款利率(%)",  validators=[DataRequired()], default="5.635",
                      render_kw={"type": "number", "step": "0.01", "class": "form-control"})
    commercial_loan_submit = SubmitField("确认", render_kw={"class":"btn btn-xs btn-success"})


# 公积金贷部分
class HouseLoanFundLoanForm(RenderForm):
    amount = StringField("贷款总金额(万元)", validators=[DataRequired(), Length(max=100)], default="0",
                         render_kw={"type": "number", "step": "1", "class": "form-control"})
    duration = SelectField("贷款年限(年)", coerce=int, choices=[(1, "10"), (2, "20"), (3, "30")], default=3,
                                render_kw={"class": "select-control"})
    tax = SelectField("贷款利率(%)", coerce=int, choices=[(1, "3.25"), (2, "3.575")], default=1,
                           render_kw={"class": "select-control"})
    fund_loan_submit = SubmitField("确认", render_kw={"class":"btn btn-xs btn-success"})


# 组合贷部分
class HouseLoanMergeLoanForm(RenderForm):
    commercial_amount = StringField("商贷贷款总金额(万元)", validators=[DataRequired(), Length(max=100)], default="0",
                         render_kw={"type": "number", "step": "1", "class": "form-control"})
    fund_amount = StringField("公积金贷款总金额(万元)", validators=[DataRequired(), Length(max=100)], default="0",
                                    render_kw={"type": "number", "step": "1", "class": "form-control"})
    duration = SelectField("贷款年限(年)", coerce=int, choices=[(1, "10"), (2, "20"), (3, "30")], default=3,
                                render_kw={"class": "select-control"})
    commercial_tax = StringField("贷款利率(%)",  validators=[DataRequired()], default="5.635",
                      render_kw={"type": "number", "step": "0.01", "class": "form-control"})
    fund_tax = SelectField("公积金贷款利率(%)", coerce=int, choices=[(1, "3.25"), (2, "3.575")], default=1,
                      render_kw={"class": "select-control"})
    merge_loan_submit = SubmitField("确认", render_kw={"class":"btn btn-xs btn-success"})