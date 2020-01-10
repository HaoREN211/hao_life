# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/26 9:04
# IDE：PyCharm
from app import db
from flask import redirect, url_for, flash
from datetime import datetime
from app.management.forms.estate import EstateModifyForm, BuildingTypeModifyForm, BuildingPropertyModifyForm, BuildingModifyForm

# 重新构造修改的表单
def modify_form_constructor(items, temp_form):
    list_modify_form = {}
    for current_item in items.items:

        if temp_form == "EstateModifyForm":
            modify_form = EstateModifyForm()
        elif temp_form == "BuildingTypeModifyForm":
            modify_form = BuildingTypeModifyForm()
        elif temp_form == "BuildingPropertyModifyForm":
            modify_form = BuildingPropertyModifyForm()
        elif temp_form == "BuildingModifyForm":
            modify_form = BuildingModifyForm()

        for current_key in modify_form.__dict__.keys():
            if str(current_key).startswith("_"):
                continue
            elif str(current_key).startswith("validate_"):
                continue
            elif not str(current_key) in current_item.__dict__.keys():
                continue
            elif str(current_key).endswith("_id"):
                target_id = current_item.__getattribute__(current_key)
                target_id = 0 if target_id is None else target_id
                modify_form.__getattribute__(current_key).data = target_id
            else:
                modify_form.__getattribute__(current_key).data = current_item.__getattribute__(current_key)
        list_modify_form[current_item.id] = modify_form
    return list_modify_form

# 根据修改的form修改数据库数据
def modify_db(modify_form, db_model, url):
    current_item = db_model.query.filter_by(id=int(modify_form.id.data)).first()
    is_modified = False

    for current_key in modify_form.__dict__.keys():
        if str(current_key).startswith("_"):
            continue
        elif str(current_key) in ["modify_submit", "cancel", "meta", "csrf_token", "id"]:
            continue
        elif str(current_key).startswith("validate_"):
            continue
        elif not str(current_key) in current_item.__dict__.keys():
            continue
        elif str(current_key).endswith("_id"):
            target_id = modify_form.__getattribute__(current_key).data
            target_id = target_id if target_id > 0 else None
            if current_item.__getattribute__(current_key) != target_id:
                is_modified = True
                current_item.__setattr__(current_key, target_id)
        else:
            if current_item.__getattribute__(current_key) != modify_form.__getattribute__(current_key).data:
                is_modified = True
                current_item.__setattr__(current_key, modify_form.__getattribute__(current_key).data)
    if is_modified:
        if "update_time" in current_item.__dict__.keys():
            current_item.__setattr__("update_time", datetime.now())
        flash("修改成功")
    else:
        flash("毫无任何修改")
    return redirect(url_for(url))

# 根据add_form创建数据
def create_db_row(add_form, db_table, url):
    for current_key in add_form.__dict__.keys():
        if str(current_key).startswith("_"):
            continue
        elif str(current_key) in ["create_submit", "cancel", "meta", "csrf_token"]:
            continue
        elif str(current_key).endswith("_id"):
            target_id = int(add_form.__getattribute__(current_key).data)
            target_id = target_id if target_id > 0 else None
            db_table.__setattr__(current_key, target_id)
        else:
            db_table.__setattr__(current_key, add_form.__getattribute__(current_key).data)
    db.session.add(db_table)
    flash("添加成功")
    return redirect(url_for(url))
