import matplotlib.pyplot as plt
import numpy as np


def trajectories(y, y_analytical, surface_func) -> None:
    plt.plot(y[:, 0], y[:, 1], 'b-')
    plt.plot(y_analytical[:, 0], y_analytical[:, 1], 'r-')

    x_surface = np.linspace(min(y[:, 0]) - 2, max(y[:, 0]) + 2, 1000)
    plt.plot(x_surface, [surface_func(x) for x in x_surface], 'k-')

    plt.show()

def error(steps_sizes, errors):
    plt.plot(steps_sizes, errors, '.-')
    plt.show()