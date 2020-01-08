# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 17:17
# IDE：PyCharm
from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import ValidationError
from app.models.consume import Shop


class ShopCreateForm(RenderForm):
    name = StringField("名称")
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_shop = Shop.query.filter_by(name=str(name.data).strip()).all()
        if list_shop and (len(list_shop) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ShopModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_shop = Shop.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_shop and (len(list_consume_shop) > 0):
            list_id = [x.id for x in list_consume_shop]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')