# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/8 15:27
# IDE：PyCharm

import re
from urllib.request import urlopen


def save_pic_from_url(url, path):
    try:
        img_content = urlopen(url).read()
    except:
        print(url + "找不到源文件")
    else:
        f = open(path, 'wb+')
        f.write(img_content)
        f.close()


def get_file_type(file_name):
    return str(file_name).rsplit('.', 1)[1]


def get_standard_name(new_name):
    return str(new_name).strip() if (
        (new_name is not None) and len(str(new_name).strip()) > 0) else None


# 从datetime中重建构造datetime_local所需要的的格式
def reform_datetime_local_with_datetime(datetime):
    result = str(datetime.year)
    result += "-"+add_zero_for_month_day_hour_minute(datetime.month)
    result  += "-"+add_zero_for_month_day_hour_minute(datetime.day)
    result += "T" + add_zero_for_month_day_hour_minute(datetime.hour)
    result += ":" + add_zero_for_month_day_hour_minute(datetime.minute)
    return result


# 如果月日时分秒只有一位数字，则给它前面加一个0
def add_zero_for_month_day_hour_minute(time_unit):
    if len(str(time_unit)) == 1:
        time_unit = "0"+str(time_unit)
    return str(time_unit)


# 获取文件类型
def get_file_type(file_name):
    return str(file_name).rsplit('.', 1)[1]


# 字符串是否是时间戳
def is_timestamp(string):
    pattern = re.compile("^[1-2][0-9]{3}-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")
    if pattern.match(str(string).strip()):
        return True
    return False

def is_date(string):
    pattern = re.compile("^[1-2][0-9]{3}-[01][0-9]-[0-3][0-9]$")
    if pattern.match(str(string).strip()):
        return True
    return False


# 根据贷款年限主键，返回贷款期限
# year=False时返回月数，year=True时返回年数
def get_loan_duration(loan_duration, year = False):
    base = 12 if year == False else 1
    return int(loan_duration)*10*base


# 根据贷款金额、贷款利率、贷款月数计算等额本息贷款额度明细
def get_loan_repay_info_dengebenxi(loan_amount, loan_tax, loan_duration):
    # 根据年利率计算月利率，因为是百分制计数还要除以100
    loan_tax_month = float(loan_tax)/1200
    # 根据下拉菜单选择loan_duration，1代表10年，2代表20年，3代表30年
    loan_month = get_loan_duration(loan_duration)

    sub_equation = (1.0 + loan_tax_month)**loan_month

    # 还款本金本金
    principal = int(loan_amount)*10000

    # 计算每月还款总额
    repay_amount_per_month = round((float(principal*float(loan_tax_month) *sub_equation)/float(sub_equation-1.0)), 2)

    # 还款总金额
    repay_amount_total = round(repay_amount_per_month * loan_month, 2)

    # 还款利息
    interest = round(repay_amount_total - principal, 2)

    # 累计已还本金
    repaid_principal = 0

    # 每月还款明细
    month_details = []
    for i in range(loan_month):
        current_interest = round((principal - repaid_principal)*loan_tax_month, 2)
        current_principal = round(repay_amount_per_month - current_interest, 2)
        month_details.append({
            "number": i+1,
            "amount": repay_amount_per_month,
            "principal": current_principal,
            "interest": current_interest
        })
        repaid_principal = round(repaid_principal+current_principal, 2)


    return {
        "repay_amount_total": repay_amount_total,
        "repay_amount_per_month": repay_amount_per_month,
        "principal": principal,
        "interest": interest,
        "details": month_details
    }

# 合并商贷和公积金贷款的额度
def merge_commercial_and_fund_loan_repay_details(first_repay_detail, second_repay_detail):
    month_details = []
    for i in range(len(first_repay_detail["details"])):
        month_details.append({
            "number": i+1,
            "amount": round(first_repay_detail["details"][i]["amount"] + second_repay_detail["details"][i]["amount"], 2),
            "amount_fund": first_repay_detail["details"][i]["amount"],
            "amount_commercial": second_repay_detail["details"][i]["amount"],
            "principal": round(first_repay_detail["details"][i]["principal"] + second_repay_detail["details"][i]["principal"], 2),
            "principal_fund": first_repay_detail["details"][i]["principal"],
            "principal_commercial": second_repay_detail["details"][i]["principal"],
            "interest": round(first_repay_detail["details"][i]["interest"] + second_repay_detail["details"][i]["interest"], 2),
            "interest_fund": first_repay_detail["details"][i]["interest"],
            "interest_commercial": second_repay_detail["details"][i]["interest"],
        })
    return {
        "repay_amount_total": round(first_repay_detail["repay_amount_total"]+second_repay_detail["repay_amount_total"], 2),
        "repay_amount_total_fund": first_repay_detail["repay_amount_total"],
        "repay_amount_total_commercial": second_repay_detail["repay_amount_total"],
        "repay_amount_per_month": round(first_repay_detail["repay_amount_per_month"] + second_repay_detail["repay_amount_per_month"], 2),
        "principal": round(first_repay_detail["principal"] + second_repay_detail["principal"], 2),
        "principal_fund": first_repay_detail["principal"],
        "principal_commercial": second_repay_detail["principal"],
        "interest": round(first_repay_detail["interest"] + second_repay_detail["interest"], 2),
        "interest_fund": first_repay_detail["interest"],
        "interest_commercial": second_repay_detail["interest"],
        "details": month_details
    }