import numpy as np


def solve_ode(f_ode, t0, y0, h, predicate_func, method):
    if method == 'rk4':
        return RK4(f_ode, t0, y0, h).next_while(predicate_func)
    if method == 'adams4':
        t_rk4, y_rk4 = RK4(f_ode, t0, y0, h).next_n(3)
        return Adams4(f_ode, t_rk4, y_rk4, h).next_while(predicate_func)


class RK4:

    def __init__(self, f, t0, y0, h):
        self.f = f
        self.tn = t0
        self.yn = y0
        self.h = h

    def next(self):
        k1 = self.f(self.tn, self.yn)
        k2 = self.f(self.tn + self.h/2, self.yn + k1*self.h/2)
        k3 = self.f(self.tn + self.h/2, self.yn + k2*self.h/2)
        k4 = self.f(self.tn + self.h, self.yn + k3*self.h)
        self.tn += self.h
        self.yn = self.yn + (k1 + 2*k2 + 2*k3 + k4) * self.h/6
        return self.tn, self.yn

    def next_while(self, predicate_func):
        t = [self.tn]
        y = [self.yn]
        while predicate_func(t[-1], y[-1]):
            tn, yn = self.next()
            t.append(tn)
            y.append(yn)
        return np.array(t), np.array(y)

    def next_n(self, n):
        t = [self.tn]
        y = [self.yn]
        for _ in range(n):
            tn, yn = self.next()
            t.append(tn)
            y.append(yn)
        return np.array(t), np.array(y)


class Adams4:

    def __init__(self, f, t, y, h):
        assert len(t) == len(y) >= 4, 't_values and y_values must be same size >= 4'
        self.f = f
        self.t = list(t)
        self.y = list(y)
        self.h = h

    def next(self):
        t4, y4 = self.t[-1], self.y[-1]
        t3, y3 = self.t[-2], self.y[-2]
        t2, y2 = self.t[-3], self.y[-3]
        t1, y1 = self.t[-4], self.y[-4]
        t5 = t4 + self.h
        y5 = y4 + self.h * (55*self.f(t4, y4) - 59*self.f(t3, y3) +
                            37*self.f(t2, y2) - 9*self.f(t1, y1)) / 24
        self.t.append(t5)
        self.y.append(y5)
        return t5, y5

    def next_while(self, predicate_func):
        while predicate_func(self.t[-1], self.y[-1]):
            self.next()
        return np.array(self.t), np.array(self.y)

    def next_n(self, n):
        for _ in range(n):
            self.next()
        return np.array(self.t), np.array(self.y)