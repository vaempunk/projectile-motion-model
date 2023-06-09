# Постановка задачи

Дано уравнение полета снаряда:
$$
\begin{cases}

ma_x = - cv_x \\
v_x(0) = v_0 \cos{\theta} \\
x(0) = x_0 \\
ma_y = -cv_y - mg \\
v_y(0) = v_0 \sin{\theta} \\
y(0) = y_0

\end{cases}
$$

Необходимо найти такое $t_{ans}$, что $y(t_{ans}) = \phi(x(t_{ans}))$

# Аналитическое решение

Уравнение принимает форму:

$$
y_0 + \frac{m}{c}((\frac{m}{c}g + v_0 \sin{\theta})(1 - e^{-\frac{c}{m}t}) - gt)
- \phi(x_0 + \frac{m}{c}v_0 \cos{\theta}(1 - e^{-\frac{c}{m}t})) = 0
$$