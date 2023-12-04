import unittest
import query
import fixpoint_tree as ft

from graph import Graph
from naive import NaiveChecker


class SanityTest(unittest.TestCase):
    def test_basic(self):
        g = Graph.from_file("./testcases/boolean/test.aut")
        q = query.TrueLiteral()
        checker = NaiveChecker(g)
        res = checker.solve_formula({}, q)
        self.assertIsNotNone(res)

    def test_tree(self):
        formula = "nu X. (mu Y. Y && mu Z. Z)"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        self.assertEqual(tree.label, "X")
        self.assertEqual(len(tree.children), 2)

    def test_tree_deep(self):
        formula = "nu X. (mu Y. Y && (mu Z. Z || nu Q. (mu V. Q && mu T. T)))"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        self.assertEqual(tree.label, "X")
        self.assertEqual(len(tree.children), 2)
        pr = ft.create_parent_relation(tree)
        self.assertDictEqual(pr, {'Y': 'X', 'Z': 'X', 'Q': 'X', 'V':'Q', 'T': 'Q'})
        tr = ft.create_fixpoint_to_type_relation(tree)
        self.assertDictEqual(tr, {'X': 'max', 'Y': 'min', 'Z': 'min', 'Q':'max', 
                                  'V': 'min', 'T': 'min'})
