import numpy as np


g = 9.81


def get_ode(params):
    m = params['m']
    c = params['c']

    def ode(t, y):
        _, _, vx, vy = y
        dx = vx
        dy = vy
        dvx = -c/m * vx
        dvy = -(c*vy + m*g) / m
        return np.array([dx, dy, dvx, dvy])
    return ode


def get_above_surface(params):
    surface_func = params['phi']
    def above_surface(t, y): return y[1] >= surface_func(y[0])
    return above_surface


def get_cauchy_data(params):
    angle = params['angle']
    x0 = params['x0']
    y0 = params['y0']
    v0 = params['v0']
    return np.array([x0, y0, v0*np.cos(angle), v0*np.sin(angle)])


def get_root_equation(params, polynomial):
    surface_func = params['phi']

    def root_equation(t):
        x, y, *_ = polynomial(t)
        return y - surface_func(x)
    return root_equation


def get_equation(params):
    m = params['m']
    c = params['c']
    x0 = params['x0']
    y0 = params['y0']
    v0 = params['v0']
    angle = params['angle']

    def equation(t):
        x = x0 + m/c*v0 * np.cos(angle)*(-np.exp(-c/m*t) + 1)
        y = y0 + m/c * ((m/c*g + v0*np.sin(angle)) * (1 - np.exp(-c/m*t)) - g*t)
        vx = np.exp(-c/m*t) * v0 * np.cos(angle)
        vy = (v0*np.sin(angle) + m/c*g) * np.exp(-c/m*t) - m/c*g
        return x, y, vx, vy
    return equation

def calculate_angle(params, y_ans, t_ans):
    c = params['c']
    m = params['m']
    x0 = params['x0']
    v0 = params['v0']
    return np.arccos(c * (y_ans[0] - x0) / (m * v0 * (1 - np.exp(-c / m * t_ans))))