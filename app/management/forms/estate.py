# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/10 11:37
# IDE：PyCharm


from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.country import District
from app.models.estate import Estate, BuildingType, BuildingProperty, Building, BuildingOwner, DistrictTimes, Apartment
from app.models.enterprise import Enterprise

class EstateCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    district_id = SelectField("区域所在", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    address = StringField("门牌号码", validators=[Length(max=100)])
    enterprise_id = SelectField("承包公司", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(EstateCreateForm, self).__init__(*args, **kwargs)
        self.district_id.choices.extend([(x.id, x.name) for x in District.query.all()])
        self.enterprise_id.choices.extend([(x.id, x.name) for x in Enterprise.query.all()])

    def validate_name(self, name):
        list_estate = Estate.query.filter_by(name=str(name.data).strip()).all()
        if list_estate and (len(list_estate) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class EstateModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")
    district_id = SelectField("区域所在", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    address = StringField("门牌号码", validators=[Length(max=100)], default="  ")
    enterprise_id = SelectField("承包公司", coerce=int, choices=[(0, " ")], default=0,
                                render_kw={"class": "select-control"})
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(EstateModifyForm, self).__init__(*args, **kwargs)
        self.district_id.choices.extend([(x.id, x.name) for x in District.query.all()])
        self.enterprise_id.choices.extend([(x.id, x.name) for x in Enterprise.query.all()])


    def validate_name(self, name):
        list_estate = Estate.query.filter_by(name=str(name.data).strip()).all()
        if list_estate and (len(list_estate) > 0):
            list_id = [x.id for x in list_estate]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingTypeCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_type = BuildingType.query.filter_by(name=str(name.data).strip()).all()
        if list_building_type and (len(list_building_type) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingTypeModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_type = BuildingType.query.filter_by(name=str(name.data).strip()).all()
        if list_building_type and (len(list_building_type) > 0):
            list_id = [x.id for x in list_building_type]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingPropertyCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_property = BuildingProperty.query.filter_by(name=str(name.data).strip()).all()
        if list_building_property and (len(list_building_property) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingPropertyModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_property = BuildingProperty.query.filter_by(name=str(name.data).strip()).all()
        if list_building_property and (len(list_building_property) > 0):
            list_id = [x.id for x in list_building_property]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingCreateForm(RenderForm):
    surface = DecimalField("面积", validators=[DataRequired(message="请填写房屋面积")],
                           render_kw={"type":"number", "step":"0.01"})
    total_price = DecimalField("总价（单位：万元）", validators=[DataRequired("请填写房屋总价")],
                               render_kw={"type":"number", "step":"0.01"})
    total_level = StringField("总楼层", render_kw={"type": "number", "step": "1"})
    has_elevator = BooleanField("是否有电梯")
    type_id = SelectField("户型", coerce=int, choices=[(0, " ")], default=0,
                                render_kw={"class": "select-control"})
    property_id = SelectField("产权", coerce=int, choices=[(0, " ")], default=0,
                          render_kw={"class": "select-control"})
    estate_id = SelectField("小区", coerce=int, choices=[(0, " ")], default=0,
                          render_kw={"class": "select-control"})
    owner_id = SelectField("属性", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    build_time = DateField("建造时间", render_kw={"type":"date"})
    lottery_time = DateField("摇号时间", render_kw={"type": "date"})
    link = StringField("网页链接", validators=[Length(max=500)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(BuildingCreateForm, self).__init__(*args, **kwargs)
        self.property_id.choices.extend([(x.id, x.name) for x in BuildingProperty.query.all()])
        self.type_id.choices.extend([(x.id, x.name) for x in BuildingType.query.all()])
        self.estate_id.choices.extend([(x.id, x.name) for x in Estate.query.all()])
        self.owner_id.choices.extend([(x.id, x.name) for x in BuildingOwner.query.all()])

    def validate_name(self, name):
        list_building = Building.query.filter_by(name=str(name.data).strip()).all()
        if list_building and (len(list_building) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')


class BuildingModifyForm(RenderForm):
    id = HiddenField("主键")
    surface = DecimalField("面积", validators=[DataRequired(message="请填写房屋面积")],
                           render_kw={"type": "number", "step": "0.01"})
    total_price = DecimalField("总价（单位：万元）", validators=[DataRequired()], render_kw={"type":"number", "step":"0.01"})
    total_level = StringField("总楼层", render_kw={"type": "number", "step": "1"})
    has_elevator = BooleanField("是否有电梯")
    type_id = SelectField("户型", coerce=int, choices=[(0, " ")], default=0,
                          render_kw={"class": "select-control"})
    property_id = SelectField("产权", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    estate_id = SelectField("小区", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    owner_id = SelectField("属性", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    build_time = DateField("建造时间", render_kw={"type": "date"})
    lottery_time = DateField("摇号时间", render_kw={"type": "date"})
    link = StringField("网页链接", validators=[Length(max=500)])
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(BuildingModifyForm, self).__init__(*args, **kwargs)
        self.property_id.choices.extend([(x.id, x.name) for x in BuildingProperty.query.all()])
        self.type_id.choices.extend([(x.id, x.name) for x in BuildingType.query.all()])
        self.estate_id.choices.extend([(x.id, x.name) for x in Estate.query.all()])
        self.owner_id.choices.extend([(x.id, x.name) for x in BuildingOwner.query.all()])

    def validate_name(self, name):
        list_building = Building.query.filter_by(name=str(name.data).strip()).all()
        if list_building and (len(list_building) > 0):
            list_id = [x.id for x in list_building]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')


class BuildingOwnerCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_owner = BuildingOwner.query.filter_by(name=str(name.data).strip()).all()
        if list_building_owner and (len(list_building_owner) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class BuildingOwnerModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_building_owner = BuildingOwner.query.filter_by(name=str(name.data).strip()).all()
        if list_building_owner and (len(list_building_owner) > 0):
            list_id = [x.id for x in list_building_owner]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class DistrictTimesCreateForm(RenderForm):
    name = StringField("楼盘名称", validators=[DataRequired(), Length(max=100)])
    estate_id = SelectField("楼盘", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    times = StringField("期数", render_kw={"type": "number", "step": "1"})
    start_register_time = StringField("登记开始时间", render_kw={"type": "date"})
    end_register_time = StringField("登记结束时间", render_kw={"type": "date"})
    lotto_date = StringField("摇号时间", render_kw={"type": "date"})
    pick_date = StringField("选房时间", render_kw={"type": "date"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(DistrictTimesCreateForm, self).__init__(*args, **kwargs)
        self.estate_id.choices.extend([(x.id, x.name) for x in Estate.query.all()])

class DistrictTimesModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("楼盘名称", validators=[DataRequired(), Length(max=100)])
    estate_id = SelectField("楼盘", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    times = StringField("期数", render_kw={"type": "number", "step": "1"})
    start_register_time = StringField("登记开始时间", render_kw={"type": "date"})
    end_register_time = StringField("登记结束时间", render_kw={"type": "date"})
    lotto_date = StringField("摇号时间", render_kw={"type": "date"})
    pick_date = StringField("选房时间", render_kw={"type": "date"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(DistrictTimesModifyForm, self).__init__(*args, **kwargs)
        self.estate_id.choices.extend([(x.id, x.name) for x in Estate.query.all()])

class ApartmentCreateForm(RenderForm):
    district_times_id = SelectField("楼盘", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    order = StringField("期望顺序", render_kw={"type": "number", "step": "1"})
    building_number = StringField("栋数", render_kw={"type": "number", "step": "1"})
    floor = StringField("楼层", render_kw={"type": "number", "step": "1"})
    number = StringField("号数", render_kw={"type": "number", "step": "1"})
    size = StringField("建筑面积(平方米)", render_kw={"type": "number", "step": "0.01"})
    unique_price = StringField("单价(元)", render_kw={"type": "number", "step": "0.01"})
    total_price = StringField("总价(元)", render_kw={"type": "number", "step": "0.01"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ApartmentCreateForm, self).__init__(*args, **kwargs)
        self.district_times_id.choices.extend([(x.id, x.name) for x in DistrictTimes.query.all()])


class ApartmentModifyForm(RenderForm):
    id = HiddenField("主键")

    district_times_id = SelectField("楼盘", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    order = StringField("期望顺序", render_kw={"type": "number", "step": "1"})
    building_number = StringField("栋数", render_kw={"type": "number", "step": "1"})
    floor = StringField("楼层", render_kw={"type": "number", "step": "1"})
    number = StringField("号数", render_kw={"type": "number", "step": "1"})
    size = StringField("建筑面积(平方米)", render_kw={"type": "number", "step": "0.01"})
    unique_price = StringField("单价(元)", render_kw={"type": "number", "step": "0.01"})
    total_price = StringField("总价(元)", render_kw={"type": "number", "step": "0.01"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(ApartmentModifyForm, self).__init__(*args, **kwargs)
        self.district_times_id.choices.extend([(x.id, x.name) for x in DistrictTimes.query.all()])


class ListDistrictTimes(RenderForm):
    list_district_times_id = SelectField("楼盘", coerce=int, choices=[(0, " ")], default=0,
                                    render_kw={"class": "select-control"})
    def __init__(self, *args, **kwargs):
        super(ListDistrictTimes, self).__init__(*args, **kwargs)
        self.list_district_times_id.choices.extend([(x.id, x.name) for x in DistrictTimes.query.all()])