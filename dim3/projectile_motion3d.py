import numpy as np
from numerical import *


g = 9.81


def get_ode(m, c):
    def ode(t, w):
        _, _, _, vx, vy, vz = w
        dx = vx
        dy = vy
        dz = vz
        dvx = -c/m * vx
        dvy = -c/m * vy
        dvz = -(c*vz/m + g)
        return np.array([dx, dy, dz, dvx, dvy, dvz])
    return ode


def get_above_surface(surface_func):
    def above_surface(t, w): return w[2] >= surface_func(w[0], w[1])
    return above_surface


def get_cauchy_data(x0, y0, z0, v0, anglexy, anglexz):
    return 0, np.array([
        x0, y0, z0,
        v0*np.cos(anglexy)*np.cos(anglexz), v0*np.cos(anglexy)*np.sin(anglexz), v0*np.sin(anglexy)
    ])


def get_root_equation(surface_func, polynomial):
    def root_equation(t):
        x, y, z, *_ = polynomial(t)
        return z - surface_func(x, y)
    return root_equation


def get_equation(m, c, x0, y0, z0, v0, anglexy, anglexz):
    def equation_air_resistance(t):
        x = x0 + m/c*v0 * np.cos(anglexy)*np.cos(anglexz)*(-np.exp(-c/m*t) + 1)
        y = y0 + m/c*v0 * np.cos(anglexy)*np.sin(anglexz)*(-np.exp(-c/m*t) + 1)
        z = z0 + m/c * ((m/c*g + v0*np.sin(anglexy)) * (1 - np.exp(-c/m*t)) - g*t)
        vx = np.exp(-c/m*t) * v0 * np.cos(anglexy) * np.cos(anglexz)
        vy = np.exp(-c/m*t) * v0 * np.cos(anglexy) * np.sin(anglexz)
        vz = (v0*np.sin(anglexy) + m/c*g) * np.exp(-c/m*t) - m/c*g
        return x, y, z, vx, vy, vz
    def equation_no_air_resistance(t):
        x = x0 + v0 * np.cos(anglexy) * np.cos(anglexz) * t
        y = y0 + v0 * np.cos(anglexy) * np.sin(anglexz) * t
        z = z0 + v0 * np.sin(anglexy) * t - g * t**2 / 2
        vx = v0 * np.cos(anglexy) * np.cos(anglexz)
        vy = v0 * np.cos(anglexy) * np.sin(anglexz)
        vz = v0 * np.sin(anglexy) - g * t
        return x, y, z, vx, vy, vz
    if c == 0:
        return equation_no_air_resistance
    else:
        return equation_air_resistance

# def calculate_angle(m, c, x0, v0, x, t):
#     if c == 0:
#         return np.arccos((x-x0) / (v0*t))
#     else:
#         return np.arccos(c * (x-x0) / (m * v0 * (1-np.exp(-c/m*t))))


def calculate_error(w, w_analytical, h):
    return np.max(np.linalg.norm(w[-4:] - w_analytical[-4:], axis=1)) / h**4


class Solution:
    def __init__(self, p, step_size, eps):
        self.m = p['m']
        self.c = p['c']
        self.x0 = p['x0']
        self.y0 = p['y0']
        self.z0 = p['z0']
        self.v0 = p['v0']
        self.anglexy = p['anglexy']
        self.anglexz = p['anglexz']
        self.surface_func = p['surface_func']
        self.step_size = step_size
        self.eps = eps
        self._solve()

    def _solve(self):
        ode_func = get_ode(self.m, self.c)
        t0, w0 = get_cauchy_data(
            self.x0, self.y0, self.z0,
            self.v0, self.anglexy, self.anglexz
        )
        above_surface = get_above_surface(self.surface_func)

        self.t, self.w = integration.solve_ode(
            ode_func, t0, w0, self.step_size,
            predicate_func=above_surface,
            method='rk4'
        )
        polynomial = interpolation.interpolate(self.t[-4:], self.w[-4:], 'lagrange')
        root_equation = get_root_equation(self.surface_func, polynomial)
        self.t_ans = rootfind.find_root(root_equation, self.t[-2], self.t[-1], self.eps, 'secant')
        self.w_ans = polynomial(self.t_ans)

    def get_solution_pts(self):
        solution_pts = self.w.copy()
        solution_pts[-1] = self.w_ans
        return solution_pts