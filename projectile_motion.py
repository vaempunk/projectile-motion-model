import numpy as np


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