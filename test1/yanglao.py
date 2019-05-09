import math

# 每月计划投入多少钱
plan = 5000

# 现在几岁
now_age = 27

# 多少岁可以取
plan_age = 40

# 目标活到多少岁
target_age = 80

# 周期，按月则是12，按周52，按天356
cycle = 12

# 分红，分红先不计算利率
profit = 129060

# 到期后每月返还多少
get_plan = 1029.5
# 预期利率
plan_rate = 0.10

def getWorthy():
    '''
    计算利息
    :return:
    '''
    global plan, plan_age, now_age, target_age, cycle, plan_rate

    # 计算支付的
    pay_year = plan_age - now_age
    pay_total = 0
    while pay_year > 0:
        pay_total += math.pow(1 + plan_rate, pay_year)

        pay_year -= 1
    pay_total = pay_total * plan * cycle
    # 计算收益
    get_total = 0
    get_year = target_age - plan_age

    # 计算投入的钱到死的时候的雪球
    pay_total = pay_total * math.pow(1 + plan_rate, get_year)

    while get_year > 0:
        get_total += math.pow(1 + plan_rate, get_year)

        get_year -= 1

    # 计算能得到的
    get_total = get_total * get_plan * cycle + profit
    print(pay_total, get_total)
    return "不值" if pay_total > get_total else "值"

print(getWorthy())

