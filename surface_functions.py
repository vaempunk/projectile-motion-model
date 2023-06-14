import numpy as np


def phi1(x):
    return 0


def phi2(x):
    return (x-5)**2 - 4 if 3 < x <= 7 else 0


def phi3(x):
    return np.max([0, 1 - 2*(x-5.5)**2])


