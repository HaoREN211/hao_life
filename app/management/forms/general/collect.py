# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/21 16:11
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, URL
from app.models.collect import Collect, WebSite

class CollectCreateForm(RenderForm):
    name = StringField("链接收藏名称", validators=[DataRequired(), Length(max=100)])
    link = StringField("链接收藏地址", validators=[DataRequired(), Length(max=1000)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    # 不能再存已经存在的链接
    def validate_link(self, link):
        list_collect = Collect.query.filter_by(link=str(link.data).strip()).all()
        if list_collect and (len(list_collect) > 0):
            raise ValidationError('添加失败：《' + str(self.link.data) + '》已经存在，请挑选另外一个名字。')

class CollectModifyForm(RenderForm):
    id = HiddenField("主键")

    name = StringField("链接收藏名称", validators=[DataRequired(), Length(max=100)])
    link = StringField("链接收藏地址", validators=[DataRequired(), Length(max=1000)])

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    # 不能再修改成为已经存在的链接
    def validate_link(self, link):
        list_collect = Collect.query.filter_by(link=str(link.data).strip()).all()
        if list_collect and (len(list_collect) > 0):
            list_id = [x.id for x in list_collect]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(link.data) + '》已经存在，请存储另外一个链接。')

class WebSiteModifyForm(RenderForm):
    id = HiddenField("主键")

    name = StringField("网站名称", validators=[DataRequired(), Length(max=100)])

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    # 不能再修改成为已经存在的链接
    def validate_name(self, name):
        list_collect = WebSite.query.filter_by(name=str(name.data).strip()).all()
        if list_collect and (len(list_collect) > 0):
            list_id = [x.id for x in list_collect]
            list_id = [0 if int(x) == int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请选择另外一个名称。')


class CollectNamesForm(RenderForm):
    name = SelectField("歌曲名称", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})

    def __init__(self, *args, **kwargs):
        super(CollectNamesForm, self).__init__(*args, **kwargs)
        self.name.choices.extend([(x.id, x.name) for x in Collect.query.all()])


