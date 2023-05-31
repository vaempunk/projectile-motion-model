import functools


def interpolate_lagrange(points):
    def polynomial(x):
        basis_funcs = []
        for i1, (x1, _) in enumerate(points):
            basis_func_multipliers = [(x - x2) / (x1 - x2)
                                    for i2, (x2, _) in enumerate(points)
                                    if i2 != i1]
            basis_funcs.append(
                functools.reduce(lambda x, y: x * y, basis_func_multipliers, 1))
        ans = sum([basis_funcs[i] * points[i][1] for i in range(len(points))])
        return ans
    return polynomial

def interpolate_hermit():
    pass