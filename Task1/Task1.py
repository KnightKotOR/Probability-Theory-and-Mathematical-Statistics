import linecache
from matplotlib import pyplot
import numpy as np
import re


# класс корзины, который содержит:
# номер - 1,
# общее количество шаров,
# количество шаров соответсвующего цвета,
# математический профиль корзины
class Box:
    def __init__(self, n, t, balls):
        math_profile = []
        for c in balls:
            math_profile.append(c / t)

        self.n = int(n)
        self.T = int(t)
        self.balls = balls
        self.P = math_profile

# Построение графиков
def plot_graphs():
    pyplot.title('1a')
    pyplot.plot(plot_res)
    pyplot.legend(np.arange(1, N + 1, 1))
    pyplot.show()

    pyplot.title('1b')
    pyplot.plot(plot_mod)
    pyplot.legend([mod + 1])
    pyplot.show()

    pyplot.title('1c')
    pyplot.plot(plot_dom)
    pyplot.show()

    pyplot.title('2c')
    pyplot.plot(exp_prof)
    pyplot.show()

# Визуализация математических профилей
def plot_hists():
    c = ['r', 'w', 'bk', 'g', 'b']
    for box in Boxes:
        pyplot.title(("Box №" + str(box.n + 1)))
        pyplot.bar(c, box.P, width=0.5, color=['red', 'white', 'black', 'green', 'blue'],
                   edgecolor='black')
        pyplot.show()

    pyplot.title("Exp")
    pyplot.bar(c, exp_prof[-1], width=0.5, color=['red', 'white', 'black', 'green', 'blue'],
               edgecolor='black')
    pyplot.show()

# Получение и обработка входных параметров
def getInitData():
    global N, m, d, p_change, nExp
    init_data = linecache.getline('task_1_ball_boxes.txt', 2).split(',')

    N = int(re.sub("\D", "", init_data[0]))
    m = int(re.sub("\D", "", init_data[1]))
    d = int(re.sub("\D", "", init_data[2]))
    p_change = float(re.sub("[^\d.]", "", init_data[3]))
    nExp = int(re.sub("\D", "", init_data[4]))

    boxes_data = []
    for i in range(0, N):
        cur_box = linecache.getline('task_1_ball_boxes.txt', 3 + i).split(' ')
        n = int(re.sub("\D", "", cur_box[1]))
        T = int(re.sub("\D", "", cur_box[3]))
        r = int(re.sub("\D", "", cur_box[5]))
        w = int(re.sub("\D", "", cur_box[7]))
        bk = int(re.sub("\D", "", cur_box[9]))
        g = int(re.sub("\D", "", cur_box[11]))
        b = int(re.sub("\D", "", cur_box[13]))
        colors = [r, w, bk, g, b]

        boxes_data.append(Box(n - 1, T, colors))

    return boxes_data

# Подсчет вероятности достать комбинацию шагов exp_balls на k шаге эксперимента для корзины box
def get_prob(box, exp_balls):
    c = 0
    res = 1
    for color in box.balls:
        res *= color ** exp_balls[c]
        c += 1
    res /= box.T ** 4
    return res

# Получение превалирующих гипотез на k шаге эксперимента
def get_dom():
    cur_dominant = np.zeros(N)
    max_prob = max(PAHi)
    diff = 0.1

    for i in range(0, len(PAHi)):
        p = PAHi[i]
        if max_prob - p < diff:
            cur_dominant[i] = 1
    return cur_dominant

# Получение результатов k-ого шага эксперимента
def get_k_res(x, balls):
    global p_change, PAHi, total_balls

    # Обработка полученных данных
    k = linecache.getline('task_1_ball_boxes.txt', x).split(' ')
    for j in range(1, 5):
        if k[len(k) - j].__contains__('Red'):
            balls[0] += 1
        elif k[len(k) - j].__contains__('White'):
            balls[1] += 1
        elif k[len(k) - j].__contains__('Black'):
            balls[2] += 1
        elif k[len(k) - j].__contains__('Green'):
            balls[3] += 1
        elif k[len(k) - j].__contains__('Blue'):
            balls[4] += 1

    # Подсчет вероятностей гипотез
    for box in Boxes:
        t = get_prob(box, balls) * (1 - p_change)
        inner_t = 0
        for inner_box in Boxes:
            if inner_box.n != box.n:
                inner_t += get_prob(inner_box, balls)
        inner_t *= p_change / (N - 1)
        t += inner_t
        PAHi[box.n] *= t

    s = sum(PAHi)

    res = []
    for i in range(0, len(Boxes)):
        PAHi[i] /= s
        res.append(PAHi[i])
    return res

# Подсчет математического профиля эксперимента на k шаге
def get_prof(x, cur_balls, cur_prof):
    res = list(cur_prof)
    for i in range(0, len(cur_balls)):
        res[i] = cur_balls[i] / (x * d)
    return res

# Получение полных результатов эксперимента
def get_exp_res():
    total_balls, counter_balls, cur_prof = np.zeros(5), np.zeros(5), np.zeros(5)
    prob, dominant, prof = [], [], []
    for i in range(10, nExp + 10):
        prob.append(get_k_res(i, counter_balls))
        total_balls += counter_balls
        prof.append(get_prof(i, total_balls, cur_prof))
        dominant.append(get_dom())
        counter_balls = np.zeros(5)
    return prob, dominant, prof


if __name__ == "__main__":

    Boxes = getInitData()

    PAHi = np.ones(N)

    exp_prob, exp_dominant, exp_prof = get_exp_res()
    mod = int(np.argmax(sum(exp_dominant)))

    # Создание списков с меньшим количеством данных для лучшей визуализации изменений
    plot_res, plot_dom, plot_mod = [], [], []
    for i in range(0, 100):
        plot_res.append(exp_prob[i])
        plot_dom.append(sum(exp_dominant[i]))
        plot_mod.append(exp_prob[i][mod])

    plot_graphs()
    plot_hists()

