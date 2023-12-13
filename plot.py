import matplotlib.pyplot as plt
import numpy as np

import query
from graph import Graph
from main import get_files
from naive import NaiveChecker
from emerson import EmersonChecker


def plot_num_iterations(experiment: str, xlabel: str, begin_range: int, end_range: int):
    emerson, naive = get_num_iterations(experiment)
    i = 0
    for query_string, emerson_data in emerson.items():
        naive_data = naive[query_string]
        plt.figure()
        plt.title(f'Comparison for Query: {query_string}')
        plt.xlabel(f'{xlabel}')
        plt.ylabel('Total Number of Iterations')
        x = np.arange(begin_range, end_range + 1)

        plt.plot(x, emerson_data ,marker='o', label='Emerson')
        plt.plot(x, naive_data, marker='x', label='Naive')
        plt.legend()
        plt.savefig(f"plots/{experiment}/{query_string}.png")
        i += 1


def get_num_iterations(experiment:str):
    path = f'Experiments/{experiment}/'
    query_files, graph_files = get_files(path)
    sorted_graph_files = sorted(graph_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    print(query_files)
    queries = []

    emerson_iterations = {}
    naive_iterations = {}

    for query_file in query_files:
        key = query.parse_query(path + query_file)
        queries.append(key)
        emerson_iterations[query_file] = []
        naive_iterations[query_file] = []
    for graph_file in sorted_graph_files:
        print(f'hey {graph_file}')
        graph = Graph.from_file(path + graph_file)
        for i in range(len(queries)):
            checker = EmersonChecker(graph)
            formula, variables, formula_string = queries[i]
            res = checker.solve_formula(variables, formula)
            total_num_iter = 0
            for variable in res.num_iter:
                total_num_iter += res.num_iter[variable]
            emerson_iterations[query_files[i]] += [total_num_iter]

            checker = NaiveChecker(graph)
            res = checker.solve_formula(variables, formula)
            total_num_iter = 0
            for variable in res.num_iter:
                total_num_iter += res.num_iter[variable]
            naive_iterations[query_files[i]] += [total_num_iter]
            print(f'query {i} done :)')

    return emerson_iterations, naive_iterations


plot_num_iterations('demanding', 'amount of children', 2, 10)
#plot_num_iterations('dining', 'amount of professors', 2, 11)
#plot_num_iterations('ccp', 'amount of clients', 2, 5)








