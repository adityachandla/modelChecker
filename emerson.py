from graph import Graph

import query
import fixpoint_tree as ft
import checker_utils as cu


class EmersonChecker:
    def __init__(self, graph: Graph):
        self.graph = graph

    def solve_formula(self, variables: set[str],
                      formula: query.Formula) -> cu.CheckerOutput:
        tree = ft.create_tree(formula)
        self.type_relation = ft.create_fixpoint_to_type_relation(tree)
        rel_creator = ft.ResetRelationCreator(formula)
        self.reset_relation = rel_creator.find_relation(formula)
        # Initialization step
        self.varState = {}
        self.iter_count = {}
        for v in variables:
            if self.type_relation[v] == "max":
                self.varState[v] = set(range(0, self.graph.num_nodes))
            else:
                self.varState[v] = set()
            self.iter_count[v] = 0
        start = cu.get_time()
        res = self.solve(formula)
        duration = cu.get_time()-start
        return cu.CheckerOutput(res, self.iter_count, duration)

    def solve(self, formula: query.Formula) -> set[int]:
        match formula:
            case query.RecursionVariable(name):
                return self.varState[name]
            case query.TrueLiteral():
                return set(range(0, self.graph.num_nodes))
            case query.FalseLiteral():
                return set()
            case query.LogicFormula(left, right, is_and):
                left_solution = self.solve(left)
                right_solution = self.solve(right)
                if is_and:
                    return left_solution.intersection(right_solution)
                else:
                    return left_solution.union(right_solution)
            case query.BoxFormula(l, f):
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
            case query.DiamondFormula(l, f):
                result = self.solve(f)
                diamond_result = set()
                for i in range(self.graph.num_nodes):
                    out_neighbours = self.graph.get_outgoing(i, l)
                    for neighbour in out_neighbours:
                        if neighbour in result:
                            diamond_result.add(i)
                            break
                return diamond_result
            case query.NuFormula(var, f):
                while True:
                    updatedState = {i for i in self.varState[var.name]}
                    self.varState[var.name] = self.solve(f)
                    if self.varState[var.name] == updatedState:
                        break
                    self.iter_count[var.name] += 1
                return self.varState[var.name]
            case query.MuFormula(var, f):
                if var.name in self.reset_relation:
                    for var_to_reset in self.reset_relation[var.name]:
                        self.varState[var_to_reset] = set()
                while True:
                    updatedState = {i for i in self.varState[var.name]}
                    self.varState[var.name] = self.solve(f)
                    if self.varState[var.name] == updatedState:
                        break
                    self.iter_count[var.name] += 1
                return self.varState[var.name]
            case _:
                raise AssertionError
