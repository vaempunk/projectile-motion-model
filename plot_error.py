from numerical import integration
import plot
import projectile_motion
import numpy as np

def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
params = {
    'mass': 1,
    'air_resist_coeff': 1,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(45),
    'surface_func': phi
}
ode = projectile_motion.get_ode(params)
t0, y0 = projectile_motion.get_cauchy_data(params)
above_surface = projectile_motion.get_above_surface(params)
equation = projectile_motion.get_equation(params)
step_sizes = [0.1, 0.05, 0.025, 0.0125]
errors = []
for step_size in step_sizes:
    t, y = integration.solve_ode(
        ode, t0, y0, step_size,
        predicate_func=above_surface,
        method='rk4'
    )
    y_analytical = np.array([equation(tn) for tn in t])
    error = projectile_motion.calculate_error(y, y_analytical, step_size)
    errors.append(error)
plot.error(step_sizes, errors)