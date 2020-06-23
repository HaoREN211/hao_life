# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/23 16:07
# IDE：PyCharm

from app.management import bp
from flask import render_template, request
from app.management.forms.work.tools import TimestampForm
from app.management.routes.entertainment.movie import flash_form_errors
import datetime as dt

# 时间戳转时间
@bp.route('/timestamp_to_datetime', methods=['GET', 'POST'])
def timestamp_to_datetime():
    form = TimestampForm()
    result = None
    if request.method == "POST":
        if form.create_submit.data and form.is_submitted():
            if not form.validate():
                flash_form_errors(form)
            else:
                result = dt.datetime.fromtimestamp(int(form.timestamp.data)*1.0/1000.0).strftime("%Y-%m-%d %H:%M:%S")
    return render_template("work/timestamp_to_datetime.html", title="时间戳转时间", result=result, form=form)