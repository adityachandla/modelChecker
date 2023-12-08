from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

import parse


@dataclass
class Graph:
    adjacency_dict: dict[tuple[int, str],list[int]]
    num_nodes: int

    def get_outgoing(self, src: int, label: str) -> tuple[int]:
        return self.adjacency_dict[(src, label)]

    @staticmethod
    def from_file(filename: str) -> Graph:
        with open(filename, 'r') as graph_file:
            lines = graph_file.read().strip().split('\n')
        header_format_str = "des ({start:d},{edges:d},{nodes:d})"
        header = parse.parse(header_format_str, lines[0].strip())
        g = Graph(defaultdict(list), header['nodes'])
        edge_format = parse.compile("({src:d},\"{label}\",{dest:d})")
        for i in range(1, len(lines)):
            res = edge_format.parse(lines[i].strip())
            key = (res['src'], res['label'])
            g.adjacency_dict[key].append(res['dest'])
        return g
