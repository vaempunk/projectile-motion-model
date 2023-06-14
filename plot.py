import matplotlib.pyplot as plt
import numpy as np


def trajectories(w, w_analytical, surface_func) -> None:
    plt.plot(w[:, 0], w[:, 1], 'b-')
    plt.plot(w_analytical[:, 0], w_analytical[:, 1], 'r-')

    x_surface = np.linspace(min(w[:, 0]) - 2, max(w[:, 0]) + 2, 1000)
    plt.plot(x_surface, [surface_func(x) for x in x_surface], 'k-')

    plt.show()
