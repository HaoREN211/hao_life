# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/23 20:57
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.country import City
from app.models.train import TrainNumber

class TrainCreateForm(RenderForm):
    cost = StringField("票价", render_kw={"type":"number", "step":"0.01"})

    time_from = StringField("乘坐时间", render_kw={"type":"datetime-local"})
    time_to = StringField("下车时间", render_kw={"type": "datetime-local"})

    city_from_id = SelectField("乘坐起始地", coerce=int, choices=[(0, " ")], default=0,
                                render_kw={"class": "select-control"})
    city_to_id = SelectField("乘坐下车地", coerce=int, choices=[(0, " ")], default=0,
                               render_kw={"class": "select-control"})
    train_number_id = SelectField("火车班次", coerce=int, choices=[(0, " ")], default=0,
                             render_kw={"class": "select-control"})


    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(TrainCreateForm, self).__init__(*args, **kwargs)
        self.city_from_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.city_to_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.train_number_id.choices.extend([(x.id, x.name) for x in TrainNumber.query.all()])

class TrainModifyForm(RenderForm):
    id = HiddenField("主键")
    cost = StringField("票价", render_kw={"type": "number", "step": "0.01"})

    time_from = StringField("乘坐时间", render_kw={"type": "datetime-local"})
    time_to = StringField("下车时间", render_kw={"type": "datetime-local"})

    city_from_id = SelectField("乘坐起始地", coerce=int, choices=[(0, " ")], default=0,
                               render_kw={"class": "select-control"})
    city_to_id = SelectField("乘坐下车地", coerce=int, choices=[(0, " ")], default=0,
                             render_kw={"class": "select-control"})
    train_number_id = SelectField("火车班次", coerce=int, choices=[(0, " ")], default=0,
                                  render_kw={"class": "select-control"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(TrainModifyForm, self).__init__(*args, **kwargs)
        self.city_from_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.city_to_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.train_number_id.choices.extend([(x.id, x.name) for x in TrainNumber.query.all()])


class TrainNumberCreateForm(RenderForm):
    name = StringField("班次名称", validators=[DataRequired(), Length(max=100)])
    city_from_id = SelectField("起始地", coerce=int, choices=[(0, " ")], default=0,
                                render_kw={"class": "select-control"})
    city_to_id = SelectField("终止地", coerce=int, choices=[(0, " ")], default=0,
                               render_kw={"class": "select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(TrainNumberCreateForm, self).__init__(*args, **kwargs)
        self.city_from_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.city_to_id.choices.extend([(x.id, x.name) for x in City.query.all()])

    def validate_name(self, name):
        list_train_number = TrainNumber.query.filter_by(name=str(name.data).strip()).all()
        if list_train_number and (len(list_train_number) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class TrainNumberModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("班次名称", validators=[DataRequired(), Length(max=100)])
    city_from_id = SelectField("起始地", coerce=int, choices=[(0, " ")], default=0,
                               render_kw={"class": "select-control"})
    city_to_id = SelectField("终止地", coerce=int, choices=[(0, " ")], default=0,
                             render_kw={"class": "select-control"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(TrainNumberModifyForm, self).__init__(*args, **kwargs)
        self.city_from_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.city_to_id.choices.extend([(x.id, x.name) for x in City.query.all()])

    def validate_name(self, name):
        list_train_number = TrainNumber.query.filter_by(name=str(name.data).strip()).all()
        if list_train_number and (len(list_train_number) > 0):
            list_id = [x.id for x in list_train_number]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')
