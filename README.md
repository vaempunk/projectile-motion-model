# Projectile motion with air resistance problem

## Main problem

Given equation:

$ma_x = - cv_x$

$v_x(0) = v_0 \cos{\theta}$

$x(0) = x_0$

$ma_y = -cv_y - mg$

$v_y(0) = v_0 \sin{\theta}$

$y(0) = y_0$

Find $t_{ans}$: $y(t_{ans}) = \phi(x(t_{ans}))$

## Analytical solution

$y_0 + \frac{m}{c}((\frac{m}{c}g + v_0 \sin{\theta})(1 - e^{-\frac{c}{m}t}) - gt)c - \phi(x_0 + \frac{m}{c}v_0 \cos{\theta}(1 - e^{-\frac{c}{m}t})) = 0$

## Numerical solution

1. Solve ODE using Runge-Kutta 4 or Adams method
2. Interpolate last 4 points using Lagrange polynomial
3. Find solution using bisection or secant method

## Reverse problem

For each surface hit coordinate $x$, find launch angle(s) $\theta$

## 3D projectile motion

Find surface hit coordinates $x$, $y$, $z$ and motion time $t$ in 3 dimensions

## Reflection

Find motion of a projectile that is reflected from surface
