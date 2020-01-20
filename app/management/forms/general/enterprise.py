# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/9 10:21
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import ValidationError, DataRequired
from app.models.enterprise import Enterprise
from app.models.person import Person
from app.models.country import District

class EnterpriseCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(message="请填写公司名称")])
    short_name = StringField("简称")
    founded_time = StringField("创立时间", validators=[DataRequired(message="请填写公司创立时间")],
                               render_kw={"type":"date"})
    president_id = SelectField("公司总裁", coerce=int, choices=[(0, " ")], default=0,
                               render_kw={"class": "select-control"})
    headquarter_id = SelectField("公司总部", coerce=int, choices=[(0, " ")], default=0,
                                 render_kw={"class":"select-control"})
    rank_2019 = StringField("2019年排名", render_kw={"type": "number", "step": "1"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(EnterpriseCreateForm, self).__init__(*args, **kwargs)
        self.president_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.headquarter_id.choices.extend([(x.id, x.name) for x in District.query.all()])

    def validate_name(self, name):
        list_enterprise = Enterprise.query.filter_by(name=str(name.data).strip()).all()
        if list_enterprise and (len(list_enterprise) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class EnterpriseModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(message="请填写公司名称")])
    short_name = StringField("简称")
    founded_time = StringField("创立时间", validators=[DataRequired(message="请填写公司创立时间")],
                               render_kw={"type": "date"})
    president_id = SelectField("公司总裁", coerce=int, choices=[(0, " ")],
                               render_kw={"class": "select-control"})
    headquarter_id = SelectField("公司总部", coerce=int, choices=[(0, " ")],
                                 render_kw={"class":"select-control"})
    rank_2019 = StringField("2019年排名", render_kw={"type": "number", "step": "1"})
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(EnterpriseModifyForm, self).__init__(*args, **kwargs)
        self.president_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.headquarter_id.choices.extend([(x.id, x.name) for x in District.query.all()])

    def validate_name(self, name):
        list_consume_enterprise = Enterprise.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_enterprise and (len(list_consume_enterprise) > 0):
            list_id = [x.id for x in list_consume_enterprise]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')