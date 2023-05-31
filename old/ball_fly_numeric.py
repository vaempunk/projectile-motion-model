import numpy as np
import matplotlib.pyplot as plt

import ball_fly_analytic


t_max = 3600000


x0, y0 = 0, 0
v0 = 10
theta = np.radians(45)
m = 1
c = 1
g = 9.81
phi = lambda x: 0
assert c != 0

def get_fly_equation_system(x0, y0, v0, angle, m, c, phi=lambda x: 0):
    def fly_equation_system(t, y):
        dy0 = -c/m * y[0]
        dy1 = y[0]
        dy2 = -(c*y[2] + m*g) / m
        dy3 = y[2]
        return np.array([dy0, dy1, dy2, dy3])
    return fly_equation_system

t = 0.0
t_old = t
res = np.array([v0*np.cos(theta), x0, v0 * np.sin(theta), y0])
res_old = res
h = 0.0001
history = [(t, res[1], res[3])]
fly_equation_system = get_fly_equation_system(x0, y0, v0, theta, m, c, phi)
while t < t_max and res[3] >= phi(res[1]):
        t_old = t
        res_old = res.copy()
        k1 = fly_equation_system(t, res)
        k2 = fly_equation_system(t + h/2, res + h/2*k1)
        k3 = fly_equation_system(t + h/2, res + h/2*k2)
        k4 = fly_equation_system(t + h, res + h*k3)
        res += h/6 * (k1 + 2*k2 + 2*k3 + k4)
        t += h
        history.append((t, res[1], res[3]))
assert t < t_max

# interpolation of `history`
def polinom(t, ts, ys):
    l = []
    for i in range(len(ts)):
        li = 1
        for j in range(0, i):
            li *= (t - ts[j]) / (ts[i] - ts[j])
        for j in range(i+1, len(ts)):
            li *= (t - ts[j]) / (ts[i] - ts[j])
        l.append(li)
    ll = 0.0
    for i in range(len(ys)):
        ll += l[i] * ys[i]
    return ll

ts, xs, ys = zip(*history[-5:])
t_before, x_before, y_before = history[-1]
t_after, x_after, y_after = history[-2]

eps = 0.00000001
def res_func(t):
    return polinom(t, ts, ys) - phi(polinom(t, ts, xs))

ans = t_after
ans_old = t_before
while np.abs(ans - ans_old) > eps:
    new_ans = ans_old - res_func(ans_old) * (ans - ans_old) / (res_func(ans) - res_func(ans_old))
    ans_old = ans
    ans = new_ans 
print('Время полета:', ans)
print('x:', polinom(ans, ts, xs))
print('y:', polinom(ans, ts, ys))
