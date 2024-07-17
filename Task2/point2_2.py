import matplotlib.pyplot as plt
from math import log, sqrt
import numpy as np
import statistics as stat

from scipy import special
from scipy.stats import gamma, lognorm, weibull_min


def moment_method_gamma(x, asym):
    global p_gamma
    k = (2 / asym) ** 2
    t = sqrt(var / k)
    r = "a = " + str(k) + ", scale = " + str(t)
    plt.title("гамма")
    x_sorted = sorted(x)
    y = np.linspace(0, 1, 19200)
    plt.step(x_sorted, y, label="эмпирическая функция")

    x_theor = np.linspace(0, 3.5, 19200)
    p_gamma = sorted(gamma.cdf(x, k, t))
    plt.plot(x_theor, p_gamma, label="теоретическая функция")
    plt.legend()
    plt.show()
    return r


def moment_method_lognorm(x):
    global p_lognorm
    c = log(med)
    s2 = log(med / mod)
    s = sqrt(abs(s2))
    r = "a = " + str(s) + ", scale = " + str(c)
    plt.title("логнормальное")
    x_sorted = sorted(x)
    y = np.linspace(0, 1, 19200)
    plt.step(x_sorted, y, label="эмпирическая функция")

    x_theor = np.linspace(0, 3.5, 19200)
    p_lognorm = sorted(lognorm.cdf(x, s, c))
    plt.plot(x_theor, p_lognorm, label="теоретическая функция")
    plt.legend()
    plt.show()
    return r


def moment_method_weibull(x):
    global p_weibull
    ks = np.arange(0.1, 10, 0.1)
    for k in ks:
        l1 = med / log(2) ** (1 / k)
        l2 = mean / special.gamma(1 + (1 / k))
        if abs(l2 - l1) < 0.002 and k == round((log(med / l1, log(2))) ** -1, 1):
            l = l1
            break
    r = "a = " + str(k) + ", scale = " + str(l)

    plt.title("Вейбулла")
    x_sorted = sorted(x)
    y = np.linspace(0, 1, 19200)
    plt.step(x_sorted, y, label="эмпирическая функция")

    x_theor = np.linspace(0, 3.5, 19200)
    p_weibull = weibull_min.cdf(x_theor, k, 0, l)
    plt.plot(x_sorted, p_weibull, label="теоретическая функция")
    plt.legend()
    plt.show()
    return r


def mmp_gamma(x):
    global p_mmp_gamma
    a, b, c = gamma.fit(x)
    r = "a = " + str(a) + ", scale = " + str(c)
    x_theor = np.linspace(0, 3.5, 19200)
    p_mmp_gamma = gamma.pdf(x_theor, a, b, c)
    plt.title("гамма распределение")
    plt.plot(x_theor, p_mmp_gamma)
    plt.hist(x, 14, density=True)
    plt.show()
    return r


def mmp_lognorm(x):
    global p_mmp_lognorm
    d, e, f = lognorm.fit(x)
    r = "a = " + str(d) + ", scale = " + str(f)
    x_theor = np.linspace(0, 3.5, 19200)
    p_mmp_lognorm = lognorm.pdf(x_theor, d, e, f)
    plt.title("логнормальное распределение")
    plt.plot(x_theor, p_mmp_lognorm)
    plt.hist(x, 14, density=True)
    plt.show()
    return r


def mmp_weibull(x):
    global p_mmp_weibull
    k, h, l = weibull_min.fit(x, floc=0)
    r = "a = " + str(k) + ", scale = " + str(l)
    x_theor = np.linspace(0, 3.5, 19200)
    p_mmp_weibull = weibull_min.pdf(x_theor, k, h, l)
    plt.title("распределение Вейбулла")
    plt.plot(x_theor, p_mmp_weibull)
    plt.hist(x, 14, density=True)
    plt.show()
    return r


def compare_with_theory_params(x, ex):
    global mean, var, mod, med
    mean = stat.mean(x)
    var = stat.variance(x)
    mod = stat.mode(x)
    med = stat.median(x)

    print("гамма:")
    print("метод моментов:", moment_method_gamma(x, ex))
    print("ммп:", mmp_gamma(x))

    print("логнормальное:")
    print("метод моментов:", moment_method_lognorm(x))
    print("ммп:", mmp_lognorm(x))

    print("Вейбулла:")
    print("метод моментов:", moment_method_weibull(x))
    print("ммп:", mmp_weibull(x), "\n")
    return [p_gamma, p_lognorm, p_weibull], [p_mmp_gamma, p_mmp_lognorm, p_mmp_weibull]
