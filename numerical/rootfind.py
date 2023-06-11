def find_root(equation, a, b, eps, method):
    if method == 'secant':
        return Secant(equation, a, b).find_root(eps=eps)
    if method == 'bisection':
        return Bisection(equation, a, b).find_root(eps=eps)


def sign(x):
    if x >= 0:
        return 1
    return -1


class Secant:

    def __init__(self, func, a, b) -> None:
        self.func = func
        self.x1 = a
        self.x2 = b

    def next(self):
        numerator = self.x1 * self.func(self.x2) - self.x2 * self.func(self.x1)
        denominator = self.func(self.x2) - self.func(self.x1)
        self.x1 = self.x2
        self.x2 = numerator / denominator
        return self.x2

    def find_root(self, eps):
        x0 = self.x1
        x1 = self.x2
        while abs(x1 - x0) > eps:
            x0 = x1
            x1 = Secant.next(self)
        return x1


class Bisection:

    def __init__(self, func, a, b) -> None:
        self.func = func
        self.x1 = a
        self.x2 = b

    def next(self):
        x = (self.x1 + self.x2) / 2
        if sign(self.func(x)) == sign(self.func(self.x1)):
            self.x1 = x
        else:
            self.x2 = x
        return x

    def find_root(self, eps, nmax=1000000000):
        x0 = self.x1
        x1 = self.x2
        for _ in range(nmax):
            x0 = x1
            x1 = self.next()
            if abs(x1 - x0) < eps:
                return x1
        raise ValueError("No root found")
