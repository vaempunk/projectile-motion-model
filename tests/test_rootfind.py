import unittest
import numerical.rootfind as rootfind
import math

class TestSecant(unittest.TestCase):

    def test_secant_1(self):
        def f(x): return (x-3)**2 - 4
        secant = rootfind.Secant(f, 3, 7)
        self.assertAlmostEqual(5, secant.find_root(0.0001), delta=0.0001)

    def test_secant_2(self):
        def f(x): return math.e ** x - 1
        secant = rootfind.Secant(f, -3, 3)
        self.assertAlmostEqual(0, secant.find_root(0.0001), delta=0.0001)