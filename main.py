import numpy as np
import plot
import matplotlib.pyplot as plt
import projectile_motion
import scipy.misc
from numerical import integration, interpolation, rootfind


class Solution:
    def __init__(self, params, step_size, eps):
        self.m = params['mass']
        self.c = params['air_resist_coeff']
        self.x0 = params['x0']
        self.y0 = params['y0']
        self.v0 = params['v0']
        self.angle = params['angle']
        self.surface_func = params['surface_func']
        self.step_size = step_size
        self.eps = eps

    def solve(self):
        ode = projectile_motion.get_ode(self.m, self.c)
        t0, y0 = projectile_motion.get_cauchy_data(
            self.x0, self.y0, self.v0, self.angle)
        above_surface = projectile_motion.get_above_surface(self.surface_func)

        self.t, self.y = integration.solve_ode(
            ode, t0, y0, self.step_size,
            predicate_func=above_surface,
            method='rk4'
        )
        polynomial = interpolation.interpolate(
            self.t[-4:], self.y[-4:], 'lagrange')
        root_equation = projectile_motion.get_root_equation(
            self.surface_func, polynomial)
        self.t_ans = rootfind.find_root(
            root_equation, self.t[-2], self.t[-1], self.eps, 'bisection')
        self.y_ans = polynomial(self.t_ans)


# # define parameters
# def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0


# # def phi(x): return 0
# params = {
#     'mass': 1,
#     'air_resist_coeff': 1,
#     'x0': 0,
#     'y0': 0,
#     'v0': 10,
#     'angle': np.radians(45),
#     'surface_func': phi
# }
# step_size = 0.01
# eps = 0.0001


# solution = Solution(params, step_size, eps)
# solution.solve()
# print(f'Answer: {solution.t_ans}, ({solution.y_ans[0]}, {solution.y_ans[1]})')

# # get analytical solution
# equation = projectile_motion.get_equation(
#     params['mass'], params['air_resist_coeff'],
#     params['x0'], params['y0'], params['v0'],
#     params['angle'])
# y_analytical = np.array([equation(tn) for tn in solution.t])

# # find error
# error = projectile_motion.calculate_error(solution.y, y_analytical, step_size)
# print(f'Error: {error}')

# # plot numerical and analytical trajectories
# plot.trajectories(solution.y, y_analytical, phi)
