# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 9:38
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from app.models.country import Country, Province

class ProvinceCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired()])
    country_id = SelectField("国家", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ProvinceCreateForm, self).__init__(*args, **kwargs)
        self.country_id.choices.extend([(x.id, x.name) for x in Country.query.all()])

    def validate_name(self, name):
        list_province = Province.query.filter_by(name=str(name.data).strip()).all()
        if list_province and (len(list_province) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ProvinceModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired()])
    country_id = SelectField("国家", coerce=int, choices=[(0, " ")], default=0,
                             render_kw={"class": "select-control"})
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ProvinceModifyForm, self).__init__(*args, **kwargs)
        self.country_id.choices.extend([(x.id, x.name) for x in Country.query.all()])

    def validate_name(self, name):
        list_province = Province.query.filter_by(name=str(name.data).strip()).all()
        if list_province and (len(list_province) > 0):
            list_id = [x.id for x in list_province]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')