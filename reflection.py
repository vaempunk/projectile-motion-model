import numpy as np
import matplotlib.pyplot as plt
import projectile_motion
import scipy.misc
import surface_functions

# define parameters
# def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
# def phi(x): return 0
phi = surface_functions.phi3

params = {
    'mass': 1,
    'air_resist_coeff': 0.5,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(60),
    'surface_func': phi
}
step_size = 0.01
eps = 1e-6
num_hits = 4
dx = 1e-15

xmin = params['x0']
xmax = params['x0']

for _ in range(num_hits):
    solution = projectile_motion.Solution(params, step_size, eps)
    # dphi_dx = scipy.misc.derivative(phi, solution.y_ans[0])
    dphi_dx = (phi(solution.y_ans[0] + dx) - phi(solution.y_ans[0])) / dx
    phi_angle = np.arctan(dphi_dx) # + np.pi/2
    new_angle = 2*phi_angle - np.arctan2(solution.y_ans[3], solution.y_ans[2]) # - np.pi
    plt.plot(solution.get_solved_y()[:, 0], solution.get_solved_y()[:, 1])
    params['v0'] = np.sqrt(solution.y_ans[2]**2 + solution.y_ans[3]**2)
    params['x0'] = solution.y_ans[0]
    params['y0'] = phi(solution.y_ans[0])
    params['angle'] = new_angle % (2*np.pi)
    if xmax < params['x0']:
        xmax = params['x0']
    if xmin > params['x0']:
        xmin = params['x0']

x_surface = np.linspace(xmin - 2, xmax + 2, 500)
y_surface = np.array([phi(x) for x in x_surface])
plt.plot(x_surface, y_surface, 'k-')

plt.show()