import unittest
import numpy as np
import numerical.interpolation as interpolation


class TestLagrange(unittest.TestCase):

    def test_lagrange_1(self):
        x_vals = [0, 1, 2, 3, 4]
        y_vals = [0, 1, 4, 9, 16]
        polynomial = interpolation.interpolate_lagrange(x_vals, y_vals)
        self.assertListEqual(y_vals, [polynomial(x) for x in x_vals])

    def test_lagrange_2(self):
        x_vals = np.linspace(-5, 5, 100)
        y_vals = 3*x_vals**2 + 12*x_vals + 21
        polynomial = interpolation.interpolate_lagrange(x_vals, y_vals)
        for i, y in enumerate(y_vals):
            self.assertAlmostEqual(y, polynomial(x_vals[i]))


if __name__ == '__main__':
    unittest.main()
