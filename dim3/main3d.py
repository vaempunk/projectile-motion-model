import numpy as np
import plot3d
import projectile_motion3d


# define parameters
phi = lambda x, y: np.sin(x+y)
p = {
    'm': 1,
    'c': 1,
    'x0': 0,
    'y0': 0,
    'z0': 0,
    'v0': 10,
    'anglexy': np.radians(60),
    'anglexz': np.radians(30),
    'surface_func': phi
}
step_size = 0.01
eps = 1e-6


solution = projectile_motion3d.Solution(p, step_size, eps)
print(f'Answer: {solution.t_ans}, ({solution.w_ans[0]}, {solution.w_ans[1]}, {solution.w_ans[2]})')

# get analytical solution
equation = projectile_motion3d.get_equation(
    p['m'], p['c'],
    p['x0'], p['y0'], p['z0'],
    p['v0'], p['anglexy'], p['anglexz'])
w_analytical = np.array([equation(tn) for tn in solution.t])

# find error
error = projectile_motion3d.calculate_error(solution.w, w_analytical, step_size)
print(f'Error: {error}')

# plot numerical and analytical trajectories
w = solution.w.copy()
w[-1] = solution.w_ans
w_analytical[-1] = solution.w_ans
plot3d.trajectories(w, w_analytical, phi)


