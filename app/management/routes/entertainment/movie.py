# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:25
# IDE：PyCharm

from app import db
from app.management import bp
from flask import render_template, request, flash, url_for, redirect, current_app
from flask_login import login_required, current_user
from app.models.movie import Movie, MovieCinema, MovieType
from app.management.forms.movie import (MovieForm, MovieTypeForm, MovieModifyForm,
                                        MovieCinemaModifyForm, MovieDeleteForm, MovieCinemaCreateForm,
                                        MovieTypeModifyForm, MovieTypeSelectForm, MovieActorSelectForm)
from sqlalchemy import desc
from datetime import datetime
from app.management.forms.general.upload import LinkForm
from urllib import request as urllib_request
from app.tools import get_file_type
from os import makedirs, remove
from os.path import exists, join, dirname


# 电影列表
@bp.route('/movies', methods=['GET'])
def movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.order_by(Movie.show_time.desc()).paginate(page, 10, False)
    next_url = url_for('management.movies', page=movies.next_num) if movies.has_next else None
    prev_url = url_for('management.movies', page=movies.prev_num) if movies.has_prev else None
    return render_template("movie/movies.html", movies=movies.items, next_url=next_url, prev_url=prev_url)


# 电影院列表：新增、修改、删除电影院
@bp.route('/cinemas', methods=['GET', 'POST'])
def cinemas():
    modify_form = MovieCinemaModifyForm()
    delete_form = MovieDeleteForm()
    create_form = MovieCinemaCreateForm()
    dict_cinema = {}

    page = request.args.get('page', 1, type=int)
    cinemas = MovieCinema.query.order_by(desc(MovieCinema.movie_cnt)).paginate(page, 10, False)

    if request.method == "GET":
        if current_user.is_authenticated and current_user.is_admin:
            if (not modify_form.submit.data) and (not delete_form.delete_submit.data) and (not create_form.add_submit.data):
                dict_cinema = get_dict_cinema(cinemas)

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if modify_form.submit.data and modify_form.is_submitted():
                if modify_form.validate():
                    return function_cinema_modify(modify_form)
                else:
                    dict_cinema = get_dict_cinema(cinemas)
                    flash_form_errors(modify_form)
                    dict_cinema[int(modify_form.id.data)] = modify_form
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                return function_cinema_delete(delete_form)
            if create_form.add_submit.data and create_form.is_submitted():
                if create_form.validate():
                    return function_cinema_create(create_form)
                else:
                    flash_form_errors(create_form)
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.cinemas"))
    next_url = url_for('management.cinemas', page=cinemas.next_num) if cinemas.has_next else None
    prev_url = url_for('management.cinemas', page=cinemas.prev_num) if cinemas.has_prev else None
    return render_template("movie/cinemas.html", cinemas=cinemas.items, next_url=next_url, prev_url=prev_url,
                           modify_form=modify_form, delete_form=delete_form, create_form=create_form, dict_cinema=dict_cinema)

# 电影类型列表：新增、修改、删除电影类型
@bp.route('/movie_types', methods=['GET', 'POST'])
def movie_types():
    movie_type_create_form = MovieTypeForm()
    movie_type_modify_form = MovieTypeModifyForm()
    delete_form = MovieDeleteForm()
    page = request.args.get('page', 1, type=int)
    types = MovieType.query.order_by(desc(MovieType.movie_cnt)).paginate(page, 10, False)
    list_modify_form = {}

    if request.method == "GET":
        if current_user.is_authenticated and current_user.is_admin:
            if (not movie_type_create_form.movie_type_add_submit.data) and (not movie_type_modify_form.movie_type_modify_submit.data):
                list_modify_form = get_dict_movie_type(types)

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if movie_type_create_form.movie_type_add_submit.data and movie_type_create_form.is_submitted():
                if movie_type_create_form.validate():
                    return function_movie_type_add(movie_type_create_form)
                else:
                    flash_form_errors(movie_type_create_form)
            if movie_type_modify_form.movie_type_modify_submit.data and movie_type_modify_form.is_submitted():
                if movie_type_modify_form.validate():
                    return function_movie_type_modify(movie_type_modify_form)
                else:
                    flash_form_errors(movie_type_modify_form)
                    list_modify_form = get_dict_movie_type(types)
                    list_modify_form[int(movie_type_modify_form.id.data)] = movie_type_modify_form
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                current_type = MovieType.query.filter_by(id=int(delete_form.id.data)).first()
                db.session.delete(current_type)
                flash("成功删除电影类型<"+current_type.name+">")
                return redirect(url_for("management.movie_types"))
        else:
            flash("您不是超级管理员，无法进行电影类型数据的管理")
            return redirect(url_for("management.movie_types"))


    next_url = url_for('management.movie_types', page=types.next_num) if types.has_next else None
    prev_url = url_for('management.movie_types', page=types.prev_num) if types.has_prev else None
    return render_template("movie/types.html", types=types.items, next_url=next_url, prev_url=prev_url,
                           movie_type_create_form=movie_type_create_form,
                           delete_form=delete_form,
                           list_modify_form=list_modify_form)


# 修改电影院信息
def function_cinema_modify(modify_form):
    current_cinema_id = int(modify_form.id.data)
    current_cinema = MovieCinema.query.filter_by(id=current_cinema_id).first()
    is_modify = False
    if current_cinema.name != str(modify_form.name.data).strip():
        current_cinema.name = str(modify_form.name.data).strip()
        is_modify = True
    if  current_cinema.address != str(modify_form.address.data).strip():
        current_cinema.address = str(modify_form.address.data).strip()
        is_modify = True
    if is_modify:
        flash("修改成功！")
    else:
        flash("没有任何修改！")
    return redirect(url_for("management.cinemas"))

# 删除电影院信息
def function_cinema_delete(delete_form):
    to_delete_cinema = MovieCinema.query.filter_by(id=int(delete_form.id.data)).first()
    db.session.delete(to_delete_cinema)
    flash("删除成功！")
    return redirect(url_for("management.cinemas"))

# 添加电影院信息
def function_cinema_create(create_form):
    to_add = MovieCinema(
        name=str(create_form.name.data).strip(),
        address=str(create_form.address.data).strip()
    )
    db.session.add(to_add)
    flash("成功添加电影院《" + create_form.name.data + "》")
    return redirect(url_for("management.cinemas"))


# 添加电影类型
def function_movie_type_add(create_form):
    to_add = MovieType(
        name=str(create_form.name.data).strip()
    )
    db.session.add(to_add)
    flash("添加《" + str(create_form.name.data).strip() + "》成功")
    return redirect(url_for("management.movie_types"))

# 修改电影类型
def function_movie_type_modify(movie_type_modify_form):
    current_type = MovieType.query.filter_by(id=int(movie_type_modify_form.id.data)).first()
    if current_type.name == str(movie_type_modify_form.name.data).strip():
        flash("无任何修改！")
    else:
        current_type.name = str(movie_type_modify_form.name.data).strip()
        flash("修改成功")
    return redirect(url_for("management.movie_types"))

# 给电影添加类型
def function_movie_add_type(movie_type_select_form, current_movie):
    result = current_movie.update_type_by_list_type_id(movie_type_select_form.list_select.data)
    if result:
        flash(result)
    else:
        flash("电影类型没有发生变化")
    return redirect(url_for("management.movie", id=current_movie.id))

# 给电影添加类型
def function_movie_add_actor(movie_actor_select_form, current_movie):
    result = current_movie.update_actor_by_list_actor_id(movie_actor_select_form.list_select.data)
    if result:
        flash(result)
    else:
        flash("电影演员没有发生变化")
    return redirect(url_for("management.movie", id=current_movie.id))

# 打印错误信息
def flash_form_errors(form):
    for current_error_key in list(form.errors.keys()):
        for current_error in form.errors[current_error_key]:
            flash(current_error)


# 显示电影详情
@bp.route('/movie/<id>', methods=['GET', 'POST'])
def movie(id):
    movie_type_select_form = MovieTypeSelectForm()
    movie_actor_select_form = MovieActorSelectForm()
    current_movie = Movie.query.filter_by(id=id).first()
    list_types = current_movie.types
    list_type_id = [int(x.id) for x in list_types]
    list_actors = current_movie.actors
    list_actor_id = [int(x.id) for x in list_actors]

    upload_image_form = LinkForm()
    upload_image_form.id.data = int(id)

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if movie_type_select_form.movie_type_select_submit.data and movie_type_select_form.is_submitted():
                if movie_type_select_form.validate():
                    return function_movie_add_type(movie_type_select_form, current_movie)
                else:
                    flash_form_errors(movie_type_select_form)
            if upload_image_form.file_submit.data and upload_image_form.validate_on_submit():
                file_link = upload_image_form.file_select.data
                if (file_link is not None) and (len(str(file_link).strip()) > 0):
                    f = urllib_request.urlopen(file_link)
                    data = f.read()
                    current_file_type = get_file_type(file_link)
                    file_name = 'static/images/movies/' + str(upload_image_form.id.data) + "." + current_file_type
                    file_path = join(current_app.root_path, file_name)
                    folder_path = dirname(file_path)
                    if not exists(folder_path):
                        makedirs(folder_path)
                    if exists(file_path):
                        remove(file_path)
                    with open(file_path, "wb") as code:
                        code.write(data)
                    current_movie = Movie.query.get(int(upload_image_form.id.data))
                    current_movie.bill_link = "/" + file_name
                    flash("电影海报上传成功")
                return redirect(url_for("management.movie", id=id))
        if movie_actor_select_form.movie_actor_select_submit.data and movie_actor_select_form.is_submitted():
            if movie_actor_select_form.validate():
                return function_movie_add_actor(movie_actor_select_form, current_movie)
            else:
                flash_form_errors(movie_actor_select_form)
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.movie", id=id))
    if current_user.is_authenticated and current_user.is_admin:
        movie_type_select_form.list_select.data = list_type_id
        movie_actor_select_form.list_select.data = list_actor_id

    return render_template("movie/movie.html", movie=current_movie,
                           movie_type_select_form=movie_type_select_form,
                           upload_image_form=upload_image_form,
                           movie_actor_select_form=movie_actor_select_form)


# 新增电影
@bp.route('/movie/add', methods=['GET', 'POST'])
@login_required
def movie_add():
    if not current_user.is_admin:
        flash("您不是超级管理员，无法进行电影数据的管理")
        return redirect(url_for("management.movies"))

    movie_form = MovieForm()
    if request.method =="GET":
        movie_form.watch_time.data = datetime.utcnow().date()

    if movie_form.validate_on_submit():
        to_add = Movie(
            name=str(movie_form.name.data).strip(),
            show_time=movie_form.show_time.data,
            film_length=movie_form.film_length.data,
            bill_link=str(movie_form.bill_link.data).strip(),
            is_watched=movie_form.is_watched.data,
            description=str(movie_form.description.data).strip(),
            cinema_id=int(movie_form.cinema_id.data),
            country_id=int(movie_form.country_id.data)
        )
        if movie_form.is_watched.data:
            to_add.watch_time = movie_form.watch_time.data
        db.session.add(to_add)
        flash("成功添加电影《" + movie_form.name.data + "》")
        return redirect(url_for("management.movies"))
    return render_template("movie/movie_add.html", movie_form=movie_form)


# 修改电影
@bp.route('/movie/modify/<id>', methods=['GET', 'POST'])
@login_required
def movie_modify(id):
    if not current_user.is_admin:
        flash("您不是超级管理员，无法进行电影数据的管理")
        return redirect(url_for("management.movies"))

    movie_form = MovieModifyForm()
    current_movie = Movie.query.filter_by(id=id).first()
    if request.method =="GET":
        movie_form.name.data = current_movie.name
        movie_form.show_time.data = current_movie.show_time
        movie_form.film_length.data = current_movie.film_length
        movie_form.bill_link.data = current_movie.bill_link
        movie_form.is_watched.data = current_movie.is_watched
        if current_movie.is_watched:
            movie_form.watch_time.data = datetime.utcnow().date()
        movie_form.description.data = current_movie.description
        movie_form.cinema_id.data = current_movie.cinema_id
        movie_form.country_id.data = current_movie.country_id

    if movie_form.validate_on_submit():
        if movie_form.name.data != current_movie.name:
            current_movie.name = str(movie_form.name.data).strip()
        if movie_form.show_time.data != current_movie.show_time:
            current_movie.show_time = movie_form.show_time.data
        if movie_form.film_length.data != current_movie.film_length:
            current_movie.film_length = movie_form.film_length.data
        if movie_form.bill_link.data != current_movie.bill_link:
            current_movie.bill_link = str(movie_form.bill_link.data).strip()
        if movie_form.is_watched.data != current_movie.is_watched:
            current_movie.is_watched = movie_form.is_watched.data
        if movie_form.is_watched.data:
            movie_form.is_watched.render_kw = {"checked": "checked"}
            if movie_form.watch_time.data != current_movie.watch_time:
                current_movie.watch_time = movie_form.watch_time.data
        if movie_form.description.data != current_movie.description:
            current_movie.description = str(movie_form.description.data).strip()
        if movie_form.cinema_id.data != current_movie.cinema_id:
            current_movie.cinema_id = movie_form.cinema_id.data
        if movie_form.country_id.data != current_movie.country_id:
            current_movie.country_id = movie_form.country_id.data
        flash("成功修改电影《" + movie_form.name.data + "》")
        return redirect(url_for("management.movie", id=id))
    return render_template("movie/movie_add.html", movie_form=movie_form)


# 在电影类别列表中生成各个电影类别的修改表单
def get_dict_movie_type(types):
    list_modify_form = {}
    for current_type in types.items:
        new_modify_form = MovieTypeModifyForm()
        new_modify_form.id.data = current_type.id
        new_modify_form.name.data = current_type.name
        list_modify_form[current_type.id] = new_modify_form
    return list_modify_form


# 在电影院列表中生成各个电影院的修改表单
def get_dict_cinema(cinemas):
    dict_cinema = {}
    for current_cinema in cinemas.items:
        current_modify_form = MovieCinemaModifyForm()
        current_modify_form.id.data = current_cinema.id
        current_modify_form.name.data = current_cinema.name
        current_modify_form.address.data = current_cinema.address
        dict_cinema[current_cinema.id] = current_modify_form
    return dict_cinema