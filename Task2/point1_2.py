import numpy as np
from math import e, pi, sqrt

# Получение ядерного оценивания
def kernel(x, h):
    # Вложенные функции для получения
    def Gauss(p):
        return pow(e, (-pow(p, 2) / 2)) / sqrt(2 * pi)

    def Cauchy(p):
        return 1 / (pi * (1 + pow(p, 2)))

    def Exponential(p):
        return pow(e, -abs(p)) / 2

    x_sorted = sorted(x)
    n = len(x)
    nh = n * h
    pkde_gauss, pkde_cauchy, pkde_exponential = np.zeros(n), np.zeros(n), np.zeros(n)
    for i in range(0, n):
        print(i)
        t_gauss, t_cauchy, t_exponential = 0, 0, 0
        for j in range(0, n):
            diff = x_sorted[i] - x_sorted[j]
            t_gauss += Gauss(diff / h)
            t_cauchy += Cauchy(diff / h)
            t_exponential += Exponential(diff / h)
        pkde_gauss[i] = t_gauss / nh
        pkde_cauchy[i] = t_cauchy / nh + 0.001
        pkde_exponential[i] = t_exponential / nh
    return x_sorted, [pkde_gauss, pkde_cauchy, pkde_exponential]

def kernal_res(x):
    plot_hist(x)
    x_sorted, PKDE = kernel(x, 0.1)
    plot_sdf(x_sorted)
    plot_kernal(x_sorted, PKDE)
