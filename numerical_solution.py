import numpy as np
from numerical import *
import analytical_solution
import plot


# constants
g = 9.81
step_size = 0.01

# parameters
x0, y0 = 0, 0
v0 = 10
theta = np.radians(45)
m = 1
c = 1
def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0


def get_projectile_motion_equation(m, c):
    def projectile_motion_equation(t, y):
        z1, _, z2, _ = y
        dz1 = -c/m * z1
        dx = z1
        dz2 = -(c*z2 + m*g) / m
        dy = z2
        return np.array([dz1, dx, dz2, dy])
    return projectile_motion_equation


projectile_motion = get_projectile_motion_equation(m, c)

# find motion points using rk4 and adams4
t_vals = np.array([0.0])
y_vals = np.array([[v0*np.cos(theta), x0, v0*np.sin(theta), y0],])
print(y_vals)
rk4 = diffequation.RK4(projectile_motion, t_vals[0], y_vals[0], step_size)
t_vals[len(t_vals):], y_vals[len(y_vals):] = zip(*(rk4.next() for _ in range(4)))
adams4 = diffequation.Adams4(
    projectile_motion, t_vals, y_vals, step_size)
t_vals_adams, y_vals_adams = adams4.next_while(
    lambda _, solution_points: solution_points[3] > phi(solution_points[1]))
t_vals = np.append(t_vals, t_vals_adams)
y_vals = np.append(y_vals, y_vals_adams, axis=0)

# get (x, y) from solution
motion_points = y_vals[:, [1, 3]]

# interpolate motion points
polynomial = interpolation.interpolate_lagrange(
    t_vals[-4:], motion_points[-4:])


def motion_equation(t):
    x, y = polynomial(t)
    return y - phi(x)


# find root
secant = rootfind.Secant(motion_equation, t_vals[-2], t_vals[-1])
t_ans = secant.find_root(0.000001)

print('t =', t_ans)
print('end point coords =', polynomial(t_ans))

t_ans_analytical, x_ans_analytical, y_ans_analytical = analytical_solution.calculate_fly(
    x0, y0, v0, theta, m, c, phi)
print('analytical t =', t_ans_analytical)
print('analytical end point coords =', (x_ans_analytical, y_ans_analytical))

coordinates_equation = analytical_solution.get_coordinates_equations(
    x0, y0, v0, theta, m, c)
motion_points_analytic = np.array(
    [coordinates_equation(t) for t in t_vals])

# plot trajectory
plot.plot_trajectories(motion_points, motion_points_analytic, phi)

# compare rk-adams method and analytical
diff = motion_points - motion_points_analytic
norm = np.linalg.norm(diff, axis=1) / step_size**4

plot.plot_norm(t_vals, norm)
