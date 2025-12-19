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


graph = HyperGraph()
coords = [(1, 1), (1, 6), (5, 9), (9, 6), (9, 1)]
nodes = [graph.add_node(x, y) for (x, y) in coords]

edges = []
for i in range(5):
    n1 = nodes[i]
    n2 = nodes[(i + 1) % 5]
    border = i < 2 or i == 4
    e = graph.add_edge(n1, n2, is_border=border)
    edges.append(e)
p = graph.add_hyperedge(nodes, label="P")
n1 = graph.add_node(14, 1)
n2 = graph.add_node(14, 6)
n3 = graph.add_node(14, 9)
graph.add_edge(nodes[4], n1, is_border=True)
graph.add_edge(nodes[3], n2, is_border=False)
graph.add_edge(nodes[2], n3, is_border=True)
graph.add_edge(n1, n2, is_border=True)
graph.add_edge(n2, n3, is_border=True)
p = graph.add_hyperedge([nodes[4], nodes[3], n1, n2], label="P")
p = graph.add_hyperedge([nodes[2], nodes[3], n3, n2], label="P")

graph.visualize(os.path.join(output_dir, "before_p6_larger_graph_before.png"))

can_apply, matched = production.can_apply(graph)
if can_apply:
    production.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "after_p6_larger_graph_after.png"))
