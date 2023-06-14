import numpy as np
import plot
import projectile_motion
import surface_functions


# define parameters
phi = surface_functions.phi2
p = {
    'm': 1,
    'c': 1,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(45),
    'surface_func': phi
}
step_size = 0.01
eps = 1e-6


solution = projectile_motion.Solution(p, step_size, eps)
print('Answer:', solution.t_ans, solution.w_ans[0], solution.w_ans[1])

# get analytical solution
equation = projectile_motion.get_equation(
    p['m'], p['c'],
    p['x0'], p['y0'], p['v0'],
    p['angle'])
w_analytical = np.array([equation(tn) for tn in solution.t])

# find error
error = projectile_motion.calculate_error(solution.w, w_analytical, step_size)
print(f'Error: {error}')

# plot numerical and analytical trajectories
w = solution.w.copy()
w[-1] = solution.w_ans
w_analytical[-1] = solution.w_ans
plot.trajectories(w, w_analytical, phi)


