import numpy as np
import matplotlib.pyplot as plt
import projectile_motion3d
import scipy.misc

# phi = lambda x, y: np.zeros(x.shape)
phi = lambda x, y: y
p = {
    'm': 1,
    'c': 0.5,
    'x0': 0,
    'y0': 0,
    'z0': 0,
    'v0': 20,
    'anglexy': np.radians(60),
    'anglexz': np.radians(45),
    'surface_func': phi
}
step_size = 0.01
eps = 1e-6
num_hits = 8
dx = 1e-15
dy = 1e-15

xmin = p['x0']
xmax = p['x0']
ymin = p['y0']
ymax = p['y0']
ax = plt.figure().add_subplot(projection='3d')

for _ in range(num_hits):
    solution = projectile_motion3d.Solution(p, step_size, eps)
    x, y, z, vx, vy, vz = solution.w_ans
    # print(solution.w_ans)
    dphi_dx = (phi(x + dx, y) - phi(x, y)) / dx
    dphi_dy = (phi(x, y + dy) - phi(x, y)) / dy
    n = np.array([-dphi_dx, -dphi_dy, 1])
    n /= np.linalg.norm(n)
    v = np.array([vx, vy, vz])
    v_new = v - 2 * np.dot(v, n) * n
    # ax.plot([x, v_new[0]], [y, v_new[1]], [z, v_new[2]])
    # print(v_new)
    anglexy = np.arctan2(v_new[2], v_new[0]) 
    anglexz = np.arctan2(v_new[1], v_new[0]) 
    print(np.degrees(anglexy), np.degrees(anglexz))
    # print(np.degrees(anglexy), np.degrees(anglexz))
    ax.plot(solution.get_solution_pts()[:, 0], solution.get_solution_pts()[:, 1], solution.get_solution_pts()[:, 2])
    p['v0'] = np.sqrt(vx**2 + vy**2 + vz**2)
    p['x0'] = x
    p['y0'] = y
    p['z0'] = phi(x, y)
    p['anglexy'] = anglexy % (2*np.pi)
    p['anglexz'] = anglexz % (2*np.pi)
    if xmax < p['x0']:
        xmax = p['x0']
    if xmin > p['x0']:
        xmin = p['x0']
    if ymax < p['y0']:
        ymax = p['y0']
    if ymin > p['y0']:
        ymin = p['y0']

x_surface = np.linspace(xmin - 2, xmax + 2, 200)
y_surface = np.linspace(ymin - 2, ymax + 2, 200)
X, Y = np.meshgrid(x_surface, y_surface)
Z = phi(X, Y)
ax.plot_surface(X, Y, Z,)

plt.show()