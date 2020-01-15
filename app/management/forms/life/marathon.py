# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/13 18:16
# IDE：PyCharm

from app.models.marathon import Marathon
from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.country import District
from app.models.consume import ConsumePlate
from app.models.estate import Estate, BuildingType, BuildingProperty, Building, BuildingOwner
from app.models.enterprise import Enterprise

class MarathonCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])

    distance = StringField("距离", render_kw={"type":"number", "step":"0.01"})
    district_id = SelectField("区域所在", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    address = StringField("地址", validators=[Length(max=100)])
    plate_id = SelectField("报名平台", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    apply_start_time = StringField("报名开始时间", render_kw={"type":"datetime-local"})
    apply_end_time = StringField("报名结束时间", render_kw={"type": "datetime-local"})
    match_start_time = StringField("比赛开始时间", render_kw={"type": "datetime-local"})
    match_end_time = StringField("比赛结束时间", render_kw={"type": "datetime-local"})
    is_applied = BooleanField("是否报名")
    is_finished = BooleanField("是否完赛")


    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(MarathonCreateForm, self).__init__(*args, **kwargs)
        self.district_id.choices.extend([(x.id, x.name) for x in District.query.all()])
        self.plate_id.choices.extend([(x.id, x.name) for x in ConsumePlate.query.all()])

    def validate_name(self, name):
        list_marathon = Marathon.query.filter_by(name=str(name.data).strip()).all()
        if list_marathon and (len(list_marathon) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class MarathonModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")

    distance = StringField("距离", render_kw={"type": "number", "step": "0.01"})
    district_id = SelectField("区域所在", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    address = StringField("地址", validators=[Length(max=100)])
    plate_id = SelectField("报名平台", coerce=int, choices=[(0, " ")], default=0,
                           render_kw={"class": "select-control"})
    apply_start_time = StringField("报名开始时间", render_kw={"type": "datetime-local"})
    apply_end_time = StringField("报名结束时间", render_kw={"type": "datetime-local"})
    match_start_time = StringField("比赛开始时间", render_kw={"type": "datetime-local"})
    match_end_time = StringField("比赛结束时间", render_kw={"type": "datetime-local"})
    is_applied = BooleanField("是否报名")
    is_finished = BooleanField("是否完赛")

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(MarathonModifyForm, self).__init__(*args, **kwargs)
        self.district_id.choices.extend([(x.id, x.name) for x in District.query.all()])
        self.plate_id.choices.extend([(x.id, x.name) for x in ConsumePlate.query.all()])

    def validate_name(self, name):
        list_marathon = Marathon.query.filter_by(name=str(name.data).strip()).all()
        if list_marathon and (len(list_marathon) > 0):
            list_id = [x.id for x in list_marathon]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')
