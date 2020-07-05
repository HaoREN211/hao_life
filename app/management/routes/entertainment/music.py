# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/20 11:53
# IDE：PyCharm

from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms import modify_form_constructor, modify_db, create_db_row
from app.management.forms.entertainment.music import (MusicCreateForm, MusicModifyForm, AlbumCreateForm,
                                                      AlbumModifyForm, MusicTypeCreateForm, MusicTypeModifyForm,
                                                      MusicNamesForm)
from app.management.forms.movie import MovieDeleteForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.music import Music, Album, MusicType
from datetime import datetime
from sqlalchemy import desc


# 音乐列表
@bp.route('/musics', methods=['GET', 'POST'])
def musics():
    page = request.args.get('page', 1, type=int)
    music_id = request.args.get('music_id', 0, type=int)
    items = Music.query.order_by().paginate(page, 10, False) if music_id==0 \
        else Music.query.filter_by(id=music_id).paginate(page, 10, False)

    music_names_form = MusicNamesForm()
    music_names_form.name.data = music_id


    add_form = MusicCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = MusicModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, Music(), "management.musics")
                    last_music = Music.query.order_by(Music.id.desc()).first()
                    last_music.create_user_id = current_user.id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Music, 'management.musics')
                    modified_music = Music.query.get(int(temp_modify_form.id.data))
                    modified_music.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Music.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.musics"))
        else:
            flash("您不是超级管理员，无法进行数据的管理")
            return redirect(url_for("management.musics"))
    modify_form = modify_form_constructor(items, "MusicModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.musics', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.musics', page=items.prev_num) if items.has_prev else None

    return render_template("entertainment/music.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form,
                           music_names_form=music_names_form)


# 专辑列表
@bp.route('/albums', methods=['GET', 'POST'])
def albums():
    page = request.args.get('page', 1, type=int)
    items = Album.query.order_by(desc(Album.music_cnt)).paginate(page, 10, False)

    add_form = AlbumCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = AlbumModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, Album(), "management.albums")
                    last_album = Album.query.order_by(Album.id.desc()).first()
                    last_album.create_user_id = current_user.id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, Album, 'management.albums')
                    modified_album = Album.query.get(int(temp_modify_form.id.data))
                    modified_album.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = Album.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.albums"))
        else:
            flash("您不是超级管理员，无法进行数据的管理")
            return redirect(url_for("management.albums"))
    modify_form = modify_form_constructor(items, "AlbumModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.albums', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.albums', page=items.prev_num) if items.has_prev else None

    return render_template("entertainment/album.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)


# 音乐类型
@bp.route('/music/types', methods=['GET', 'POST'])
def music_types():
    page = request.args.get('page', 1, type=int)
    items = MusicType.query.order_by(desc(MusicType.music_cnt)).paginate(page, 10, False)

    add_form = MusicTypeCreateForm()
    delete_form = MovieDeleteForm()
    temp_error_form = None
    temp_modify_form = MusicTypeModifyForm()

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.create_submit.data and add_form.is_submitted():
                if not add_form.validate():
                    flash_form_errors(add_form)
                else:
                    create_info = create_db_row(add_form, MusicType(), "management.music_types")
                    last_music_type = MusicType.query.order_by(MusicType.id.desc()).first()
                    last_music_type.create_user_id = current_user.id
                    return create_info
            if temp_modify_form.modify_submit.data and temp_modify_form.is_submitted():
                if not temp_modify_form.validate():
                    temp_error_form = temp_modify_form
                    flash_form_errors(temp_modify_form)
                else:
                    modify_info = modify_db(temp_modify_form, MusicType, 'management.music_types')
                    modified_music_type = MusicType.query.get(int(temp_modify_form.id.data))
                    modified_music_type.update_time = datetime.now()
                    return modify_info
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                to_delete = MusicType.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(to_delete)
                flash("删除成功")
                return redirect(url_for("management.music_types"))
        else:
            flash("您不是超级管理员，无法进行数据的管理")
            return redirect(url_for("management.music_types"))
    modify_form = modify_form_constructor(items, "MusicTypeModifyForm")
    if not temp_error_form is None:
        modify_form[int(temp_error_form.id.data)] = temp_error_form

    next_url = url_for('management.music_types', page=items.next_num) if items.has_next else None
    prev_url = url_for('management.music_types', page=items.prev_num) if items.has_prev else None

    return render_template("entertainment/music_type.html", items=items.items,
                           next_url=next_url, prev_url=prev_url,
                           add_form=add_form, delete_form=delete_form, modify_form=modify_form)