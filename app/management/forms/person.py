# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/6 17:44
# IDE：PyCharm

import datetime
from wtforms import IntegerField, HiddenField, StringField, SelectField, DateField, DecimalField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError
from app.management.forms.movie import RenderForm
from app.models.country import Country, City, Constellation, BloodGroup
from app.models.person import Person

class PersonCreateForm(RenderForm):
    name = StringField("名字", validators=[DataRequired(), Length(max=100)])
    bill_link = StringField("海报链接", validators=[Length(max=500)])
    foreign_name = StringField("外国名字", validators=[Length(max=100)])
    sex = SelectField("性别", choices=[(0, "男性"), (1, "女性"), (2, "不明")], coerce=int, default=2)
    birth_day = DateField("出生日期", default=datetime.datetime.strptime("2111-11-11", "%Y-%m-%d"))
    nationality_id = SelectField("国籍", coerce=int, choices=[(0, "暂无")], default=0)
    birth_city_id = SelectField("出生城市", coerce=int, choices=[(0, "暂无")], default=0)
    origin_city_id = SelectField("籍贯城市", coerce=int, choices=[(0, "暂无")], default=0)
    constellation_id = SelectField("星座", coerce=int, choices=[(0, "暂无")], default=0)
    blood_group_id = SelectField("血型", coerce=int, choices=[(0, "暂无")], default=0)
    height = DecimalField("身高(CM)", default=0.0, render_kw={"type":"number", "step":"0.1"})
    weight = DecimalField("体重(G)", default=0.0, render_kw={"type":"number", "step":"0.1"})
    person_add_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(PersonCreateForm, self).__init__(*args, **kwargs)
        self.nationality_id.choices.extend([(x.id, x.name) for x in Country.query.all()])
        self.birth_city_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.origin_city_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.constellation_id.choices.extend([(x.id, x.name) for x in Constellation.query.all()])
        self.blood_group_id.choices.extend([(x.id, x.name) for x in BloodGroup.query.all()])

    def validate_name(self, name):
        list_cinema = Person.query.filter_by(name=str(name.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个人物名字。')


class PersonModifyForm(RenderForm):
    id = HiddenField("ID", validators=[DataRequired()])
    name = StringField("名字", validators=[DataRequired(), Length(max=100)])
    bill_link = StringField("海报链接", validators=[Length(max=500)])
    foreign_name = StringField("外国名字", validators=[Length(max=100)])
    sex = SelectField("性别", choices=[(0, "男性"), (1, "女性"), (2, "不明")], coerce=int, default=2)
    birth_day = StringField("出生日期", render_kw={"type":"date"})
    nationality_id = SelectField("国籍", coerce=int, choices=[(0, "暂无")], default=0)
    birth_city_id = SelectField("出生城市", coerce=int, choices=[(0, "暂无")], default=0)
    origin_city_id = SelectField("籍贯城市", coerce=int, choices=[(0, "暂无")], default=0)
    constellation_id = SelectField("星座", coerce=int, choices=[(0, "暂无")], default=0)
    blood_group_id = SelectField("血型", coerce=int, choices=[(0, "暂无")], default=0)
    height = DecimalField("身高(CM)", default=0.0, render_kw={"type":"number", "step":"0.1"})
    weight = DecimalField("体重(G)", default=0.0, render_kw={"type":"number", "step":"0.1"})
    person_modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(PersonModifyForm, self).__init__(*args, **kwargs)
        self.nationality_id.choices.extend([(x.id, x.name) for x in Country.query.all()])
        self.birth_city_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.origin_city_id.choices.extend([(x.id, x.name) for x in City.query.all()])
        self.constellation_id.choices.extend([(x.id, x.name) for x in Constellation.query.all()])
        self.blood_group_id.choices.extend([(x.id, x.name) for x in BloodGroup.query.all()])

    def validate_name(self, name):
        list_cinema = Person.query.filter_by(name=str(name.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            list_id = [x.id for x in list_cinema]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个人物名字。')