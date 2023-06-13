import numpy as np
from main import Solution
from numerical import rootfind
import matplotlib.pyplot as plt

# define parameters
# def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
def phi(x): return 0
params = {
    'mass': 1,
    'air_resist_coeff': 0.5,
    'x0': 0,
    'y0': 0,
    'v0': 20,
    'angle': np.radians(60.732782),
    'surface_func': phi
}
step_size = 0.01
eps = 0.000001

def find_xcoord(angle):
    param = params.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    solution.solve()
    return solution.y_ans[0]

def find_time(angle):
    param = params.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    solution.solve()
    return solution.t_ans

angles = np.linspace(0, np.pi/4, 90)
xcoords = np.array([find_xcoord(angle) for angle in angles])

solution = Solution(params, step_size, eps)
solution.solve()

xcoord = solution.y_ans[0]


for i in range(len(xcoords) - 1):
    if xcoords[i] <= solution.y_ans[0] < xcoords[i+1]:
        print(np.degrees(angles[i]), np.degrees(angles[i+1]))
        my_angle = rootfind.find_root(lambda angle: find_xcoord(angle) - solution.y_ans[0], angles[i], angles[i+1], 1e-6, 'bisection')
        print('Angle:', np.degrees(my_angle))


angles = np.linspace(np.pi/4, np.pi/2, 90)
xcoords = np.array([find_xcoord(angle) for angle in angles])

solution = Solution(params, step_size, eps)
solution.solve()

xcoord = solution.y_ans[0]


for i in range(len(xcoords) - 1):
    if xcoords[i] > solution.y_ans[0] >= xcoords[i+1]:
        print(np.degrees(angles[i]), np.degrees(angles[i+1]))
        my_angle = rootfind.find_root(lambda angle: find_xcoord(angle) - solution.y_ans[0], angles[i], angles[i+1], 1e-6, 'bisection')
        print('Angle:', np.degrees(my_angle))
