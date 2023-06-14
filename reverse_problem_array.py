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
    'v0': 15,
    'angle': np.radians(60),
    'surface_func': surface_functions.phi2
}
step_size = 0.01
eps = 1e-9

x_end_vals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
ans = []

test_angles = np.linspace(0, np.pi/2, 100, endpoint=True)
test_x = np.array([find_x(angle) for angle in test_angles])
for x_end in x_end_vals:
    i = 0
    while i < len(test_x) - 1:
        if test_x[i] <= x_end < test_x[i+1]:
            angle_ans = rootfind.find_root(lambda angle: find_x(angle) - x_end, test_angles[i], test_angles[i+1], 1e-15, 'bisection')
            x = find_x(angle_ans)
            if np.abs(x - x_end) <= 0.1:
                test_angles = np.insert(test_angles, i, [angle_ans])
                test_x = np.insert(test_x, i, [x])
                ans.append((x_end, angle_ans))
                i += 1
        elif test_x[i] > x_end >= test_x[i+1]:
            angle_ans = rootfind.find_root(lambda angle: find_x(angle) - x_end, test_angles[i+1], test_angles[i], 1e-15, 'bisection')
            x = find_x(angle_ans)
            if np.abs(x - x_end) <= 0.1:
                test_angles = np.insert(test_angles, i, [angle_ans])
                test_x = np.insert(test_x, i, [x])
                ans.append((x_end, angle_ans))
                i += 1
        i += 1

print(ans)

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