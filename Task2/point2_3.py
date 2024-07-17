from scipy.stats import chi2_contingency, ks_2samp

def chi_square(x, theor):
    observed = []
    for i in range(len(x)):
        if (x[i] * theor[i] == 0):
            observed.append([x[i], 0.000000000000001])
        else:
            observed.append([x[i], theor[i]])
    chi2, p, dof, expected = chi2_contingency(observed)
    print("chi_square: ", chi2, p)


def kolmogorov_smirnov(x, theor):
    ks_statistic, p_value = ks_2samp(x, theor)
    print("kolmogorov_smirnov: ",ks_statistic, p_value)


def von_mises(x, f):
    n = len(x)
    mises = 1 / (12 * len(x))
    for i in range(0, len(x)):
        mises += (f[i] - (2 * i - 1) / (2 * n)) ** 2
    print("von_mises: ", mises / n)

def check_hypothsis(x, P, MMP):
    print("P: \n")
    for p in P:
        chi_square(x, p)
        kolmogorov_smirnov(x, p)
        von_mises(x, p)
        print("\n")
    print("MMP: \n")
    for mmp in MMP:
        chi_square(x, mmp)
        kolmogorov_smirnov(x, mmp)
        von_mises(x, mmp)
        print("\n")

