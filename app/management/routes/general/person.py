# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/6 17:24
# IDE：PyCharm

from datetime import datetime

from flask import request, url_for, render_template, flash, redirect
from flask_login import current_user

from app import db
from app.management import bp
from app.management.forms.movie import MovieDeleteForm
from app.management.forms.person import PersonCreateForm, PersonModifyForm
from app.management.routes.entertainment.movie import flash_form_errors
from app.models.person import Person


@bp.route('/persons', methods=['GET', 'POST'])
def persons():
    add_form = PersonCreateForm()
    m_form = PersonModifyForm()
    delete_form = MovieDeleteForm()
    modify_error_form = None

    if request.method == "POST":
        if current_user.is_authenticated and current_user.is_admin:
            if add_form.person_add_submit.data and add_form.is_submitted():
                if add_form.validate():
                    add_person(add_form)
                    flash("成功添加人物《"+str(add_form.name.data).strip()+"》")
                    return redirect(url_for("management.persons"))
                else:
                    flash_form_errors(add_form)
            if m_form.person_modify_submit.data and m_form.is_submitted():
                if m_form.validate():
                    return modify_person(m_form)
                else:
                    modify_error_form = m_form
                    flash_form_errors(modify_error_form)
            if delete_form.delete_submit.data and delete_form.validate_on_submit():
                return remove_person(delete_form)
        else:
            flash("您不是超级管理员，无法进行电影院数据的管理")
            return redirect(url_for("management.cinemas"))

    page = request.args.get('page', 1, type=int)
    persons = Person.query.paginate(page, 10, False)

    modify_form = {}
    for current_item in persons.items:
        modify_form[current_item.id] = reform_person_modify_form(current_item)

    if modify_error_form is not None:
        modify_form[int(modify_error_form.id.data)] = modify_error_form

    next_url = url_for('management.persons', page=persons.next_num) if persons.has_next else None
    prev_url = url_for('management.persons', page=persons.prev_num) if persons.has_prev else None
    return render_template("general/persons.html", items=persons.items, next_url=next_url, prev_url=prev_url,
                           add_form=add_form,
                           modify_form=modify_form,
                           delete_form=delete_form,
                           create_label="添加人物",
                           modify_label="修改人物信息",
                           delete_label="您確认要删除该人物吗？")


# 重新构造SELECT表单
def reform_select(model_data, default=0):
    if model_data:
        return model_data
    else:
        return default


# 重新构造修改表单，将以前的信息重新填进菜单中
def reform_person_modify_form(current_item):
    temp_modify_form = PersonModifyForm()
    temp_modify_form.id.data = current_item.id
    temp_modify_form.name.data = current_item.name
    temp_modify_form.foreign_name.data = current_item.foreign_name
    temp_modify_form.bill_link.data = current_item.bill_link
    if (current_item.sex == 0) or (current_item.sex == 1):
        temp_modify_form.sex.data = current_item.sex
    else:
        temp_modify_form.sex.data = 2
    temp_modify_form.birth_day.data = current_item.birth_day
    temp_modify_form.nationality_id.data = reform_select(current_item.nationality_id)
    temp_modify_form.birth_city_id.data = reform_select(current_item.birth_city_id)
    temp_modify_form.origin_city_id.data = reform_select(current_item.origin_city_id)
    temp_modify_form.constellation_id.data = reform_select(current_item.constellation_id)
    temp_modify_form.blood_group_id.data = reform_select(current_item.blood_group_id)
    temp_modify_form.weight.data = reform_select(current_item.weight)
    temp_modify_form.height.data = reform_select(current_item.height)
    return temp_modify_form


# 添加新人物
def add_person(add_form):
    to_add = Person(name=str(add_form.name.data).strip(),
                    create_time=datetime.now(),
                    update_time=datetime.now())
    if (not add_form.birth_day.data is None) and (len(str(add_form.birth_day.data).strip())>0):
        to_add.birth_day = add_form.birth_day.data
    if add_form.sex.data < 2:
        to_add.sex = add_form.sex.data
    if (not add_form.foreign_name.data is None) and (len(str(add_form.foreign_name.data).strip())>0):
        to_add.foreign_name = str(add_form.foreign_name.data).strip()
    if (not add_form.bill_link.data is None) and (len(str(add_form.bill_link.data).strip())>0):
        to_add.bill_link = str(add_form.bill_link.data).strip()
    if add_form.nationality_id.data > 0:
        to_add.nationality_id = add_form.nationality_id.data
    if add_form.birth_city_id.data > 0:
        to_add.birth_city_id = add_form.birth_city_id.data
    if add_form.origin_city_id.data > 0:
        to_add.origin_city_id = add_form.origin_city_id.data
    if add_form.constellation_id.data > 0:
        to_add.constellation_id = add_form.constellation_id.data
    if add_form.blood_group_id.data > 0:
        to_add.blood_group_id = add_form.blood_group_id.data
    if add_form.height.data > 0:
        to_add.height = add_form.height.data
    if add_form.weight.data > 0:
        to_add.weight = add_form.weight.data
    db.session.add(to_add)


# 修改人物
def modify_person(m_form):
    is_modified = False
    temp_modi_form = PersonModifyForm()
    current_person = Person.query.filter_by(id=int(m_form.id.data)).first()
    information = []
    if m_form.name.data != current_person.name:
        if (not m_form.name.data is None) and (len(str(m_form.name.data).strip()) > 0):
            information.append("名字从《" + str(current_person.name) + "》变为《" + str(m_form.name.data) + "》")
            current_person.name = m_form.name.data
            is_modified = True


    change_number = None
    if (not m_form.birth_day.data is None) and (len(str(m_form.birth_day.data).strip()) > 0):
        change_number = str(m_form.birth_day.data).strip()
    original_number = None
    if (not current_person.birth_day is None) and (len(str(current_person.birth_day).strip()) > 0):
        original_number = str(current_person.birth_day).strip()
    if change_number != original_number:
        information.append("出生生日从《" + str(current_person.birth_day) + "》变为《" + str(change_number) + "》")
        current_person.birth_day = change_number
        is_modified = True

    change_number = None
    if m_form.sex.data < 2:
        change_number = m_form.sex.data
    if change_number != current_person.sex:
        information.append("性别从《" + str(current_person.sex) + "》变为《" + str(change_number) + "》")
        is_modified = True
        current_person.sex = change_number

    change_number = None
    str(m_form.bill_link.data).strip()
    if (not m_form.bill_link.data is None) and (len(str(m_form.bill_link.data).strip()) > 0):
        change_number = str(m_form.bill_link.data).strip()
    if change_number != current_person.bill_link:
        information.append("海报链接从《" + str(current_person.bill_link) + "》变为《" + str(change_number) + "》")
        current_person.bill_link = change_number
        is_modified = True

    change_number = None
    str(m_form.foreign_name.data).strip()
    if (not m_form.foreign_name.data is None) and (len(str(m_form.foreign_name.data).strip()) > 0):
        change_number = str(m_form.foreign_name.data).strip()
    if change_number != current_person.foreign_name:
        information.append("外语名从《" + str(current_person.foreign_name) + "》变为《" + str(change_number) + "》")
        current_person.foreign_name = change_number
        is_modified = True

    change_number = None
    nationality_name = "None"
    if int(m_form.nationality_id.data) > 0:
        change_number = int(m_form.nationality_id.data)
        if current_person.nationality is not None:
            nationality_name = current_person.nationality.name
    if change_number != current_person.nationality_id:
        information.append("国籍从《" + str(nationality_name) + "》变为《" \
                           + str(temp_modi_form.nationality_id.choices[int(m_form.nationality_id.data)][1]) + "》")
        current_person.nationality_id = change_number
        is_modified = True

    change_number = None
    birth_city_name = "None"
    if int(m_form.birth_city_id.data) > 0:
        change_number = int(m_form.birth_city_id.data)
        if current_person.birth_city is not None:
            birth_city_name = current_person.birth_city.name
    if change_number != current_person.birth_city_id:
        information.append("出生地从《" + str(birth_city_name) + "》变为《" \
                           + str(
            temp_modi_form.birth_city_id.choices[int(m_form.birth_city_id.data)][1]) + "》")
        current_person.birth_city_id = change_number
        is_modified = True

    change_number = None
    origin_city_name = "None"
    if int(m_form.origin_city_id.data) > 0:
        change_number = int(m_form.origin_city_id.data)
        if current_person.origin_city is not None:
            origin_city_name = current_person.origin_city.name
    if change_number != current_person.origin_city_id:
        information.append("籍贯地从《" + str(origin_city_name) + "》变为《" \
                           + str(
            temp_modi_form.origin_city_id.choices[int(m_form.origin_city_id.data)][1]) + "》")
        current_person.origin_city_id = change_number
        is_modified = True

    change_number = None
    constellation_name = "None"
    if int(m_form.constellation_id.data) > 0:
        change_number = int(m_form.constellation_id.data)
        if current_person.constellation is not None:
            constellation_name = current_person.constellation.name
    if change_number != current_person.constellation_id:
        information.append("星座从《" + str(constellation_name) + "》变为《" \
                           + str(
            temp_modi_form.constellation_id.choices[int(m_form.constellation_id.data)][1]) + "》")
        current_person.constellation_id = change_number
        is_modified = True

    change_number = None
    blood_group_name = "None"
    if int(m_form.blood_group_id.data) > 0:
        change_number = int(m_form.blood_group_id.data)
        if current_person.blood_group is not None:
            blood_group_name = current_person.blood_group.name
    if change_number != current_person.blood_group_id:
        information.append("血型从《" + str(blood_group_name) + "》变为《" \
                           + str(
            temp_modi_form.blood_group_id.choices[int(m_form.blood_group_id.data)][1]) + "》")
        current_person.blood_group_id = change_number
        is_modified = True

    change_number = None
    if float(m_form.height.data) > 0:
        change_number = float(m_form.height.data)
    original_number = None
    if not current_person.height is None:
        original_number = float(current_person.height)
    if change_number != original_number:
        information.append("身高从《" + str(current_person.height) + "》变为《" \
                           + str(change_number) + "》")
        current_person.height = change_number
        is_modified = True

    change_number = None
    if float(m_form.weight.data) > 0:
        change_number = float(m_form.weight.data)
    original_number = None
    if not current_person.weight is None:
        original_number = float(current_person.weight)
    if change_number != original_number:
        information.append("体重从《" + str(current_person.weight) + "》变为《" \
                           + str(change_number) + "》")
        current_person.weight = change_number
        is_modified = True

    if is_modified:
        information = "、".join(information)
        current_person.update_time = datetime.now()
        flash("修改成功：" + str(information).strip())
    else:
        flash("毫无任何修改")
    return redirect(url_for("management.persons"))


# 删除人物
def remove_person(delete_form):
    current_person = Person.query.filter_by(id=int(delete_form.id.data)).first()
    current_person_name = current_person.name
    db.session.delete(current_person)
    flash("成功删除《" + str(current_person_name) + "》")
    return redirect(url_for("management.persons"))