# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/20 15:05
# IDE：PyCharm

from app.models.music import Music, Album, MusicType
from app.models.person import Person
from app.management.forms.movie import RenderForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Length

class MusicCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    issue_date = StringField("发行时间", render_kw={"type":"date"})

    lyrics_id = SelectField("作词人", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    composer_id = SelectField("作曲人", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    singer_id = SelectField("演唱人", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    album_id = SelectField("专辑", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    music_type_id = SelectField("音乐类型", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(MusicCreateForm, self).__init__(*args, **kwargs)
        self.lyrics_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.composer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.singer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.album_id.choices.extend([(x.id, x.name) for x in Album.query.all()])
        self.music_type_id.choices.extend([(x.id, x.name) for x in MusicType.query.all()])

    def validate_name(self, name):
        list_music = Music.query.filter_by(name=str(name.data).strip()).all()
        if list_music and (len(list_music) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class MusicModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    issue_date = StringField("发行时间", render_kw={"type": "date"})

    lyrics_id = SelectField("作词人", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    composer_id = SelectField("作曲人", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    singer_id = SelectField("演唱人", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    album_id = SelectField("专辑", coerce=int, choices=[(0, " ")], default=0,
                           render_kw={"class": "select-control"})
    music_type_id = SelectField("音乐类型", coerce=int, choices=[(0, " ")], default=0,
                                render_kw={"class": "select-control"})

    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(MusicModifyForm, self).__init__(*args, **kwargs)
        self.lyrics_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.composer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.singer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])
        self.album_id.choices.extend([(x.id, x.name) for x in Album.query.all()])
        self.music_type_id.choices.extend([(x.id, x.name) for x in MusicType.query.all()])

    def validate_name(self, name):
        list_music = Music.query.filter_by(name=str(name.data).strip()).all()
        if list_music and (len(list_music) > 0):
            list_id = [x.id for x in list_music]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')

class AlbumCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    issue_date = StringField("发行时间", render_kw={"type": "date"})
    singer_id = SelectField("演唱人", coerce=int, choices=[(0, " ")], default=0,
                              render_kw={"class": "select-control"})
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.singer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])

    def validate_name(self, name):
        list_album = Album.query.filter_by(name=str(name.data).strip()).all()
        if list_album and (len(list_album) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class AlbumModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    issue_date = StringField("发行时间", render_kw={"type": "date"})
    singer_id = SelectField("演唱人", coerce=int, choices=[(0, " ")], default=0,
                            render_kw={"class": "select-control"})
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def __init__(self, *args, **kwargs):
        super(AlbumModifyForm, self).__init__(*args, **kwargs)
        self.singer_id.choices.extend([(x.id, x.name) for x in Person.query.all()])

    def validate_name(self, name):
        list_album = Album.query.filter_by(name=str(name.data).strip()).all()
        if list_album and (len(list_album) > 0):
            list_id = [x.id for x in list_album]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')


class MusicTypeCreateForm(RenderForm):
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    create_submit = SubmitField("添加", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_music_type = MusicType.query.filter_by(name=str(name.data).strip()).all()
        if list_music_type and (len(list_music_type) > 0):
            raise ValidationError('添加失败：《' + str(self.name.data) + '》已经存在，请挑选另外一个名字。')

class MusicTypeModifyForm(RenderForm):
    id = HiddenField("主键")
    name = StringField("名称", validators=[DataRequired(), Length(max=100)])
    modify_submit = SubmitField("修改", render_kw={"class":"btn btn-xs btn-success"})
    cancel = SubmitField("取消", render_kw={"class": "btn btn-xs btn-warning",
                                          "data-dismiss": "modal",
                                          "type": "button"})

    def validate_name(self, name):
        list_music_type = MusicType.query.filter_by(name=str(name.data).strip()).all()
        if list_music_type and (len(list_music_type) > 0):
            list_id = [x.id for x in list_music_type]
            list_id = [0 if int(x)==int(self.id.data) else 1 for x in list_id]
            if sum(list_id) > 0:
                raise ValidationError('修改失败：《' + str(name.data) + '》已经存在，请挑选另外一个名字。')
