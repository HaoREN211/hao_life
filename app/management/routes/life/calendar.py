# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/6/11 10:27
# IDE：PyCharm

import datetime as dt
from app.management import bp
from flask import render_template, request
from copy import copy


# 程序员老黄历所需要的数据
class Data:
    weeks = ["日", "一", "二", "三", "四", "五", "六"]
    directions = ["北方", "东北方", "东方", "东南方", "南方", "西南方", "西方", "西北方"]
    tools =["Eclipse写程序", "MSOfice写文档", "记事本写程序", "Windows8", "Linux", "MacOS", "IE", "Android设备", "iOS设备"]
    varNames = ["jieguo", "huodong", "pay", "expire", "zhangdan", "every", "free", "i1", "a", "virtual", "ad", "spider", "mima", "pass", "ui"]
    drinks = ["水","茶","红茶","绿茶","咖啡","奶茶","可乐","鲜奶","豆奶","果汁","果味汽水","苏打水","运动饮料","酸奶","酒"]
    activities = [
        ("写单元测试", "写单元测试将减少出错", "写单元测试会降低你的开发效率", False),
        ("洗澡", "你几天没洗澡了？", "会把设计方面的灵感洗掉", True),
        ("锻炼一下身体", "", "能量没消耗多少，吃得却更多", True),
        ("抽烟", "抽烟有利于提神，增加思维敏捷", "除非你活够了，死得早点没关系", True),
        ("白天上线", "今天白天上线是安全的", "可能导致灾难性后果", False),
        ("重构", "代码质量得到提高", "你很有可能会陷入泥潭", False),
        ("使用%t", "你看起来更有品位", "别人会觉得你在装逼", False),
        ("跳槽", "该放手时就放手", "鉴于当前的经济形势，你的下一份工作未必比现在强", False),
        ("招人", "你面前这位有成为牛人的潜质", "这人会写程序吗？", False),
        ("面试", "面试官今天心情很好", "面试官不爽，会拿你出气", False),
        ("提交辞职申请", "公司找到了一个比你更能干更便宜的家伙，巴不得你赶快滚蛋", "鉴于当前的经济形势，你的下一份工作未必比现在强", False),
        ("申请加薪", "老板今天心情很好", "公司正在考虑裁员", False),
        ("晚上加班", "晚上是程序员精神最好的时候", "", True),
        ("在妹子面前吹牛", "改善你矮穷挫的形象", "会被识破", True),
        ("撸管", "避免缓冲区溢出", "强撸灰飞烟灭", True),
        ("浏览成人网站", "重拾对生活的信心", "你会心神不宁", True),
        ("命名变量%v", "", "", False),
        ("写超过%l行的方法", "你的代码组织的很好，长一点没关系", "你的代码将混乱不堪，你自己都看不懂", False),
        ("提交代码", "遇到冲突的几率是最低的", "你遇到的一大堆冲突会让你觉得自己是不是时间穿越了", False),
        ("代码复审", "发现重要问题的几率大大增加", "你什么问题都发现不了，白白浪费时间", False),
        ("开会", "写代码之余放松一下打个盹，有益健康", "小心被扣屎盆子背黑锅", False),
        ("打DOTA", "你将有如神助", "你会被虐的很惨", True),
        ("晚上上线", "晚上是程序员精神最好的时候", "你白天已经筋疲力尽了", False),
        ("修复BUG", "你今天对BUG的嗅觉大大提高", "新产生的BUG将比修复的更多", False),
        ("设计评审", "设计评审会议将变成头脑风暴", "人人筋疲力尽，评审就这么过了", False),
        ("需求评审", "", "", False),
        ("上微博", "今天发生的事不能错过", "今天的微博充满负能量", True),
        ("上AB站", "还需要理由吗？", "满屏兄贵亮瞎你的眼", True),
        ("玩FlappyBird", "今天破纪录的几率很高", "除非你想玩到把手机砸了", True)
    ]

# 程序员老黄历主体对象
class ProgrammerCalendar:
    date = None
    target_date_date = None
    target_date_int = None

    def __init__(self, date):
        self.date=date
        self.target_date_date = dt.datetime.strptime(self.date, "%Y-%m-%d")
        self.target_date_int = int(self.date.replace("-", ""))
        self.data = Data()

    # 本程序中的“随机”都是伪随机概念，以当前的天为种子。
    def random(self, seed=2):
        tmp_n = self.target_date_int%11117
        for tmp_i in range(100+seed):
            tmp_n = tmp_n**2
            tmp_n = tmp_n % 11117
        return tmp_n

    # 获取敲代码的朝向
    def get_direction(self):
        return self.data.directions[self.random()%len(self.data.directions)]

    # 获取今日最益喝的饮料
    def get_random_drinks(self, size=2):
        tmp_drinks = copy(self.data.drinks)
        for tmp_i in range(len(self.data.drinks)-size):
            tmp_drinks.pop(self.random(tmp_i) % len(tmp_drinks))
        return ",".join(tmp_drinks)

    # 女神亲近指数
    def get_star(self):
        return self.random(6)%5+1

    # 今日益做事项
    def get_today_luck(self):
        tmp_activities = copy(self.data.activities)
        day_of_week = int(self.target_date_date.strftime("%w"))
        # 如果是周末的话筛选出只有周末干的事儿
        if (day_of_week == 0) or (day_of_week == 6):
            tmp_activities = [tmp_activities[i] for i in range(len(tmp_activities)) if tmp_activities[i][3]]

        num_good = self.random(98) % 3 + 2
        num_bad = self.random(87) % 3 + 2

        num = num_good+num_bad
        for tmp_i in range(len(tmp_activities)-num):
            tmp_activities.pop(self.random(tmp_i) % len(tmp_activities))

        # 替换名字中动态的参数
        result_activities = []
        for current_activities in tmp_activities:
            tmp_name = current_activities[0]
            tmp_name.replace("%v", self.data.varNames[self.random(12)%len(self.data.varNames)])
            tmp_name.replace("%t", self.data.tools[self.random(11)%len(self.data.tools)])
            tmp_name.replace("%l", str(self.random(12)%247+30))
            result_activities.append({
                "name": tmp_name,
                "good": current_activities[1],
                "bad": current_activities[2]
            })

        list_good, list_bad = [], []
        for i in range(num_good):
            list_good.append({
                "name": result_activities[i]["name"],
                "description": result_activities[i]["good"]
            })
        for i in range(num_bad):
            list_bad.append({
                "name": result_activities[num_good+i]["name"],
                "description": result_activities[num_good+i]["bad"]
            })
        return {"good": list_good, "bad": list_bad}

# 程序员老黄历
@bp.route('/programmer_calendar', methods=['GET', 'POST'])
def programmer_calendar():
    # 计算
    target_date = (dt.datetime.now().strftime("%Y-%m-%d") if request.args.get('date', None, type=str) is None
                   else request.args.get('date', None, type=str))

    main_calendar = ProgrammerCalendar(target_date)
    star = main_calendar.get_star()
    stars = []
    for i in range(int(star)):
        stars.append(1)
    for i in range(5-int(star)):
        stars.append(0)
    lucks = main_calendar.get_today_luck()
    return render_template("life/programmer_calendar.html", target_date=main_calendar.target_date_date,
                           direction=main_calendar.get_direction(),
                           drinks=main_calendar.get_random_drinks(), star=stars, lucks=lucks, title="程序员老黄历")


