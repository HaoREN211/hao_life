# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/27 8:53
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.character import Weight
from datetime import datetime as dt


class WeightCreateForm(RenderForm):
    date = StringField("上称日期", validators=[DataRequired()], render_kw={"type":"date"})
    weight = StringField("体重(千克)", validators=[DataRequired()], render_kw={"type":"number", "step": "0.1"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_date(self, date):
        list_weight = Weight.query.filter_by(date=dt.strptime(date.data, "%Y-%m-%d")).all()
        if list_weight and (len(list_weight) > 0):
            raise ValidationError('添加失败：《' + str(self.date.data) + '》已经存在，请选择另外一个时间。')
        if dt.strptime(date.data, "%Y-%m-%d").date()>dt.now().date():
            raise ValidationError('今天是' + str(dt.now().year) + "年" + str(dt.now().month) + "月" + str(dt.now().day) + "日，不能未卜先知你未来的体重哦。")

    def validate_weight(self, weight):
        if float(weight.data)>=100:
            raise ValidationError("少年，你确认你的体重已经超过100公斤了吗？")
        if float(weight.data)<0:
            raise ValidationError("少年，体重"+str(self.weight.data)+"不能为负吧？")
        if float(weight.data)<50:
            raise ValidationError("少年，你确认你的体重已经少于50公斤了吗？")

class WeightModifyForm(RenderForm):
    id = HiddenField("主键")
    date = StringField("上称日期", validators=[DataRequired()], render_kw={"type": "date"})
    weight = StringField("体重(千克)", validators=[DataRequired()], render_kw={"type": "number", "step": "0.1"})
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_date(self, date):
        list_weight = Weight.query.filter_by(date=dt.strptime(date.data, "%Y-%m-%d")).all()
        if list_weight and (len(list_weight) > 0):
            list_id = [x.id for x in list_weight]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(date.data) + '》已经存在，请选择另外一个时间。')

        if dt.strptime(date.data, "%Y-%m-%d").date()>dt.now().date():
            raise ValidationError('今天是'+str(dt.now().year)+"年"+str(dt.now().month)+"月"+str(dt.now().day)+"日，不能未卜先知你未来的体重哦。")

    def validate_weight(self, weight):
        if float(weight.data)>=100:
            raise ValidationError("少年，你确认你的体重已经超过100公斤了吗？")
        if float(weight.data)<0:
            raise ValidationError("少年，体重"+str(self.weight.data)+"不能为负吧？")
        if float(weight.data)<50:
            raise ValidationError("少年，你确认你的体重已经少于50公斤了吗？")