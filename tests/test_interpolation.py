import unittest
import numpy as np
import numerical.interpolation as interpolation


class TestLagrange(unittest.TestCase):

    def test_lagrange_1(self):
        x = [0, 1, 2, 3, 4]
        y = [0, 15, 21, 46, 64]
        polynomial = interpolation.interpolate_lagrange(x, y)
        self.assertListEqual(y, [polynomial(x) for x in x])

    def test_lagrange_2(self):
        def f(x): return np.exp(x) + x**2 - 1
        x = np.linspace(-5, 5, 10)
        y = f(x)
        polynomial = interpolation.interpolate_lagrange(x, y)
        err_bound = (x[-1] - x[0])**len(x) / np.product(np.arange(1, len(x) + 1)) * np.exp(5)
        for xn in np.linspace(-5, 5, 100):
            self.assertAlmostEqual(f(xn), polynomial(xn), delta=err_bound)


if __name__ == '__main__':
    unittest.main()
