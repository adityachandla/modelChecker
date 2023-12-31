from __future__ import annotations
import os
import argparse

import query
from graph import Graph
from naive import NaiveChecker
from emerson import EmersonChecker

Checker = NaiveChecker | EmersonChecker

def get_files(path: str) -> (list[str], list[str]):
    files = os.listdir(path)
    graph_files = []
    query_files = []
    for file in files:
        if file.endswith('aut'):
            graph_files.append(file)
        elif file.endswith('mcf'):
            query_files.append(file)
    return (query_files, graph_files)

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
    # If this is provided we don't run all the graph files
    parser.add_argument('-g', '--graph', help="Name of graph file to run")
    parser.add_argument('-e', '--emerson', action="store_true")
    args = parser.parse_args()
    if not args.dirpath.endswith("/"):
        args.dirpath += "/"
    return args

def main():
    args = parse_args()
    query_files, graph_files = get_files(args.dirpath)
    if args.graph is not None:
        graph_files = [g for g in graph_files if g == args.graph]
    queries = []
    for query_file in query_files:
        queries.append(query.parse_query(args.dirpath+query_file))
    for graph_file in graph_files:
        graph = Graph.from_file(args.dirpath+graph_file)
        checker = get_checker(graph, args)
        print("############################")
        print(f"Processing file {graph_file}")
        print("############################")
        for i in range(len(queries)):
            formula, variables, formula_string = queries[i]
            print(f"Query={formula_string}")
            res = checker.solve_formula(variables, formula)
            for variable in res.num_iter:
                print(f"Variable={variable} Num Iterations={res.num_iter[variable]}")
            print(f"Duration={res.running_time_millis}ms")
            print(f"Satisfying States={len(res.satisfied_states)}")
            print("---------------------------------------")
            print()


if __name__ == "__main__":
    main()
