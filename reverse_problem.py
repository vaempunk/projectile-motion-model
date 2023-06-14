import numpy as np
from projectile_motion import Solution
import matplotlib.pyplot as plt
from numerical import rootfind
import surface_functions


def find_x(angle):
    param = p.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    return solution.w_ans[0]


# define parameters
p = {
    'm': 1,
    'c': 0.5,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(45),
    'surface_func': surface_functions.phi2
}
step_size = 0.01
eps = 0.000001

x_end = 5.0
ans = []

test_angles = np.linspace(0, np.pi, 100, endpoint=True)
test_x = np.array([find_x(angle) for angle in test_angles])
i = 0
for i in range(len(test_x) - 1):
    if test_x[i] <= x_end < test_x[i+1]:
        angle_ans = rootfind.find_root(lambda angle: find_x(angle) - x_end, test_angles[i], test_angles[i+1], 1e-12, 'bisection')
        if np.abs(find_x(angle_ans) - x_end) <= eps:
            ans.append((x_end, angle_ans))
    elif test_x[i] > x_end >= test_x[i+1]:
        angle_ans = rootfind.find_root(lambda angle: find_x(angle) - x_end, test_angles[i+1], test_angles[i], 1e-12, 'bisection')
        if np.abs(find_x(angle_ans) - x_end) <= eps:
            ans.append((x_end, angle_ans))
    i += 1

print([(x, np.degrees(angle)) for x, angle in ans])

for x, angle in ans:
    param = p.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    w = solution.w

    plt.plot(w[:, 0], w[:, 1])
    plt.plot([x], [param['surface_func'](x)], 'rx')

    x_surface = np.linspace(min(w[:, 0]) - 2, max(w[:, 0]) + 2, 1000)
    plt.plot(x_surface, [param['surface_func'](x) for x in x_surface], 'k-')

plt.show()