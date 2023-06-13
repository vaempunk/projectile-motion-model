import numpy as np
import plot
import projectile_motion
import surface_functions



# define parameters
phi = surface_functions.phi3
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
eps = 1e-6


solution = projectile_motion.Solution(params, step_size, eps)
print(f'Answer: {solution.t_ans}, ({solution.y_ans[0]}, {solution.y_ans[1]})')

# get analytical solution
equation = projectile_motion.get_equation(
    params['mass'], params['air_resist_coeff'],
    params['x0'], params['y0'], params['v0'],
    params['angle'])
y_analytical = np.array([equation(tn) for tn in solution.t])

# find error
error = projectile_motion.calculate_error(solution.y, y_analytical, step_size)
print(f'Error: {error}')

# plot numerical and analytical trajectories
y = solution.y.copy()
y[-1] = solution.y_ans
y_analytical[-1] = solution.y_ans
plot.trajectories(y, y_analytical, phi)


