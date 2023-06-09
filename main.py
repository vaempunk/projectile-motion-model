from analytical_solution import AnalyticalSolution
from numerical_solution import NumericalSolution
import numpy as np
import plot

def phi(x): return (x-5)**2 - 4 if 3 < x <= 7 else 0
params = {
    'm': 1,
    'c': 1,
    'x0': 0,
    'y0': 0,
    'v0': 10,
    'theta': np.radians(45),
    'phi': phi
}

step_size = 0.11
eps = 0.0001

numerical = NumericalSolution(params, step_size, eps)
numerical.solve()

t_vals = numerical.t_vals
y_vals = numerical.y_vals


analytical = AnalyticalSolution(params)
y_vals_analytical = analytical.calculate_values(t_vals)

print('Answer:', numerical.t_ans)

const = np.max(np.linalg.norm(y_vals[-1:] - y_vals_analytical[-1:], axis=1)) / step_size**4
print('Const:', const)

plot.plot_trajectories(y_vals[..., :2], y_vals_analytical[..., :2], phi)

