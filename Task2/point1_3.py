import matplotlib.pyplot as plt
import random
import numpy as np
from prettytable import PrettyTable
import statistics as stat

def get_subselection(x):
    x_sub = []
    x_rand = x
    n = len(x)
    random.shuffle(x_rand)
    final = int(n / 10 + 9)
    for i in range(0, 10):
        t = []
        for j in range(0, final):
            t.append(x_rand[j + (int(n / 10) - 1) * i])
        x_sub.append(t)
    return x_sub

# Получение момента
def calculate_moment(x, degree, avr):
    result = 0.0
    for i in range(0, len(x)):
        result += (x[i] - avr) ** degree
    return round(result / len(x), 3)

# Построение таблицы
def point_table(x):
    table = PrettyTable()
    table.add_column("Объём подвыборки", ns)
    table.add_column("xmean", x_mean)
    table.add_column("xmed", x_med)
    table.add_column("xave", x_ave)
    table.add_column("var", var2)
    table.add_column("m3", m3)
    table.add_column("m4", m4)
    table.add_column("As", asym)
    table.add_column("Ex", ex)
    print(table)
    print("Мода: ", round(stat.mode(x), 3))
    print("Интерквартильный промежуток: [", lower_bound, ", ", upper_bound, "]")

# Построение графиков
def plot_point():
    y = [np.zeros(10), np.ones(10), np.zeros(10) - 1]
    plt.title("Среднее арифметическое, медиана, средина размаха")
    plt.scatter(x_mean[:10], y[1], label='n = N/10')
    plt.scatter(x_mean[10], y[1][0], label='n = N', marker='d')
    plt.scatter(x_med[:10], y[0])
    plt.scatter(x_med[10], y[0][0], marker='d')
    plt.scatter(x_ave[:10], y[2])
    plt.scatter(x_ave[10], y[2][0], marker='d')
    plt.legend()
    plt.show()

    plt.title("Дисперсия")
    plt.scatter(var[:10], y[1], label='n = N/10')
    plt.scatter(var[10], y[1][0], label='n = N', marker='d')
    plt.legend()
    plt.show()

    plt.title("3й центральный момент")
    plt.scatter(m3[:10], y[1], label='n = N/10')
    plt.scatter(m3[10], y[1][0], label='n = N', marker='d')
    plt.legend()
    plt.show()

    plt.title("4й центральный момент")
    plt.scatter(m4[:10], y[1], label='n = N/10')
    plt.scatter(m4[10], y[1][0], label='n = N', marker='d')
    plt.legend()
    plt.show()

    plt.title("Асимметрия")
    plt.scatter(asym[:10], y[1], label='n = N/10')
    plt.scatter(asym[10], y[1][0], label='n = N', marker='d')
    plt.legend()
    plt.show()

    plt.title("Эксцесс")
    plt.scatter(ex[:10], y[1], label='n = N/10')
    plt.scatter(ex[10], y[1][0], label='n = N', marker='d')
    plt.legend()
    plt.show()

# Получение точечной оценки
def point_estimates(x, x_sub):
    global ns, x_mean, x_med, x_ave, var, var2, asym, ex, m3, m4, lower_bound, upper_bound, y
    n = len(x_sub)
    ns = []
    x_mean, x_med, x_ave = [], [], []  # Среднее арифметическое, медиана и середина размаха
    var, var2 = [], []  # Дисперсия и её квадрат
    asym = []  # Асимметрия
    ex = []  # Эксцесс
    m3, m4 = [], []  # Третий и четвертый центральные моменты
    for i in range(0, n + 1):
        if i != 10:
            u = x_sub[i]
            ns.append(len(x) / 10)
        else:
            u = x
            ns.append(len(x))
            lower_bound = round(stat.mean(u) - stat.stdev(u) * 1.9602111525053565, 3)
            upper_bound = round(stat.mean(u) + stat.stdev(u) * 1.9602111525053565, 3)
        x_mean.append(round(stat.mean(u), 3))
        x_med.append(round(stat.median(u), 3))
        x_ave.append(round((min(u) + max(u)) / 2, 3))
        var2.append(round(stat.variance(u), 3))
        var.append(round(var2[i] ** (1 / 2), 3))
        m3.append(calculate_moment(u, 3, x_mean[i]))
        asym.append(round(m3[i] / (calculate_moment(u, 2, x_mean[i]) ** 3 / 2), 6))
        m4.append(calculate_moment(u, 4, x_mean[i]))
        ex.append(round(m4[i] / calculate_moment(u, 2, x_mean[i]) ** 2 - 3, 3))
    return [x_mean[0], x_mean[10], var2[0], var2[10]]

def point_res(x, x_sub):
    point_estimates(x, x_sub)
    return asym[10], ex[10]
