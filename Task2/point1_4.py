import matplotlib.pyplot as plt
from prettytable import PrettyTable
import statistics as stat
from point1_3 import point_estimates


# Получение сигма
def calculate_sigma(x, ave):
    s = 0.0
    for i in x:
        s += (i - ave) ** 2
    s /= round((len(x) - 1), 3)
    s = s ** (1 / 2)
    return s

# Построение таблицы
def interval_table():
    table = PrettyTable()
    table.add_column(" ", ns)
    table.add_column("Параметрические толерантные пределы", bounds_param)
    table.add_column("Непараметрические пределы", bounds_nonparam)
    table.add_column("1й момент", m[0])
    print(table)

# Построение графиков
def plot_interval():
    plt.title("1й момент, полная выборка")
    plt.scatter(points[1], [1], color="red", label="точечная оценка")
    plt.plot(m[0][10], [1, 1], label="интервальная оценка")
    plt.legend()
    plt.show()

    plt.title("1й момент, подвыборка")
    plt.scatter(points[0], [1], color="red", label="точечная оценка")
    plt.plot(m[0][0], [1, 1], label="интервальная оценка")
    plt.legend()
    plt.show()

    plt.title("дисперсия, полная выборка")
    plt.scatter(points[3], [1], color="red", label="точечная оценка")
    plt.plot(m[1][10], [1, 1], label="интервальная оценка")
    plt.legend()
    plt.show()

    plt.title("дисперсия, подвыборка")
    plt.scatter(points[2], [1], color="red", label="точечная оценка")
    plt.plot(m[1][0], [1, 1], label="интервальная оценка")
    plt.legend()
    plt.show()

    plt.title("полная выборка, непараметрические пределы")
    plt.plot(bounds_nonparam[10], [1, 1])
    plt.show()

    plt.title("подвыборка, параметрические пределы")
    plt.plot(bounds_param[0], [1, 1])
    plt.show()

# Получение интервальной оценки
def interval_estimates(x, x_sub):
    global ns, bounds_param, bounds_nonparam, m, points

    # Получение моментов
    def get_1st_moment(x):
        ave = stat.mean(x)
        s = calculate_sigma(x, ave)
        n = len(x)
        if n == 19200:
            k = 1.281639766840975
        else:
            k = 1.2824349652798663
        return [ave - k * pow(n, -0.5) * s, ave + k * pow(n, -0.5) * s]

    def get_2nd_moment(x):
        ave = stat.mean(x)
        s = calculate_sigma(x, ave)
        n = len(x)
        if n == 19200:
            k1 = 19450.54961
            k2 = 18948.30689

        else:
            k1 = 1998.810088
            k2 = 1840.046392
        return [pow(s, 2) * (n - 1) / k1, pow(s, 2) * (n - 1) / k2]

    # Получение параметрических толерантных пределов
    def get_param(x):
        ave = stat.mean(x)
        s = calculate_sigma(x, ave)
        lower_bound = float(ave - s * 1.9602111)
        upper_bound = ave + s * 1.9602111525053565
        return [round(lower_bound, 3), round(upper_bound, 3)]

    # Получение непараметрических толерантных пределов
    def get_nonparam(x):
        sorted_x = sorted(x)
        return [sorted_x[0], sorted_x[len(x) - 1]]

    inner_x_sub = x_sub
    points = point_estimates(x, x_sub)
    inner_x_sub.append(x)
    n = len(inner_x_sub)
    ns = []
    m = [[], []]
    bounds_param = []
    bounds_nonparam = []
    for i in range(n):
        if i == n - 1:
            ns.append(n)
            bounds_nonparam.append(get_nonparam(inner_x_sub[i]))
        else:
            ns.append(n / 10)
            bounds_nonparam.append("")
        bounds_param.append(get_param(inner_x_sub[i]))
        m[0].append(get_1st_moment(inner_x_sub[i]))
        m[1].append(get_2nd_moment(inner_x_sub[i]))
    print(m[0])
    print(m[1])


def interval_res(x, x_sub):
    interval_estimates(x, x_sub)
    interval_table()
    plot_interval()
