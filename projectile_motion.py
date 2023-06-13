import numpy as np
from numerical import *


g = 9.81


def get_ode(m, c):
    def ode(t, y):
        _, _, vx, vy = y
        dx = vx
        dy = vy
        dvx = -c/m * vx
        dvy = -(c*vy/m + g)
        return np.array([dx, dy, dvx, dvy])
    return ode


def get_above_surface(surface_func):
    def above_surface(t, y): return y[1] >= surface_func(y[0])
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

def calculate_angle(m, c, x0, v0, x_ans, t_ans):
    if c == 0:
        return np.arccos((x_ans - x0) / (v0 * t_ans))
    else:
        return np.arccos(c * (x_ans - x0) / (m * v0 * (1 - np.exp(-c / m * t_ans))))


def calculate_error(y, y_analytical, h):
    return np.max(np.linalg.norm(y[-4:] - y_analytical[-4:], axis=1)) / h**4


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
        self._solve()

    def _solve(self):
        ode_func = get_ode(self.m, self.c)
        t0, y0 = get_cauchy_data(
            self.x0, self.y0, self.v0, self.angle)
        above_surface = get_above_surface(self.surface_func)

        self.t, self.y = integration.solve_ode(
            ode_func, t0, y0, self.step_size,
            predicate_func=above_surface,
            method='rk4'
        )
        polynomial = interpolation.interpolate(
            self.t[-4:], self.y[-4:], 'lagrange')
        root_equation = get_root_equation(
            self.surface_func, polynomial)
        self.t_ans = rootfind.find_root(
            root_equation, self.t[-2], self.t[-1], self.eps, 'bisection')
        self.y_ans = polynomial(self.t_ans)

    def get_solved_y(self):
        solved = self.y.copy()
        solved[-1] = self.y_ans
        return solved