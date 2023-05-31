class RK4:
    def __init__(self, func, t_initial, y_initial, step_size):
        self.func = func
        self.t = t_initial
        self.y = y_initial
        self.step = step_size
    def next(self) -> tuple:
        k1 = self.func(self.t, self.y)
        k2 = self.func(self.t + self.step/2, self.y + k1*self.step/2)
        k3 = self.func(self.t + self.step/2, self.y + k2*self.step/2)
        k4 = self.func(self.t + self.step, self.y + k3*self.step)
        self.t += self.step
        self.y += (k1 + 2*k2 + 2*k3 + k4) * self.step/6
        return self.t, self.y
    
class Adams4:
    def __init__(self, func, components_initial, step_size):
        assert len(components_initial) >= 4
        self.func = func
        self.components = components_initial.copy()
        self.step = step_size
    def next(self) -> tuple:
        t4, y4 = self.components[-1]
        t3, y3 = self.components[-2]
        t2, y2 = self.components[-3]
        t1, y1 = self.components[-4]
        y5 = y4 + self.step * (55*self.func(t4, y4) - 59*self.func(t3, y3) + 37*self.func(t2, y2) - 9*self.func(t1, y1)) / 24
        t5 = t4 + self.step
        self.components.append((t5, y5))
        return t5, y5