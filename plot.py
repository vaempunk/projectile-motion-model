import matplotlib.pyplot as plt
import numpy as np


def plot_trajectories(points_numerical, points_analytic, ground_func) -> None:
    x_vals_numeric, y_vals_numeric = zip(*points_numerical)
    plt.plot(x_vals_numeric, y_vals_numeric, 'b-')
    x_vals_analytic, y_vals_analytic = zip(*points_analytic)
    plt.plot(x_vals_analytic, y_vals_analytic, 'r-')

    x_vals_ground = np.linspace(min(points_numerical[:, 0]) - 2, max(points_numerical[:, 0]) + 2, 1000)
    plt.plot(x_vals_ground, [ground_func(x) for x in x_vals_ground], 'k-')

    plt.show()

def plot_norm(t_vals, norm):
    plt.plot(t_vals, norm, 'g.-')
    plt.show()