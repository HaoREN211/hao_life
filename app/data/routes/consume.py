# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/25 20:49
# IDE：PyCharm

from app.data import bp
from json import dumps

# 雷达图，各消费方式的花费统计
@bp.route('/consume_by_type', methods=['POST', 'GET'])
def consume_by_type():
    string = ('{"types": [{name: "交通出行", max: 2100, min: 0},'
                + '{name: "休闲娱乐", max: 2100, min: 0},'
                + '{name: "党费缴纳", max: 2100, min: 0},'
                + '{name: "其他", max: 2100, min: 0},'
                + '{name: "文体教育", max: 2100, min: 0},'
                + '{name: "日常缴费", max: 2100, min: 0},'
                + '{name: "生活日用", max: 2100, min: 0},'
                + '{name: "通讯物流", max: 2100, min: 0},'
                + '{name: "金融保险", max: 2100, min: 0},'
                + '{name: "餐饮美食", max: 2100, min: 0}], "data": [100.22, 91.80, 100.00, 30.52, 354.40, 234.30, 1124.38, 20.00, 108.45, 2045.03]}')
    return dumps(string)