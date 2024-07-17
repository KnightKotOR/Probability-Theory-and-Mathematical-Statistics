import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import gamma, lognorm, weibull_min


def compare_with_theory_plot(x):
    x_theory = np.linspace(0, 3.5, 1000)

    a, b, c = gamma.fit(x)
    d, e, f = lognorm.fit(x)
    k, h, l = weibull_min.fit(x)

    gam = gamma.pdf(x_theory, a, b, c)
    logn = lognorm.pdf(x_theory, d, e, f)
    w_min = weibull_min.pdf(x_theory, k, h, l)


    print(gamma.fit(x), " ; ", lognorm.fit(x), " ; ", weibull_min.fit(x))

    print("Медиана: ", l * pow(math.log(2, math.e), 1 / k))
    print("Мода: ", l * pow(k - 1, 1 / k) / pow(k, 1 / k))

    plt.title("гамма распределение")
    plt.plot(x_theory, gam)
    plt.hist(x, 14, density=True)
    plt.show()

    plt.title("логнормальное распределение")
    plt.plot(x_theory, logn)
    plt.hist(x, 14, density=True)
    plt.show()

    plt.title("распределение Вейбулла")
    plt.plot(x_theory, w_min)
    plt.hist(x, 14, density=True)
    plt.show()
