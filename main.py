from __future__ import annotations
import os
import argparse

import query
from graph import Graph
from naive import NaiveChecker
from emerson import EmersonChecker

Checker = NaiveChecker | EmersonChecker

def get_files(path: str) -> (list[str], str):
    files = os.listdir(path)
    graph_file = None
    query_files = []
    for file in files:
        if file.endswith('aut'):
            graph_file = file
        elif file.endswith('mcf'):
            query_files.append(file)
    assert graph_file is not None
    return (query_files, graph_file)

def get_checker(graph: Graph, args: argparse.Namespace) -> Checker:
    if not args.emerson:
        print("Using Naive checker")
        return NaiveChecker(graph)
    print("Using Emerson checker")
    print()
    return EmersonChecker(graph)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Model checker")
    parser.add_argument('dirpath', help='Path to directory')
    parser.add_argument('-e', '--emerson', action="store_true")
    args = parser.parse_args()
    if not args.dirpath.endswith("/"):
        args.dirpath += "/"
    return args

def main():
    args = parse_args()
    query_files, graph_file = get_files(args.dirpath)
    graph = Graph.from_file(args.dirpath+graph_file)
    queries = []
    for query_file in query_files:
        queries.append(query.parse_query(args.dirpath+query_file))
    checker = get_checker(graph, args)
    for i in range(len(queries)):
        formula, variables, formula_string = queries[i]
        print(f"Query={formula_string}")
        res = checker.solve_formula(variables, formula)
        for variable in res.num_iter:
            print(f"Variable={variable} Num Iterations={res.num_iter[variable]}")
        print(f"Duration={res.running_time_millis}ms")
        print(f"Satisfied={res.satisfied_states.any_satisfying()}")
        print("---------------------------------------")
        print()


if __name__ == "__main__":
    main()
