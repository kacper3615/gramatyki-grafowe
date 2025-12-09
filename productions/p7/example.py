import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p7.p7 import P7

output_dir = "./productions/p7/outputs"
os.makedirs(output_dir, exist_ok=True)

graph = HyperGraph()
production = P7()

cords = [(0.1, 0.1), (0.1, 0.6), (0.5, 0.9), (0.9, 0.6), (0.9, 0.1)]
nodes = []
for y, x in cords:
    nodes.append(graph.add_node(x, y))

edges = []
for i in range(5):
    n1 = nodes[i]
    n2 = nodes[(i + 1) % 5]
    e = graph.add_hyperedge([n1, n2], label="E")
    e.R = 0
    edges.append(e)

p = graph.add_hyperedge(nodes, label="P")
p.R = 1

graph.visualize(os.path.join(output_dir, "example_p7_before.png"))

can_apply, matched = production.can_apply(graph)
if can_apply:
    production.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "example_p7_after.png"))
