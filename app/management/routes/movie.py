# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:25
# IDE：PyCharm

from app import db
from app.management import bp
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from app.models.movie import Movie, MovieCinema
from app.management.forms.movie import MovieForm, MovieCinemaForm
from datetime import datetime


# 电影列表
@bp.route('/movies', methods=['GET'])
def movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page, 15, False)
    next_url = url_for('management.movies', page=movies.next_num) if movies.has_next else None
    prev_url = url_for('management.movies', page=movies.prev_num) if movies.has_prev else None
    return render_template("movie/movies.html", movies=movies.items, next_url=next_url, prev_url=prev_url)


# 电影列表
@bp.route('/cinemas', methods=['GET'])
def cinemas():
    page = request.args.get('page', 1, type=int)
    cinemas = MovieCinema.query.paginate(page, 15, False)
    next_url = url_for('management.cinemas', page=cinemas.next_num) if cinemas.has_next else None
    prev_url = url_for('management.cinemas', page=cinemas.prev_num) if cinemas.has_prev else None
    return render_template("movie/cinemas.html", cinemas=cinemas.items, next_url=next_url, prev_url=prev_url)


# 显示电影详情
@bp.route('/movie/<id>', methods=['GET', 'POST'])
def movie(id):
    current_movie = Movie.query.filter_by(id=id).first()
    return render_template("movie/movie.html", movie=current_movie)


# 新增电影院
@bp.route('/cinema/add', methods=['GET', 'POST'])
@login_required
def cinema_add():
    if not current_user.is_admin:
        flash("您不是超级管理员，无法进行电影院数据的管理")
        return redirect(url_for("management.cinemas"))
    cinema_form = MovieCinemaForm()
    if cinema_form.is_submitted():
        if cinema_form.validate():
            to_add = MovieCinema(
                name = str(cinema_form.name.data).strip(),
                address = str(cinema_form.address.data).strip()
            )
            db.session.add(to_add)
            flash("成功添加电影院《"+cinema_form.name.data+"》")
            return redirect(url_for("management.cinemas"))
        else:
            first_key = list(cinema_form.errors.keys())[0]
            flash(cinema_form.errors[first_key])
    return render_template("movie/cinema_add.html", cinema_form=cinema_form)


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

    if movie_form.is_submitted():
        if movie_form.validate():
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
        else:
            first_key = list(movie_form.errors.keys())[0]
            flash(movie_form.errors[first_key])
    return render_template("movie/movie_add.html", movie_form=movie_form)
