# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 14:23
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from app.models.consume import ConsumePlate, ConsumeDescription, ConsumeType, ConsumeWay, Shop

class ConsumeCreateForm(RenderForm):
    time = StringField("消费时间",
                       validators=[DataRequired(message="请填写消费时间")],
                       render_kw={"type":"datetime-local"})
    amount = StringField("消费金额", render_kw={"type":"number", "start":"0.00", "step":"0.01"})

    plate_id = SelectField("消费平台", coerce=int, choices=[(0, " ")])
    type_id = SelectField("消费种类", coerce=int, choices=[(0, " ")])
    way_id = SelectField("消费方式", coerce=int, choices=[(0, " ")])
    shop_id = SelectField("消费商家", coerce=int, choices=[(0, " ")])
    description_id = SelectField("消费说明", coerce=int, choices=[(0, " ")])

    consume_create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ConsumeCreateForm, self).__init__(*args, **kwargs)
        self.plate_id.choices.extend([(x.id, x.name) for x in ConsumePlate.query.all()])
        self.type_id.choices.extend([(x.id, x.name) for x in ConsumeType.query.all()])
        self.way_id.choices.extend([(x.id, x.name) for x in ConsumeWay.query.all()])
        self.shop_id.choices.extend([(x.id, x.name) for x in Shop.query.all()])
        self.description_id.choices.extend([(x.id, x.name) for x in ConsumeDescription.query.all()])


class ConsumeModifyForm(RenderForm):
    id = HiddenField("主键")
    time = StringField("消费时间",
                       validators=[DataRequired(message="请填写消费时间")],
                       render_kw={"type":"datetime-local"})
    amount = StringField("消费金额", render_kw={"type":"number", "start":"0.00", "step":"0.01"})

    plate_id = SelectField("消费平台", coerce=int, choices=[(0, " ")])
    type_id = SelectField("消费种类", coerce=int, choices=[(0, " ")])
    way_id = SelectField("消费方式", coerce=int, choices=[(0, " ")])
    shop_id = SelectField("消费商家", coerce=int, choices=[(0, " ")])
    description_id = SelectField("消费说明", coerce=int, choices=[(0, " ")])

    consume_modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})
    def __init__(self, *args, **kwargs):
        super(ConsumeModifyForm, self).__init__(*args, **kwargs)
        self.plate_id.choices.extend([(x.id, x.name) for x in ConsumePlate.query.all()])
        self.type_id.choices.extend([(x.id, x.name) for x in ConsumeType.query.all()])
        self.way_id.choices.extend([(x.id, x.name) for x in ConsumeWay.query.all()])
        self.shop_id.choices.extend([(x.id, x.name) for x in Shop.query.all()])
        self.description_id.choices.extend([(x.id, x.name) for x in ConsumeDescription.query.all()])


class ConsumeWayCreateForm(RenderForm):
    name = StringField("名称")
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_way = ConsumeWay.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_way and (len(list_consume_way) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ConsumeWayModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_way = ConsumeWay.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_way and (len(list_consume_way) > 0):
            list_id = [x.id for x in list_consume_way]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class ConsumeTypeCreateForm(RenderForm):
    name = StringField("名称")
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_type = ConsumeType.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_type and (len(list_consume_type) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ConsumeTypeModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_type = ConsumeType.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_type and (len(list_consume_type) > 0):
            list_id = [x.id for x in list_consume_type]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')


class ConsumePlateCreateForm(RenderForm):
    name = StringField("名称")
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "plate": "button"})

    def validate_name(self, name):
        list_consume_plate = ConsumePlate.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_plate and (len(list_consume_plate) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ConsumePlateModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "plate": "button"})

    def validate_name(self, name):
        list_consume_plate = ConsumePlate.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_plate and (len(list_consume_plate) > 0):
            list_id = [x.id for x in list_consume_plate]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class ConsumeDescriptionCreateForm(RenderForm):
    name = StringField("名称")
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_description = ConsumeDescription.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_description and (len(list_consume_description) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class ConsumeDescriptionModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称")
    modify_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_consume_description = ConsumeDescription.query.filter_by(name=str(name.data).strip()).all()
        if list_consume_description and (len(list_consume_description) > 0):
            list_id = [x.id for x in list_consume_description]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')