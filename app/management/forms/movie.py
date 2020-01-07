# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:29
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, IntegerField, BooleanField, TextAreaField, SubmitField, SelectField,
                     HiddenField, SelectMultipleField)
from wtforms.validators import DataRequired, ValidationError, Length
from app.models.movie import Movie, MovieCinema, MovieType
from app.models.country import Country
from app.models.person import Person


class RenderForm(FlaskForm):
    class Meta(FlaskForm.Meta):
        """
        https://www.jianshu.com/p/804cd09b8051
        重写render_field，实现Flask-Bootstrap与render_kw的class并存
        """
        def render_field(self, field, render_kw):
            other_kw = getattr(field, 'render_kw', None)
            if other_kw is not None:
                # 只保留自定义的class
                list_attribute_keep = ["class", "type", "onclick", "readonly", "data-dismiss", "step", "start"]

                for current_attribute in list_attribute_keep:
                    attribute_value = other_kw.get(current_attribute, None)
                    if attribute_value is not None:
                        render_kw[current_attribute] = attribute_value

                # quick_form 时外部传入的值
                class2 = render_kw.get('class', None)
            return field.widget(field, **render_kw)

# 电影类型选择表
class MovieTypeSelectForm(RenderForm):
    list_select = SelectMultipleField("电影类型",
                                      coerce=int, choices=[(1, "test"), (2, "haha")],
                                      render_kw={"class":"select_tags form-control"})
    movie_type_select_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class":"btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type":"button"})


    def __init__(self, *args, **kwargs):
        super(MovieTypeSelectForm, self).__init__(*args, **kwargs)
        all_types = MovieType.query.all()
        self.list_select.choices = [(x.id, x.name) for x  in all_types]

# 电影演员选择表
class MovieActorSelectForm(RenderForm):
    list_select = SelectMultipleField("电影演员",
                                      coerce=int, choices=[(1, "test"), (2, "haha")],
                                      render_kw={"class": "select_tags form-control"})
    movie_actor_select_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(MovieActorSelectForm, self).__init__(*args, **kwargs)
        all_actors = Person.query.all()
        self.list_select.choices = [(x.id, x.name) for x in all_actors]


# 定义一个方法，方法的名字规则是：`validate_字段名(self,字段名)`。
def validate_name(form, field):
    list_movie = Movie.query.filter_by(name=str(field.data).strip()).all()
    if len(list_movie) > 0:
        raise ValidationError("电影《" + str(field.data).strip() + "》已经存在")

class MovieForm(FlaskForm):
    name = StringField("电影名字", validators=[DataRequired(), validate_name])
    show_time = DateField("上映时间", validators=[DataRequired()])
    film_length = IntegerField("片长(分)", validators=[DataRequired()])
    bill_link = StringField("海报链接")
    is_watched = BooleanField("是否观看")
    watch_time = DateField("观看时间")
    description = TextAreaField("电影简介", validators=[DataRequired()])
    cinema_id = SelectField("电影院", validators=[DataRequired()], coerce=int)
    country_id = SelectField("拍摄国家", validators=[DataRequired()], coerce=int)
    submit = SubmitField("添加")

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.cinema_id.choices = [(x.id, x.name) for x in MovieCinema.query.all()]
        self.country_id.choices = [(x.id, x.name) for x in Country.query.all()]

class MovieModifyForm(FlaskForm):
    name = StringField("电影名字", validators=[DataRequired()], render_kw={"readonly":"readonly"})
    show_time = DateField("上映时间", validators=[DataRequired()])
    film_length = IntegerField("片长(分)", validators=[DataRequired()])
    bill_link = StringField("海报链接")
    is_watched = BooleanField("是否观看")
    watch_time = DateField("观看时间")
    description = TextAreaField("电影简介", validators=[DataRequired()])
    cinema_id = SelectField("电影院", validators=[DataRequired()], coerce=int)
    country_id = SelectField("拍摄国家", validators=[DataRequired()], coerce=int)
    submit = SubmitField("添加")

    def __init__(self, *args, **kwargs):
        super(MovieModifyForm, self).__init__(*args, **kwargs)
        self.cinema_id.choices = [(x.id, x.name) for x in MovieCinema.query.all()]
        self.country_id.choices = [(x.id, x.name) for x in Country.query.all()]

class MovieCinemaCreateForm(RenderForm):
    name = StringField("电影院名字", validators=[DataRequired()])
    address = StringField("电影院地址", validators=[DataRequired()])
    add_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    add_cancel = SubmitField("取消", render_kw={"type":"button", "class":"btn btn-xs btn-warning", "data-dismiss":"modal"})

    def validate_name(self, name):
        self_name = self.name.data
        list_cinema = MovieCinema.query.filter_by(name=str(name.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            raise ValidationError('添加失败：《' + str(name.data) + '》已经存在，请挑选另外一个电影院名字。')

    def validate_address(self, address):
        self_address = self.address.data
        list_cinema = MovieCinema.query.filter_by(address=str(address.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            raise ValidationError('添加失败：《' + str(address.data) + '》已经存在，请挑选另外一个电影院地址。')

class MovieDeleteForm(FlaskForm):
    id = HiddenField("主键", validators=[DataRequired()])
    delete_submit = SubmitField("删除")

class MovieCinemaModifyForm(RenderForm):
    id = HiddenField("电影院主键", validators=[DataRequired()])
    name = StringField("电影院名字", validators=[DataRequired()])
    address = StringField("电影院地址", validators=[DataRequired()])
    submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"type": "button",
                                          "class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal"})

    def validate_name(self, name):
        list_cinema = MovieCinema.query.filter_by(name=str(name.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            list_id = [x.id for x in list_cinema]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个电影院名字。')

    def validate_address(self, address):
        list_cinema = MovieCinema.query.filter_by(address=str(address.data).strip()).all()
        if list_cinema and (len(list_cinema) > 0):
            list_id = [x.id for x in list_cinema]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(address.data) + '》已经存在，请挑选另外一个地址。')

class MovieTypeForm(RenderForm):
    name = StringField("电影类型名字", validators=[DataRequired(),
                                             Length(min=1, max=100, message="电影类型长度在1-100之间")])
    movie_type_add_submit = SubmitField("添加", render_kw={"class": "btn btn-xs btn-success"},)
    cancel = SubmitField("取消", render_kw={"type": "button",
                                          "class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal"} )

    def validate_name(self, name):
        temp_name = self.name.data
        users = MovieType.query.filter_by(name=str(name.data)).all()
        if len(users)>0:
            raise ValidationError('已经添加过《'+str(name.data)+'》电影类型。')

class MovieTypeModifyForm(RenderForm):
    id = HiddenField("电影类型主键", validators=[DataRequired()])
    name = StringField("电影院名字", validators=[DataRequired()])
    movie_type_modify_submit = SubmitField("修改", render_kw={"class": "btn btn-xs btn-success"}, )
    cancel = SubmitField("取消", render_kw={"type": "button",
                                          "class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal"})
    def validate_name(self, name):
        list_movie_type = MovieType.query.filter_by(name=str(name.data).strip()).all()
        if list_movie_type and (len(list_movie_type) > 0):
            list_id = [x.id for x in list_movie_type]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个电影类型。')
