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

    def test_reset_relation(self):
        formula = "nu X. nu Y. mu Z. mu A. (X || (Y || (mu B. B && true)))"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z', 'A']})

    def test_reset_relation_2(self):
        formula = "nu X. nu Y. mu Z. mu A. (X || (Y || mu B. (B && X)))"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z', 'A', 'B']})

    def test_reset_relation_3(self):
        formula = "nu X. nu Y. mu Z. mu A. (A || (Z || mu B. (B && true)))"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['A']})

    def test_reset_relation_4(self):
        formula = "nu X. (mu Y. X && mu Z. X)"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z'], 'Y': ['Y']})

    def test_reset_relation_5(self):
        formula = "mu T. nu X. (mu Y. X && mu Z. X)"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        self.assertDictEqual(rc.find_relation(res), {'Z': ['Z'], 'Y': ['Y']})

    def test_reset_relation_6(self):
        formula = "nu X. mu Y. (Y && nu Z. mu T. mu R. Z)"
        parser = query.Parser(formula)
        res = parser.parse()
        tree = ft.create_tree(res)
        type_relation = ft.create_fixpoint_to_type_relation(tree)
        rc = ft.ResetRelationCreator(tree, type_relation)
        print(rc.find_relation(res))

