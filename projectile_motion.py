import numpy as np
from numerical import *
import collections


g = 9.81


def get_ode(m, c):
    def ode(t, w):
        _, _, vx, vy = w
        dx = vx
        dy = vy
        dvx = -c/m * vx
        dvy = -(c*vy/m + g)
        return np.array([dx, dy, dvx, dvy])
    return ode


def get_above_surface(surface_func):
    def above_surface(t, w): return w[1] >= surface_func(w[0])
    return above_surface


def get_cauchy_data(x0, y0, v0, angle):
    return 0, np.array([x0, y0, v0*np.cos(angle), v0*np.sin(angle)])


def get_root_equation(surface_func, polynomial):
    def root_equation(t):
        x, y, *_ = polynomial(t)
        return y - surface_func(x)
    return root_equation


def get_equation(m, c, x0, y0, v0, angle):
    def equation_air_resistance(t):
        x = x0 + m/c*v0 * np.cos(angle)*(-np.exp(-c/m*t) + 1)
        y = y0 + m/c * ((m/c*g + v0*np.sin(angle)) * (1 - np.exp(-c/m*t)) - g*t)
        vx = np.exp(-c/m*t) * v0 * np.cos(angle)
        vy = (v0*np.sin(angle) + m/c*g) * np.exp(-c/m*t) - m/c*g
        return x, y, vx, vy
    def equation_no_air_resistance(t):
        x = x0 + v0 * np.cos(angle) * t
        y = y0 + v0 * np.sin(angle) * t - g * t**2 / 2
        vx = v0 * np.cos(angle)
        vy = v0 * np.sin(angle) - g * t
        return x, y, vx, vy
    if c == 0:
        return equation_no_air_resistance
    else:
        return equation_air_resistance

def calculate_angle(m, c, x0, v0, x, t):
    if c == 0:
        return np.arccos((x-x0) / (v0*t))
    else:
        return np.arccos(c * (x-x0) / (m * v0 * (1-np.exp(-c/m*t))))


def calculate_error(w, w_analytical, h):
    return np.max(np.linalg.norm(w[-1:] - w_analytical[-1:], axis=1)) / h**4


class Solution:
    def __init__(self, param, step_size, eps, ode_method='adams4', interp_method='lagrange', rootfind_method='bisection'):
        self.m = param['m']
        self.c = param['c']
        self.x0 = param['x0']
        self.y0 = param['y0']
        self.v0 = param['v0']
        self.angle = param['angle']
        self.surface_func = param['surface_func']
        self.step_size = step_size
        self.eps = eps
        self.ode_method = ode_method
        self.interp_method = interp_method
        self.rootfind_method = rootfind_method
        self._solve()

    def _solve(self):
        ode_func = get_ode(self.m, self.c)
        t0, w0 = get_cauchy_data(
            self.x0, self.y0, self.v0, self.angle)
        above_surface = get_above_surface(self.surface_func)

        self.t, self.w = integration.solve_ode(
            ode_func, t0, w0, self.step_size,
            predicate_func=above_surface,
            method=self.ode_method
        )
        polynomial = interpolation.interpolate(self.t[-4:], self.w[-4:], self.interp_method)
        root_equation = get_root_equation(self.surface_func, polynomial)
        self.t_ans = rootfind.find_root(root_equation, self.t[-2], self.t[-1], self.eps, self.rootfind_method)
        self.w_ans = polynomial(self.t_ans)

    def get_solution_pts(self):
        solution_pts = self.w.copy()
        solution_pts[-1] = self.w_ans
        return solution_pts