import unittest

from graph import Graph
from query import TrueLiteral
from naive import NaiveChecker


class SanityTest(unittest.TestCase):
    def test_basic(self):
        g = Graph.from_file("./testcases/boolean/test.aut")
        query = TrueLiteral()
        checker = NaiveChecker(g)
        res = checker.solve_formula({}, query)
        self.assertIsNotNone(res)
