import os
import sys
import argparse
import query

from graph import Graph
from naive import NaiveChecker

def get_files(path: str) -> (list[str],str):
    files = os.listdir(path)
    graph_file = None
    query_files = []
    for file in files:
        if file.endswith('aut'):
            graph_file = file
        elif file.endswith('mcf'):
            query_files.append(file)
    assert graph_file != None
    return (query_files, graph_file)

def main():
    parser = argparse.ArgumentParser(prog="Model checker")
    parser.add_argument('dirpath', help='Path to directory with graph and queries')
    args = parser.parse_args()

    query_files, graph_file = get_files(args.dirpath)
    if not args.dirpath.endswith("/"):
        args.dirpath += "/"
    graph = Graph.from_file(args.dirpath+graph_file)
    queries = []
    for query_file in query_files:
        queries.append(query.parse_query(args.dirpath+query_file))
    naiveChecker = NaiveChecker(graph)
    for i in range(len(queries)):
        formula, variables, formula_string = queries[i]
        print(formula_string)
        res = naiveChecker.solve_formula(variables, formula)
        print(res)
        print()

if __name__ == "__main__":
    main()
