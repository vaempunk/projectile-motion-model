import unittest
import numerical.integration as integration


class TestRungeKutta4(unittest.TestCase):

    def test_rk4_1(self):
        def f(t, y): return 3 * t**2
        h = .1
        rk4 = integration.RK4(f, .0, .0, h)
        for _ in range(10):
            t_val, y_val = rk4.next()
            self.assertAlmostEqual(t_val**3, y_val, delta=h**4)


if __name__ == '__main__':
    unittest.main()
