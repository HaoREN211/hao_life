# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/8 18:01
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.diary import WorkDiary

class WorkDiaryCreateForm(RenderForm):
    date = StringField("日期", validators=[DataRequired(), Length(max=100)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_word_diary = WorkDiary.query.filter_by(name=str(name.data).strip()).all()
        if list_word_diary and (len(list_word_diary) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class WorkDiaryModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)], default="  ")
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})
