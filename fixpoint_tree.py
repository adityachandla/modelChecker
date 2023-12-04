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

