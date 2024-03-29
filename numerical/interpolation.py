import numpy as np


def interpolate(x, y, method):
    if method == 'lagrange':
        return interpolate_lagrange(x, y)


def interpolate_lagrange(x_vals, y_vals):
    assert len(x_vals) == len(y_vals), 'x_vals and y_vals must be of same size'

    def polynomial(x):
        basis_funcs = np.empty((len(x_vals)))
        for i, xi in enumerate(x_vals):
            basis_func_members = np.array([(x - xj) / (xi - xj)
                                           for j, xj in enumerate(x_vals)
                                           if j != i])
            basis_funcs[i] = np.prod(basis_func_members)
        y = sum([y_vals[i] * basis_funcs[i] for i in range(len(y_vals))])
        return y
    return polynomial
