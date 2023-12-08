from __future__ import annotations
from dataclasses import dataclass

import query


@dataclass
class Node:
    label: str
    fixpoint_type: str # This can have two values "min" or "max"
    is_empty: bool
    children: list[Node]
    parent: Node


# Take in Formula
# Output the variables that need to be reset for that variable
# {"X" : ["Y", "Z"], "P": ["A","B"]}
class ResetRelationCreator:
    def __init__(self, tree: Node, type_relation: dict[str,str]):
        self.parent_relation = create_parent_relation(tree)
        self.formula_types = type_relation

    def find_relation(self, formula: query.Formula) -> dict[str, list[str]]:
        match formula:
            case query.TrueLiteral() | query.FalseLiteral():
                return {}
            case query.LogicFormula(left, right, _):
                left_dict = self.find_relation(left)
                right_dict = self.find_relation(right)
                return {**left_dict, **right_dict}
            case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
                return self.find_relation(f)
            case query.MuFormula(var, formula):
                if var.name not in self.parent_relation:
                    return {}
                surrounding = self.parent_relation[var.name]
                if surrounding is not None and self.formula_types[surrounding] == "max":
                    return {var.name: self.check_subformulas(query.MuFormula(var, formula))}
                return {}
            case query.NuFormula(var, formula):
                return self.find_relation(formula)
            case query.RecursionVariable(name):
                return {}
            case _:
                raise AssertionError()

    def check_subformulas(self, formula: query.Formula) -> list[str]:
        match formula:
            case query.TrueLiteral() | query.FalseLiteral():
                return []
            case query.LogicFormula(left, right, _):
                left_list = self.check_subformulas(left)
                right_list = self.check_subformulas(right)
                return [*left_list, *right_list]
            case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
                return self.check_subformulas(f)
            case query.MuFormula(var, formula):
                open_variables = self.find_open_variables(formula, {var.name})
                other_variables_to_reset = self.check_subformulas(formula)
                if len(open_variables) > 0:
                    return [var.name, *other_variables_to_reset]
                return other_variables_to_reset
            case query.NuFormula(var, formula):
                return self.check_subformulas(formula)
            case query.RecursionVariable(name):
                return []
            case _:
                raise AssertionError()

    def find_open_variables(self, formula: query.Formula, bound: set[str]) -> list[str]:
        match formula:
            case query.TrueLiteral() | query.FalseLiteral():
                return {}
            case query.LogicFormula(left, right, _):
                left_list = self.find_open_variables(left, bound)
                right_list = self.find_open_variables(right, bound)
                return [*left_list, *right_list]
            case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
                return self.find_open_variables(f, bound)
            case query.MuFormula(var, formula) | query.NuFormula(var, formula):
                bound.add(var.name)
                open_variables = self.find_open_variables(formula, bound)
                bound.remove(var.name)
                return open_variables
            case query.RecursionVariable(name):
                if name in bound:
                    return []
                return [name]
            case _:
                raise AssertionError()



## This gives parent relation. Ex: {X: Y, Y: T} for 
## T
## |
## Y
## |
## X
def create_parent_relation(tree_root: Node) -> dict[str, str]:
    creator = ParentRelationCreator(tree_root)
    return creator.generate_relation()


class ParentRelationCreator:
    def __init__(self, root: Node):
        self.root = root

    def generate_relation(self) -> dict[str, str]:
        if self.root is None:
            return {}
        self.relation = dict()
        self._generate_relation(self.root)
        return self.relation

    def _generate_relation(self, node: Node):
        if not node.is_empty:
            parent = self.get_parent(node)
            if parent is not None:
                self.relation[node.label] = parent.label
        if node.children is None:
            return
        for c in node.children:
            self._generate_relation(c)

    def get_parent(self, node: Node):
        p = node.parent
        while p is not None and p.is_empty:
            p = p.parent
        return p

## This gives relation from label to min/max. Ex: {X: "max", Y: "min"}
def create_fixpoint_to_type_relation(tree_root: Node) -> dict[str, str]:
    tr = TypeRelationCreator(tree_root)
    return tr.generate_relation()


class TypeRelationCreator:
    def __init__(self, root: Node):
        self.root = root

    def generate_relation(self) -> dict[str, str]:
        if self.root is None:
            return {}
        self.relation = dict()
        self._generate_relation(self.root)
        return self.relation

    def _generate_relation(self, node: Node):
        if not node.is_empty:
            self.relation[node.label] = node.fixpoint_type
        if node.children is None:
            return
        for c in node.children:
            self._generate_relation(c)

def create_tree(formula: query.Formula) -> Node:
    match formula:
        case query.TrueLiteral() | query.FalseLiteral():
            return None
        case query.RecursionVariable(name):
            return None
        case query.LogicFormula(left, right, is_and):
            left_root = create_tree(left)
            right_root = create_tree(right)
            # We need to filter in case the children don't contain mu or nu
            children = list(filter(lambda x: x is not None, [left_root, right_root]))
            empty_root = Node(None, None, True, children, None)
            for c in children:
                c.parent = empty_root
            return empty_root
        case query.BoxFormula(label, formula):
            return create_tree(formula)
        case query.DiamondFormula(label, formula):
            return create_tree(formula)
        case query.NuFormula(variable, formula):
            child_node = create_tree(formula)
            if child_node is None:
                return Node(variable.name, "max", False, None, None)
            ## Denise's contraction
            if child_node.is_empty:
                child_node.label = variable.name
                child_node.is_empty = False
                child_node.fixpoint_type = "max"
                return child_node
            # Normal case
            new_root = Node(variable.name, "max", False, [child_node], None)
            child_node.parent = new_root
            return new_root
        case query.MuFormula(variable, formula):
            child_node = create_tree(formula)
            if child_node is None:
                return Node(variable.name, "min", False, None, None)
            ## Denise's contraction
            if child_node.is_empty:
                child_node.label = variable.name
                child_node.is_empty = False
                child_node.fixpoint_type = "min"
                return child_node
            # Normal case
            new_root = Node(variable.name, "min", False, [child_node], None)
            child_node.parent = new_root
            return new_root
        case _:
            print(formula)
            raise AssertionError

