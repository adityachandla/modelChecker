from __future__ import annotations
from dataclasses import dataclass

import parse


@dataclass
class Edge:
    destination: int
    label: str

@dataclass
class Graph:
    adjacency: list[list[Edge]]

    @staticmethod
    def from_file(filename: str) -> Graph:
        with open(filename, 'r') as graph_file:
            lines = graph_file.read().strip().split('\n')
        header = parse.parse("des ({start:d},{edges:d},{nodes:d})", lines[0].strip())
        g = Graph([[] for i in range(header['nodes'])])
        edge_format = parse.compile("({src:d},\"{label}\",{dest:d})")
        for i in range(1,len(lines)):
            res = edge_format.parse(lines[i].strip())
            index = res['src']-header['start']
            g.adjacency[index].append(Edge(res['dest'], res['label']))
        return g
