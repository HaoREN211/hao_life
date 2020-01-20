# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 9:40
# IDE：PyCharm

from flask import render_template, flash
from app.management import bp
from app.models.country import Constellation
from app.management.routes.entertainment.movie import flash_form_errors
from app.management.forms.time import SingleTimeForm


# 星座列表
@bp.route('/constellations', methods=['GET', 'POST'])
def constellations():
    time_form = SingleTimeForm()
    constellations = Constellation.query.order_by().all()
    if time_form.date_submit.data and time_form.is_submitted():
        if not time_form.validate():
            flash_form_errors(time_form)
        else:
            search_time = time_form.date_field.data
            is_find = False
            id_10_name = None
            for current_constellation in constellations:
                if current_constellation.id == 10:
                    id_10_name = current_constellation.name
                    continue
                if ((current_constellation.start_time <= search_time)
                    and (current_constellation.end_time >=search_time)):
                    is_find = True
                    flash(str(search_time)+"是"+str(current_constellation.name))
            if not is_find:
                flash(str(search_time) + "是" + str(id_10_name))
    return render_template("general/constellations.html",
                           constellations=constellations,
                           time_form=time_form)