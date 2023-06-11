from numerical import integration, interpolation, rootfind
import projectile_motion
import numpy as np
import plot


# def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
def phi(x): return 0
params = {
    'm': 1,
    'c': 1,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'angle': np.radians(45),
    'phi': phi
}
step_size = 0.01
eps = 0.0001

ode = projectile_motion.get_ode(params)
y0 = projectile_motion.get_cauchy_data(params)
above_surface = projectile_motion.get_above_surface(params)
t, y = integration.solve_ode(
    f_ode=ode,
    t0=0,
    y0=y0,
    h=step_size,
    predicate_func=above_surface, 
    method='adams4'
)
polynomial = interpolation.interpolate(t[-4:], y[-4:], 'lagrange')
root_equation = projectile_motion.get_root_equation(params, polynomial)
t_ans = rootfind.find_root(root_equation, t[-2], t[-1], eps, 'secant')
y_ans = polynomial(t_ans)
print('Answer:', t_ans)
print('Angle:', np.degrees(projectile_motion.calculate_angle(params, y_ans, t_ans)))

equation = projectile_motion.get_equation(params)
y_analytical = np.array([equation(tn) for tn in t])

error = np.max(np.linalg.norm(y[-2:] - y_analytical[-2:], axis=1)) / step_size**4
print('Error:', error)
plot.plot_trajectories(y[:, :2], y_analytical[:, :2], phi)