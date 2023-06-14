import matplotlib.pyplot as plt
import numpy as np


def trajectories(w, w_analytical, surface_func):
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(w[:, 0], w[:, 1], w[:, 2], label='numerical')
    ax.plot(w_analytical[:, 0], w_analytical[:, 1], w_analytical[:, 2], label='analytical')

    x_surface = np.linspace(w[0, 0] + -2, w[-1, 0] + 2, 200)
    y_surface = np.linspace(w[0, 1] + -2, w[-1, 1] + 2, 200)
    x_mesh, y_mesh = np.meshgrid(x_surface, y_surface)
    z_mesh = surface_func(x_mesh, y_mesh)
    ax.plot_surface(x_mesh, y_mesh, z_mesh)
    ax.legend()
    plt.show()