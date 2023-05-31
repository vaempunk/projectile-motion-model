import numpy as np
import numerical.diffequation as diffequation
import numerical.interpolation as interpolation
import numerical.rootfind as rootfind
import matplotlib.pyplot as plt
import analytical


g = 9.81
t_max = 100000000
t_initial = 0.0
step_size = 0.0001

x0, y0 = 0, 0
v0 = 10
theta = np.radians(45)
m = 1
c = 1
def phi(x): return -(x-6)**2 if 4 < x <= 6 else 0


def get_projectile_motion_equation(x0, y0, v0, angle, m, c, phi=lambda x: 0):
    def projectile_motion_equation(t, y):
        z1, _, z2, _ = y
        dz1 = -c/m * z1
        dx = z1
        dz2 = -(c*z2 + m*g) / m
        dy = z2
        return np.array([dz1, dx, dz2, dy])
    return projectile_motion_equation


projectile_motion = get_projectile_motion_equation(
    x0, y0, v0, theta, m, c, phi)

# find motion points using rk4 and adams4
rk4 = diffequation.RK4(projectile_motion, t_initial, np.array(
    [v0*np.cos(theta), x0, v0*np.sin(theta), y0]), step_size)
system_solution_points = [rk4.next() for _ in range(4)]
adams4 = diffequation.Adams4(
    projectile_motion, system_solution_points, step_size)
t_ans = 0
while t_ans < t_max:
    t_ans, points = adams4.next()
    system_solution_points.append((t_ans, points))
    _, x, _, y = points
    if y < phi(x):
        break

# rearrange motion points
motion_points = [(t, np.array([points[1], points[3]]))
                 for t, points in system_solution_points]
last_motion_points = motion_points[-4:]

# interpolate trajectory
def polinomial_y(t):
    return interpolation.interpolate_lagrange(last_motion_points)(t)[1]


# find root
secant = rootfind.Secant(
    polinomial_y, last_motion_points[-2][0], last_motion_points[-1][0])
t_ans = secant.find_root(0.000001)

print('t =', t_ans)
print('end point coords =', interpolation.interpolate_lagrange(last_motion_points)(t_ans))

motion_coords = [(points[0], points[1]) for t, points in motion_points]
x_vals = [point[0] for point in motion_coords]
y_vals = [point[1] for point in motion_coords]

ans, x, y = analytical.calculate_fly(x0, y0, v0, theta, m, c, phi)
t_vals_analytical = np.linspace(0, ans, len(motion_coords))
coordinates_equation = analytical.get_coordinates_equations(x0, y0, v0, theta, m, c)
analytical_solution = [coordinates_equation(t) for t in t_vals_analytical]
x_vals_analytical, y_vals_analytical = zip(*analytical_solution)

# plot trajectory
x_line = np.linspace(0, max(x_vals) + 5, 10000)
plt.plot(x_vals, y_vals, 'b-')
plt.plot(x_vals_analytical, y_vals_analytical, 'r-')
plt.plot(x_line, [phi(x) for x in x_line], 'k-')
plt.show()