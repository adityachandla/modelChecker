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
    num_nodes: int

    def get_outgoing(self, src: int, label: str) -> list[int]:
        destination_nodes = []
        for edge in self.adjacency[src]:
            if edge.label == label:
                destination_nodes.append(edge.destination)
        return destination_nodes

    @staticmethod
    def from_file(filename: str) -> Graph:
        with open(filename, 'r') as graph_file:
            lines = graph_file.read().strip().split('\n')
        header_format_str = "des ({start:d},{edges:d},{nodes:d})"
        header = parse.parse(header_format_str, lines[0].strip())
        g = Graph([[] for i in range(header['nodes'])], header['nodes'])
        edge_format = parse.compile("({src:d},\"{label}\",{dest:d})")
        for i in range(1, len(lines)):
            res = edge_format.parse(lines[i].strip())
            g.adjacency[res['src']].append(Edge(res['dest'], res['label']))
        return g
