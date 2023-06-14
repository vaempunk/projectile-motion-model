import numpy as np
import matplotlib.pyplot as plt
import projectile_motion
import scipy.misc
import surface_functions

phi = surface_functions.phi1
p = {
    'm': 1,
    'c': 0,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(30),
    'surface_func': phi
}
step_size = 0.01
eps = 1e-6
num_hits = 10
dx = 1e-15

xmin = p['x0']
xmax = p['x0']

for _ in range(num_hits):
    solution = projectile_motion.Solution(p, step_size, eps)
    # dphi_dx = scipy.misc.derivative(phi, solution.y_ans[0])
    dphi_dx = (phi(solution.w_ans[0] + dx) - phi(solution.w_ans[0])) / dx
    phi_angle = np.arctan(dphi_dx) # + np.pi/2
    new_angle = 2*phi_angle - np.arctan2(solution.w_ans[3], solution.w_ans[2]) # - np.pi
    plt.plot(solution.get_solution_pts()[:, 0], solution.get_solution_pts()[:, 1])
    p['v0'] = np.sqrt(solution.w_ans[2]**2 + solution.w_ans[3]**2)
    p['x0'] = solution.w_ans[0]
    p['y0'] = phi(solution.w_ans[0])
    p['angle'] = new_angle % (2*np.pi)
    if xmax < p['x0']:
        xmax = p['x0']
    if xmin > p['x0']:
        xmin = p['x0']

x_surface = np.linspace(xmin - 2, xmax + 2, 500)
y_surface = np.array([phi(x) for x in x_surface])
plt.plot(x_surface, y_surface, 'k-')

plt.show()