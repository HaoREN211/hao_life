# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/9 15:47
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import ValidationError
from app.models.country import City, Province

class CityCreateForm(RenderForm):
    name = StringField("名称")
    province_id = SelectField("省份", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class":"select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(CityCreateForm, self).__init__(*args, **kwargs)
        self.province_id.choices.extend([(x.id, x.name) for x in Province.query.all()])

    def validate_name(self, name):
        list_city = City.query.filter_by(name=str(name.data).strip()).all()
        if list_city and (len(list_city) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class CityModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    province_id = SelectField("省份", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(CityModifyForm, self).__init__(*args, **kwargs)
        self.province_id.choices.extend([(x.id, x.name) for x in Province.query.all()])

    def validate_name(self, name):
        list_consume_city = City.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_city and (len(list_consume_city) > 0):
            list_id = [x.id for x in list_consume_city]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')