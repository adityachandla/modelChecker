import unittest
import copy
import query
import fixpoint_tree as ft
from fast_set import FastSet

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

    def test_reset_relation(self):
        formula = "nu X. nu Y. mu Z. mu A. (X || (Y || (mu B. B && true)))"
        parser = query.Parser(formula)
        res = parser.parse()
        rc = ft.ResetRelationCreator(res)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z', 'A']})

    def test_reset_relation_2(self):
        formula = "nu X. nu Y. mu Z. mu A. (X || (Y || mu B. (B && X)))"
        parser = query.Parser(formula)
        res = parser.parse()
        rc = ft.ResetRelationCreator(res)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z', 'A', 'B']})

    def test_reset_relation_3(self):
        formula = "nu X. nu Y. mu Z. mu A. (A || (Z || mu B. (B && true)))"
        parser = query.Parser(formula)
        res = parser.parse()
        rc = ft.ResetRelationCreator(res)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['A']})

    def test_reset_relation_4(self):
        formula = "nu X. (mu Y. X && mu Z. X)"
        parser = query.Parser(formula)
        res = parser.parse()
        rc = ft.ResetRelationCreator(res)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z'], 'Y': ['Y']})


class FastSetTests(unittest.TestCase):
    def test_all_set(self):
        one = FastSet(66, True)
        self.assertEqual(len(one.get_as_list()), 66)

    def test_empty(self):
        one = FastSet(66, False)
        self.assertEqual(len(one.get_as_list()), 0)

    def test_addition(self):
        one = FastSet(66, False)
        one.add(33)
        self.assertListEqual(one.get_as_list(), [33])
        one.add(65)
        self.assertListEqual(one.get_as_list(), [33, 65])

    def test_any_satisfying(self):
        one = FastSet(66, False)
        self.assertFalse(one.any_satisfying())
        one.add(65)
        self.assertTrue(one.any_satisfying())

    def test_union(self):
        one = FastSet(66, False)
        one.add(33)
        two = FastSet(66, False)
        two.add(44)
        one.union(two)
        self.assertListEqual(one.get_as_list(), [33,44])

    def test_intersection(self):
        one = FastSet(66, False)
        one.add(33)
        one.add(8)
        two = FastSet(66, False)
        two.add(44)
        two.add(8)
        one.intersection(two)
        self.assertListEqual(one.get_as_list(), [8])

    def test_copy(self):
        one = FastSet(66, False)
        two = copy.deepcopy(one)
        two.add(33)
        self.assertListEqual(one.get_as_list(), [])

    def test_equality(self):
        one = FastSet(66, False)
        two = FastSet(66, False)
        self.assertEqual(one, two)

