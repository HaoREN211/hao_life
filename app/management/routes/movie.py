# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/4 15:25
# IDE：PyCharm

from app import db
from app.management import bp
from flask import render_template, request, flash, url_for, redirect
from app.models.movie import Movie
from app.management.forms.movie import MovieForm
from datetime import datetime


# 电影列表
@bp.route('/movies', methods=['GET'])
def movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page, 15, False)
    next_url = url_for('management.movies', page=movies.next_num) if movies.has_next else None
    prev_url = url_for('management.movies', page=movies.prev_num) if movies.has_prev else None
    return render_template("movie/movies.html", movies=movies.items, next_url=next_url, prev_url=prev_url)


# 显示电影详情
@bp.route('/movie/<id>', methods=['GET', 'POST'])
def movie(id):
    current_movie = Movie.query.filter_by(id=id).first()
    return render_template("movie/movie.html", movie=current_movie)


# 新增电影
@bp.route('/movie/add', methods=['GET', 'POST'])
def movie_add():
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
                description=str(movie_form.description.data).strip()
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
