# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/10/21 18:27
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.account import Account

class AccountCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=50)])
    account = StringField("账号", validators=[DataRequired(), Length(max=30)])
    password = StringField("密码", validators=[Length(max=30)])
    url = StringField("链接", validators=[Length(max=500)])
    comment = StringField("注释", validators=[Length(max=100)])
    user_id = HiddenField("用户ID")

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(AccountCreateForm, self).__init__(*args, **kwargs)
        self.user_id.data = kwargs["user_id"]

    def validate_name(self, name):
        list_account = Account.query.filter_by(name=str(name.data).strip()).all()
        if list_account and (len(list_account) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class AccountModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=50)])
    account = StringField("账号", validators=[DataRequired(), Length(max=30)])
    password = StringField("密码", validators=[Length(max=30)])
    url = StringField("链接", validators=[Length(max=500)])
    comment = StringField("注释", validators=[ Length(max=100)])

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    # 确保名字的唯一性。修改之后的名字不能在修改之前就存在于数据库中
    def validate_name(self, name):
        list_account = Account.query.filter_by(name=str(name.data).strip()).all()
        if list_account and (len(list_account) > 0):
            list_id = [x.id for x in list_account]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')
