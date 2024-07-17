import random
from point1_2 import kernal_res
from point1_3 import point_res
from point1_4 import interval_res
from point2_1 import compare_with_theory_plot
from point2_2 import compare_with_theory_params
from point2_3 import check_hypothsis

with open("Task_2a.txt") as f:
    n = int(f.readline().split(" ")[2])
    x = f.readline().split(" ")
    x.pop()
    for i in range(len(x)):
        x[i] = float(x[i])


# Получение массива подвыборок из выборки x
def get_subselection(x):
    x_sub = []
    x_rand = x
    random.shuffle(x_rand)
    final = int(n / 10 + 9)
    for i in range(0, 10):
        t = []
        for j in range(0, final):
            t.append(x_rand[j + (int(n / 10) - 1) * i])
        x_sub.append(t)
    return x_sub


if __name__ == "__main__":
    # 1

    # 1.1
    x_sub = get_subselection(x)
    # 1.2
    kernal_res((x))
    # 1.3
    asym, ex = point_res(x, x_sub)
    # 1.4
    interval_res(x, x_sub)

    # 2

    # 2.1
    compare_with_theory_plot(x)
    # 2.2
    P, MMP = compare_with_theory_params(x, ex)
    # 2.3
    check_hypothsis(x, P, MMP)
