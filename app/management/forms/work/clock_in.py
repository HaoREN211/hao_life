# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/29 20:21
# IDE：PyCharm


from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.clock_in import ClockIn
from datetime import datetime as dt


class ClockInCreateForm(RenderForm):
    date = StringField("日期", validators=[DataRequired()], render_kw={"type": "date"})

    clock_in_time = StringField("签到时间", validators=[DataRequired()], render_kw={"type": "datetime-local"})
    clock_out_time = StringField("签到时间", validators=[DataRequired()], render_kw={"type": "datetime-local"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_date(self, date):
        list_clock_in = ClockIn.query.filter_by(date=dt.strptime(date.data, "%Y-%m-%d")).all()
        if list_clock_in and (len(list_clock_in) > 0):
            raise ValidationError('添加失败：《' + str(self.date.data) + '》已经存在，请挑选另外一个日期。')

    def validate_clock_in_time(self, clock_in_time):
        clock_in_time = dt.strptime(clock_in_time.data, "%Y-%m-%dT%H:%M")
        clock_out_time = dt.strptime(self.clock_out_time.data, "%Y-%m-%dT%H:%M")
        if clock_in_time.strftime("%Y-%m-%d") != clock_out_time.strftime("%Y-%m-%d"):
            raise ValidationError("签到时间和签退时间不属于同一天")

    def validate_clock_out_time(self, clock_out_time):
        clock_in_time = dt.strptime(self.clock_in_time.data, "%Y-%m-%dT%H:%M")
        clock_out_time = dt.strptime(clock_out_time.data, "%Y-%m-%dT%H:%M")
        if clock_out_time < clock_in_time:
            raise ValidationError("签退时间不能早于签到时间")



class ClockInModifyForm(RenderForm):
    id = HiddenField("主键")

    date = StringField("日期", validators=[DataRequired()], render_kw={"type": "date"})

    clock_in_time = StringField("签到时间", validators=[DataRequired()], render_kw={"type": "datetime-local"})
    clock_out_time = StringField("签到时间", validators=[DataRequired()], render_kw={"type": "datetime-local"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_date(self, date):
        list_clock_in = ClockIn.query.filter_by(date=dt.strptime(date.data, "%Y-%m-%d")).all()
        if list_clock_in and (len(list_clock_in) > 0):
            list_id = [x.id for x in list_clock_in]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(date.data) + '》已经存在，请挑选另外一个日期。')

    def validate_clock_in_time(self, clock_in_time):
        clock_in_time = dt.strptime(clock_in_time.data, "%Y-%m-%dT%H:%M")
        clock_out_time = dt.strptime(self.clock_out_time.data, "%Y-%m-%dT%H:%M")
        if clock_in_time.strftime("%Y-%m-%d") != clock_out_time.strftime("%Y-%m-%d"):
            raise ValidationError("签到时间和签退时间不属于同一天")

    def validate_clock_out_time(self, clock_out_time):
        clock_in_time = dt.strptime(self.clock_in_time.data, "%Y-%m-%dT%H:%M")
        clock_out_time = dt.strptime(clock_out_time.data, "%Y-%m-%dT%H:%M")
        if clock_out_time < clock_in_time:
            raise ValidationError("签退时间不能早于签到时间")