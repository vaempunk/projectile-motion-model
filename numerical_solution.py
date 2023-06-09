import numpy as np
from numerical import *


g = 9.81


def get_pm_diffequation(m, c):
    def pm_equation(t, y):
        _, _, vx, vy = y
        dx = vx
        dy = vy
        dvx = -c/m * vx
        dvy = -(c*vy + m*g) / m
        return np.array([dx, dy, dvx, dvy])
    return pm_equation


class NumericalSolution:

    def __init__(self, params, step_size, eps):
        self.m = params['m']
        self.c = params['c']
        self.x0 = params['x0']
        self.y0 = params['y0']
        self.v0 = params['v0']
        self.theta = params['theta']
        self.phi = params['phi']
        self.step_size = step_size
        self.eps = eps

    def approximate_diffequation(self):
        pm_diffequation = get_pm_diffequation(self.m, self.c)
        t0 = 0
        y0 = np.array([
            self.x0,
            self.y0,
            self.v0*np.cos(self.theta),
            self.v0*np.sin(self.theta)
        ])
        rk4 = integration.RK4(pm_diffequation, t0, y0, self.step_size)
        t_vals_rk, y_vals_rk = rk4.next_n(3)

        adams4 = integration.Adams4(pm_diffequation, t_vals_rk, y_vals_rk, self.step_size)
        def floor_hit(_, y): return y[1] > self.phi(y[0])
        self.t_vals, self.y_vals = adams4.next_while(floor_hit)
        # self.t_vals, self.y_vals = rk4.next_while(floor_hit)

        return self.t_vals, self.y_vals

    def interpolate(self):
        self.pm_equation = interpolation.interpolate_lagrange(
            self.t_vals[-4:], self.y_vals[-4:]
        )
        return self.pm_equation

    def find_root(self):
        def root_equation(t):
            x, y, *_ = self.pm_equation(t)
            return y - self.phi(x)
        secant = rootfind.Bisection(root_equation, self.t_vals[-2], self.t_vals[-1])
        self.t_ans = secant.find_root(eps=0.0001)
        self.coord_ans = self.pm_equation(self.t_ans)
        return self.t_ans, self.coord_ans
    
    def solve(self):
        self.approximate_diffequation()
        self.interpolate()
        self.find_root()
        return self.t_ans, self.coord_ans
    
