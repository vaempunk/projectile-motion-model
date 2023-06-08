import numpy as np


class RK4:

    def __init__(self, f, t0, y0, h):
        self.f = f
        self.t = t0
        self.y = y0
        self.h = h

    def next(self) -> tuple:
        k1 = self.f(self.t, self.y)
        k2 = self.f(self.t + self.h/2, self.y + k1*self.h/2)
        k3 = self.f(self.t + self.h/2, self.y + k2*self.h/2)
        k4 = self.f(self.t + self.h, self.y + k3*self.h)
        self.t += self.h
        self.y += (k1 + 2*k2 + 2*k3 + k4) * self.h/6
        return self.t, self.y

    def next_while(self, condition_func) -> map:
        t_vals = []
        y_vals = []
        while condition_func(self.t, self.y):
            t, y = self.next()
            t_vals.append(t)
            y_vals.append(y)
        return np.array(t_vals), np.array(y_vals)


class Adams4:

    def __init__(self, f, t_vals, y_vals, h):
        assert len(t_vals) == len(
            y_vals) >= 4, 't_values and y_values must be same size >= 4'
        self.f = f
        self.t_vals = list(t_vals)
        self.y_vals = list(y_vals)
        self.h = h

    def next(self) -> tuple:
        t4, y4 = self.t_vals[-1], self.y_vals[-1]
        t3, y3 = self.t_vals[-2], self.y_vals[-2]
        t2, y2 = self.t_vals[-3], self.y_vals[-3]
        t1, y1 = self.t_vals[-4], self.y_vals[-4]
        t5 = t4 + self.h
        y5 = y4 + self.h * (55*self.f(t4, y4) - 59*self.f(t3, y3) +
                            37*self.f(t2, y2) - 9*self.f(t1, y1)) / 24
        self.t_vals.append(t5)
        self.y_vals.append(y5)
        return t5, y5

    def next_while(self, cond_func) -> map:
        while cond_func(self.t_vals[-1], self.y_vals[-1]):
            self.next()
        return np.array(self.t_vals), np.array(self.y_vals)
