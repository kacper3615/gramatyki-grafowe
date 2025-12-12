import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p6.p6 import P6

output_dir = "./productions/p6/outputs"
os.makedirs(output_dir, exist_ok=True)

graph = HyperGraph()
production = P6()

coords = [(0.1, 0.1), (0.1, 0.6), (0.5, 0.9), (0.9, 0.6), (0.9, 0.1)]
nodes = [ graph.add_node(x, y) for (x, y) in coords ]

# create 5 edges
edges = []
for i in range(5):
    n1 = nodes[i]
    n2 = nodes[(i + 1) % 5]
    e = graph.add_edge(n1, n2, is_border=False)
    edges.append(e)

# create pentagon hyperedge
p = graph.add_hyperedge(nodes, label="P")

graph.visualize(os.path.join(output_dir, "before_p6.png"))

can_apply, matched = production.can_apply(graph)
if can_apply:
    production.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "after_p6.png"))
