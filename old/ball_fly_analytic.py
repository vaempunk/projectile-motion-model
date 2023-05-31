import numpy as np
import scipy.optimize as spo


T_MAX = 3600000
g = 9.81

def get_coordinates_equations(x0, y0, v0, angle, m, c):
    def calculate_coordinates(t):
        x = x0 + m/c*v0*np.cos(angle)*(-np.exp(-c/m*t) + 1)
        y = y0 + m/c * ((m/c*g + v0*np.sin(angle)) * (1 - np.exp(-c/m*t)) - g*t)
        return x, y
    return calculate_coordinates

def get_fly_equation(x0, y0, v0, angle, m, c, phi=lambda x: 0):
    assert c != 0, ('air resistance coefficient must be non-zero')
    def fly_equation(t):
        calculate_coordinates = get_coordinates_equations(x0, y0, v0, angle, m, c)
        x, y = calculate_coordinates(t)
        return y - phi(x)
    return fly_equation

def calculate_fly(x0, y0, v0, angle, m, c, phi=lambda x: 0):
    fly_equation = get_fly_equation(x0, y0, v0, angle, m, c, phi)

    t_initial = 1
    ans = spo.fsolve(fly_equation, t_initial)
    while ans == 0:
        t_initial *= 2
        ans = spo.fsolve(fly_equation, t_initial)
        if t_initial > T_MAX / 2:
            print('fly time not found')
            break
    calculate_coordinates = get_coordinates_equations(x0, y0, v0, angle, m, c)
    x, y = calculate_coordinates(ans)
    return ans, x, y

def main():
    # initial conditions
    x0, y0 = 0, 0
    v0 = 10
    theta = np.radians(45)
    m = 1
    c = 1
    phi = lambda x: 0

    t, x, y = calculate_fly(x0, y0, v0, theta, m, c, phi)
    print('time:', t)
    print('x:', x)
    print('y:', y)

    
if __name__ == '__main__':
    main()
