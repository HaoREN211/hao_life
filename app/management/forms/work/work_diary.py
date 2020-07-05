# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/4/9 15:59
# IDE：PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, TextAreaField
from app.models.diary import WorkProject, WorkDiaryDetail
from operator import and_
from wtforms.validators import ValidationError, DataRequired, Length


class WorkProjectCreateForm(RenderForm):
    name = StringField("项目名称", validators=[DataRequired(), Length(max=50)])
    start_date = StringField("开始日期", validators=[DataRequired()], render_kw={"type":"date"})
    end_date = StringField("结束日期", validators=[DataRequired()], render_kw={"type":"date"})

    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

class WorkProjectModifyForm(RenderForm):
    id = HiddenField("项目主键")
    name = StringField("项目名称", validators=[DataRequired(), Length(max=50)], default="  ")
    start_date = StringField("开始日期", validators=[DataRequired()], render_kw={"type":"date"})
    end_date = StringField("结束日期", validators=[DataRequired()], render_kw={"type":"date"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})



class WorkDiaryDetailModifyForm(RenderForm):
    id = HiddenField("主键")

    work_diary_id = HiddenField()
    work_project_id = SelectField("项目", coerce=int, choices=[(0, " ")], default=0,
                                  render_kw={"class": "select-control"})
    content = TextAreaField("内容")

    modify_submit = SubmitField("修改", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(WorkDiaryDetailModifyForm, self).__init__(*args, **kwargs)
        self.work_project_id.choices.extend([(x.id, x.name) for x in WorkProject.query.all()])


    def validate_work_project_id(self, work_project_id):
        if(WorkDiaryDetail.query.filter(and_(and_(
            WorkDiaryDetail.work_project_id==int(self.work_project_id.data),
            WorkDiaryDetail.work_diary_id == int(self.work_diary_id.data)),
            WorkDiaryDetail.id!=int(self.id.data)
        )).count() > 0):
            raise ValidationError('修改失败：重复项目')


class WorkDiaryDetailDeleteForm(RenderForm):
    id = HiddenField("主键")

    delete_submit = SubmitField("删除", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})


class WorkDiaryDetailCreateForm(RenderForm):
    content = TextAreaField("内容")
    work_diary_id = HiddenField()
    work_project_id = SelectField("项目", coerce=int, choices=[(0, " ")], default=0,
                                  render_kw={"class": "select-control"})


    create_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})


    def __init__(self, *args, **kwargs):
        super(WorkDiaryDetailCreateForm, self).__init__(*args, **kwargs)
        self.work_project_id.choices.extend([(x.id, x.name) for x in WorkProject.query.all()])


    def validate_content(self, content):
        if(WorkDiaryDetail.query.filter(and_(
            WorkDiaryDetail.work_project_id==int(self.work_project_id.data),
            WorkDiaryDetail.work_diary_id == int(self.work_diary_id.data)
        )).count() >0):
            raise ValidationError('添加失败：重复项目')



