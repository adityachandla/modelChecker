from graph import Graph
from query import *

class NaiveChecker:
    def __init__(self, graph: Graph):
        self.graph = graph

    def solve_formula(self, variables: set[str], formula: Formula) -> set[int]:
        self.varState = dict()
        for v in variables:
            self.varState[v] = {}
        return self.solve(formula)

    def solve(self, formula: Formula) -> set[int]:
        match formula:
            case RecursionVariable(name):
                return self.varState[name]
            case TrueLiteral():
                return set(range(0, self.graph.num_nodes))
            case FalseLiteral():
                return set()
            case LogicFormula(left, right, is_and):
                l = self.solve(left)
                r = self.solve(right)
                if is_and:
                    return l.intersection(r)
                else:
                    return l.union(r)
            case BoxFormula(l, f):
                result = self.solve(f)
                box_result = set()
                for i in range(self.graph.num_nodes):
                    out_neighbours = self.graph.get_outgoing(i, l)
                    all_in = True
                    for neighbour in out_neighbours:
                        if neighbour not in result:
                            all_in = False
                            break
                    if all_in:
                        box_result.add(i)
                return box_result
            case DiamondFormula(l, f):
                result = self.solve(f)
                diamond_result = set()
                for i in range(self.graph.num_nodes):
                    out_neighbours = self.graph.get_outgoing(i, l)
                    for neighbour in out_neighbours:
                        if neighbour in result:
                            diamond_result.add(i)
                            break
                return diamond_result
            case NuFormula(var, f):
                self.varState[var.name] = set(range(0, self.graph.num_nodes))
                while True:
                    updatedState = {i for i in self.varState[var.name]}
                    self.varState[var.name] = self.solve(f)
                    if self.varState[var.name] == updatedState:
                        break
                return self.varState[var.name]
            case MuFormula(var, f):
                self.varState[var.name] = set()
                while True:
                    updatedState = {i for i in self.varState[var.name]}
                    self.varState[var.name] = self.solve(f)
                    if self.varState[var.name] == updatedState:
                        break
                return self.varState[var.name]
            case _:
                raise AssertionError
