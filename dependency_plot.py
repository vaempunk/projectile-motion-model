from numerical import integration
import plot
import matplotlib.pyplot as plt
import projectile_motion
import numpy as np
import surface_functions


def get_error(step_size):
    solution = projectile_motion.Solution(p, step_size, eps, ode_method='rk4')
    equation = projectile_motion.get_equation(p['m'], p['c'], p['x0'], p['y0'], p['v0'], p['angle'])
    w_analytical = np.array([equation(tn) for tn in solution.t])
    return projectile_motion.calculate_error(solution.w, w_analytical, step_size)


def get_time(angle):
    param = p.copy()
    param['angle'] = angle
    solution = projectile_motion.Solution(param, step_size, eps)
    return solution.t_ans

def get_x(angle):
    param = p.copy()
    param['angle'] = angle
    solution = projectile_motion.Solution(param, step_size, eps)
    return solution.w_ans[0]


p = {
    'm': 1,
    'c': 0.5,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(60),
    'surface_func': surface_functions.phi3
}
step_size = 0.01
eps = 1e-6

step_sizes = [0.1, 0.05, 0.025, 0.0125]
errors = [get_error(step_size) for step_size in step_sizes]

angles = np.linspace(0, np.pi/2, 50)
times = [get_time(angle) for angle in angles]
x_vals = [get_x(angle) for angle in angles]

solution = projectile_motion.Solution(p, step_size, eps, ode_method='rk4')
equation = projectile_motion.get_equation(p['m'], p['c'], p['x0'], p['y0'], p['v0'], p['angle'])
w_analytical = np.array([equation(tn) for tn in solution.t])

fig, axes = plt.subplots(nrows=2, ncols=2)

axes[0,0].plot(solution.w[:, 0], solution.w[:, 1], 'b-')
axes[0,0].plot(w_analytical[:, 0], w_analytical[:, 1], 'r-')
x_surface = np.linspace(min(solution.w[:, 0]) - 2, max(solution.w[:, 0]) + 2, 1000)
axes[0,0].plot(x_surface, [p['surface_func'](x) for x in x_surface], 'k-')
axes[0,0].set_title('Projectile motion')
# axes[0,0].set_xlabel('x')
axes[0,0].set_ylabel('y')

axes[0,1].plot(step_sizes, errors, '.-')
axes[0,1].set_title('Error by step size')
# axes[0,1].set_xlabel('step_size')
axes[0,1].set_ylabel('error')

axes[1,0].plot(np.degrees(angles), times)
axes[1,0].set_title('Time by angle')
# axes[1,0].set_xlabel('angle')
axes[1,0].set_ylabel('time')

axes[1,1].plot(np.degrees(angles), x_vals)
axes[1,1].set_title('x by angle')
# axes[1,1].set_xlabel('angle')
axes[1,1].set_ylabel('x')

plt.show()