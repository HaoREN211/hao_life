# @Time    : 2020/1/10 20:46
# @Author  : REN Hao
# @FileName: salary.py
# @Software: PyCharm

from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, DecimalField, BooleanField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.salary import Salary, WorkExperience


class SalaryCreateForm(RenderForm):
    date = DateField("领工资时间", validators=[DataRequired()], render_kw={"type": "date"})
    work_experience_id = SelectField("工作经历", coerce=int, choices=[(0, " ")], default=0,
                                     render_kw={"class": "select-control"})
    basic_salary = DecimalField("基本工资", validators=[DataRequired()],
                                render_kw={"type": "number", "step": "0.01"})
    personal_endowment = DecimalField("个人养老保险", validators=[DataRequired()],
                                      render_kw={"type": "number", "step": "0.01"})
    personal_medical = DecimalField("个人医疗保险", validators=[DataRequired()],
                                    render_kw={"type": "number", "step": "0.01"})
    personal_unemployment = DecimalField("个人失业保险保险", validators=[DataRequired()],
                                         render_kw={"type": "number", "step": "0.01"})
    personal_provident_fund = DecimalField("个人公积金部分", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    personal_tax = DecimalField("个人所得税", validators=[DataRequired()],
                                render_kw={"type": "number", "step": "0.01"})
    enterprise_endowment = DecimalField("公司缴纳养老保险", validators=[DataRequired()],
                                        render_kw={"type": "number", "step": "0.01"})
    enterprise_medical = DecimalField("公司缴纳医疗保险", validators=[DataRequired()],
                                      render_kw={"type": "number", "step": "0.01"})
    enterprise_supplementary_medical = DecimalField("公司缴纳补充医疗保险", validators=[DataRequired()],
                                                    render_kw={"type": "number", "step": "0.01"})
    enterprise_maternity = DecimalField("公司缴纳生育保险", validators=[DataRequired()],
                                        render_kw={"type": "number", "step": "0.01"})
    enterprise_occupational = DecimalField("公司缴纳工伤保险", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    enterprise_unemployment = DecimalField("公司缴纳失业保险", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    enterprise_provident_fund = DecimalField("公司缴纳公积金", validators=[DataRequired()],
                                             render_kw={"type": "number", "step": "0.01"})

    create_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(SalaryCreateForm, self).__init__(*args, **kwargs)
        self.work_experience_id.choices.extend([(x.id, x.enterprise.name) for x in WorkExperience.query.all()])

    def validate_date(self, date):
        list_salary = Salary.query.filter_by(work_experience_id=int(self.work_experience_id.data)).all()
        if list_salary and (len(list_salary) > 0):
            list_date = [x.date.strftime("%Y-%m") for x in list_salary]
            target_date = date.data.strftime("%Y-%m")
            for current_date in list_date:
                if current_date == target_date:
                    raise ValidationError('添加失败：该月工资已经存在。')


class SalaryModifyForm(RenderForm):
    id = HiddenField("主键")
    date = DateField("领工资时间", validators=[DataRequired()], render_kw={"type": "date"})
    work_experience_id = SelectField("工作经历", coerce=int, choices=[(0, " ")], default=0,
                                     render_kw={"class": "select-control"})
    basic_salary = DecimalField("基本工资", validators=[DataRequired()],
                                render_kw={"type": "number", "step": "0.01"})
    personal_endowment = DecimalField("个人养老保险", validators=[DataRequired()],
                                      render_kw={"type": "number", "step": "0.01"})
    personal_medical = DecimalField("个人医疗保险", validators=[DataRequired()],
                                    render_kw={"type": "number", "step": "0.01"})
    personal_unemployment = DecimalField("个人失业保险保险", validators=[DataRequired()],
                                         render_kw={"type": "number", "step": "0.01"})
    personal_provident_fund = DecimalField("个人公积金部分", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    personal_tax = DecimalField("个人所得税", validators=[DataRequired()],
                                render_kw={"type": "number", "step": "0.01"})
    enterprise_endowment = DecimalField("公司缴纳养老保险", validators=[DataRequired()],
                                        render_kw={"type": "number", "step": "0.01"})
    enterprise_medical = DecimalField("公司缴纳医疗保险", validators=[DataRequired()],
                                      render_kw={"type": "number", "step": "0.01"})
    enterprise_supplementary_medical = DecimalField("公司缴纳补充医疗保险", validators=[DataRequired()],
                                                    render_kw={"type": "number", "step": "0.01"})
    enterprise_maternity = DecimalField("公司缴纳生育保险", validators=[DataRequired()],
                                        render_kw={"type": "number", "step": "0.01"})
    enterprise_occupational = DecimalField("公司缴纳工伤保险", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    enterprise_unemployment = DecimalField("公司缴纳失业保险", validators=[DataRequired()],
                                           render_kw={"type": "number", "step": "0.01"})
    enterprise_provident_fund = DecimalField("公司缴纳公积金", validators=[DataRequired()],
                                             render_kw={"type": "number", "step": "0.01"})

    modify_submit = SubmitField("修改", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(SalaryModifyForm, self).__init__(*args, **kwargs)
        self.work_experience_id.choices.extend([(x.id, x.enterprise.name) for x in WorkExperience.query.all()])

    def validate_work_experience_id(self, work_experience_id):
        list_salary = Salary.query.filter_by(work_experience_id=int(work_experience_id.data)).all()
        list_salary = list(filter(lambda x: x.id != int(self.id.data), list_salary))
        if list_salary and (len(list_salary) > 0):
            list_date = [x.date.strftime("%Y-%m") for x in list_salary]
            target_date = self.date.data.strftime("%Y-%m")
            for current_date in list_date:
                if current_date == target_date:
                    raise ValidationError('修改失败：该月工资已经存在。')
