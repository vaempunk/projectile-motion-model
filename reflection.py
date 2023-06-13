import numpy as np
import matplotlib.pyplot as plt
import projectile_motion
import scipy.misc
from numerical import integration, interpolation, rootfind

# define parameters
def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
# def phi(x): return 0


params = {
    'mass': 1,
    'air_resist_coeff': 1,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(45),
    'surface_func': phi
}
step_size = 0.01
eps = 0.0001

# calculate initial parameters
ode = projectile_motion.get_ode(params)
t0, y0 = projectile_motion.get_cauchy_data(params)
above_surface = projectile_motion.get_above_surface(params)

# solve
t, y = integration.solve_ode(
    ode, t0, y0, step_size,
    predicate_func=above_surface,
    method='rk4'
)
polynomial = interpolation.interpolate(t[-4:], y[-4:], 'lagrange')
root_equation = projectile_motion.get_root_equation(params, polynomial)
t_ans = rootfind.find_root(root_equation, t[-2], t[-1], eps, 'bisection')
y_ans = polynomial(t_ans)

# get analytical solution
equation = projectile_motion.get_equation(params)
y_analytical = np.array([equation(tn) for tn in t])



# find and plot new reflect angle
dphi_dx = scipy.misc.derivative(phi, y_ans[0])
normal_angle = np.arctan(dphi_dx) + np.pi/2
print(np.degrees(normal_angle))
new_angle = 2 * normal_angle - np.arctan2(y_ans[3], y_ans[2]) + np.pi

plt.plot(y[:, 0], y[:, 1], 'b-')
plt.plot(y_analytical[:, 0], y_analytical[:, 1], 'r-')
x_surface = np.linspace(min(y[:, 0]) - 2, max(y[:, 0]) + 2, 1000)
plt.plot(x_surface, [phi(x) for x in x_surface], 'k-')
x_new = np.array([y_ans[0], 0.5 * np.cos(new_angle) + y_ans[0]])
y_new = np.array([y_ans[1], 0.5 * np.sin(new_angle) + y_ans[1]])
plt.plot(x_new, y_new, 'go-')
plt.show()