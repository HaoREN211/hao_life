# @Time    : 2020/7/4 18:50
# @Author  : REN Hao
# @FileName: __init__.py.py
# @Software: PyCharm
import pandas as pd
import matplotlib.pyplot as plt


# 根据两只风险股票的利益和标准差进行组合
def find_merge_interest_and_std(par_1, interest_1, std_1, interest_2, std_2, p=0):
    merge_interest = (float(par_1) * float(interest_1)
                      + float(1 - par_1) * float(interest_2))
    merge_std_1 = (par_1 ** 2 * std_1 ** 2
                   + 2 * float(par_1) * float(1 - par_1) * std_1 * std_2 * p
                   + float(1 - par_1) ** 2 * std_2 ** 2) ** 0.5
    return merge_interest, merge_std_1


# 根据无风险资产的基本利率，组合有风险资产下的利率和方差计算最优风险组合
def find_cross_coefficient(basic_interest, interest_1, std_1, interest_2, std_2, p=0):
    int_1_diff = interest_1 - basic_interest
    int_2_diff = interest_2 - basic_interest
    add_par = p*std_1*std_2
    w1 = ((int_1_diff*std_2**2 - (interest_2-basic_interest)*add_par)
          / (int_2_diff*std_1**2 + int_1_diff*std_2**2 - (interest_1+interest_2-2*basic_interest)*add_par))
    return w1, 1-w1


if __name__ == '__main__':
    # 组合风险资产的最优组合系数
    coef_1, coef_2 = find_cross_coefficient(0.05, 0.1, 0.1, 0.2, 0.2)

    # 组合之后的收益和方差
    final_interest, final_std = find_merge_interest_and_std(coef_1, 0.1, 0.1, 0.2, 0.2)

    # 画风险-收益权衡取舍曲线
    result = pd.DataFrame(columns=["part_1", "interest", "std"])
    for i in range(1001):
        current_i = float(i/1000)
        interest, std = find_merge_interest_and_std(current_i, 0.1, 0.1, 0.2, 0.2)
        result = result.append(pd.DataFrame({
            "part_1": [current_i],
            "interest": [interest],
            "std": [std]
        }))
    plt.plot([0, final_std], [0.05, final_interest], c="r")
    plt.scatter(result["std"], result["interest"], s=1)
    plt.text(final_std, final_interest,
             str(final_std)[0:4]+",  "+str(final_interest)[0:4])
    plt.show()

    final_result = pd.DataFrame(columns=["part_1", "interest", "std"])
    for i in range(1001):
        current_i = float(i/1000)
        interest, std = find_merge_interest_and_std(current_i, 0.05, 0, final_interest, final_std)
        final_result = final_result.append(pd.DataFrame({
            "part_1": [current_i],
            "interest": [interest],
            "std": [std]
        }))

    plt.scatter(final_result["std"], final_result["interest"], s=1)
    plt.show()

    min((final_result[final_result["std"] <= 0.01]["part_1"].values))

    print(result)
