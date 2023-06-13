import numpy as np
from projectile_motion import Solution
from numerical import rootfind
import surface_functions

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
    'surface_func': surface_functions.phi3
}
step_size = 0.01
eps = 0.000001

def find_xcoord(angle):
    param = params.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    return solution.y_ans[0]

def find_time(angle):
    param = params.copy()
    param['angle'] = angle
    solution = Solution(param, step_size, eps)
    return solution.t_ans

angles1 = np.linspace(0, np.pi/4, 90)
angles2 = np.linspace(np.pi/4, np.pi/2, 90)
xcoords1 = np.array([find_xcoord(angle) for angle in angles1])
xcoords2 = np.array([find_xcoord(angle) for angle in angles2])
solution = Solution(params, step_size, eps)
xcoord = solution.y_ans[0]
for i in range(len(xcoords1) - 1):
    if xcoords1[i] <= solution.y_ans[0] < xcoords1[i+1]:
        my_angle = rootfind.find_root(lambda angle: find_xcoord(angle) - solution.y_ans[0], angles1[i], angles1[i+1], 1e-6, 'bisection')
        print('Angle:', np.degrees(my_angle))
for i in range(len(xcoords2) - 1):
    if xcoords2[i] > solution.y_ans[0] >= xcoords2[i+1]:
        my_angle = rootfind.find_root(lambda angle: find_xcoord(angle) - solution.y_ans[0], angles2[i], angles2[i+1], 1e-6, 'bisection')
        print('Angle:', np.degrees(my_angle))

