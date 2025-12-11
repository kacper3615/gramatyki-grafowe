import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p2.p2 import P2

output_dir = "./productions/p2/outputs"
os.makedirs(output_dir, exist_ok=True)

# simple example

graph = HyperGraph()
p2 = P2()

n1 = graph.add_node(0, 0)
n2 = graph.add_node(0, 20)
n3 = graph.add_node(1, 10)

e12 = graph.add_edge(n1, n2, is_border=False, label="E")
e12.R = 1

e23 = graph.add_edge(n2, n3, is_border=False, label="E")
e31 = graph.add_edge(n3, n1, is_border=False, label="E")

graph.visualize(os.path.join(output_dir, "example_p2_before.png"))

can_apply, matched = p2.can_apply(graph)

if can_apply:
    p2.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "example_p2_after.png"))

# larger graph example

graph = HyperGraph()
p2 = P2()

n1 = graph.add_node(0, 0)
n2 = graph.add_node(0, 10)
n3 = graph.add_node(10, 10)
n4 = graph.add_node(15, 10)
n5 = graph.add_node(20, 10)
n6 = graph.add_node(20, 5)
n7 = graph.add_node(20, 0)
n8 = graph.add_node(15, 0)
n9 = graph.add_node(10, 0)
n10 = graph.add_node(10.3, 5)
n11 = graph.add_node(15, 5)

e12 = graph.add_edge(n1, n2, is_border=True)
e23 = graph.add_edge(n2, n3, is_border=True)
e34 = graph.add_edge(n3, n4, is_border=True)
e45 = graph.add_edge(n4, n5, is_border=True)
e56 = graph.add_edge(n5, n6, is_border=True)
e67 = graph.add_edge(n6, n7, is_border=True)
e78 = graph.add_edge(n7, n8, is_border=True)
e89 = graph.add_edge(n8, n9, is_border=True)
e91 = graph.add_edge(n9, n1, is_border=True)

e114 = graph.add_edge(n11, n4)
e116 = graph.add_edge(n11, n6)
e118 = graph.add_edge(n11, n8)
e1110 = graph.add_edge(n11, n10)

e103 = graph.add_edge(n10, n3)
e109 = graph.add_edge(n10, n9)
e39 = graph.add_edge(n3, n9)

e91.R = 1
e118.R = 1
e39.R = 1

graph.visualize(os.path.join(output_dir, "example_p2_larger_graph_before.png"))

can_apply, matched = p2.can_apply(graph)

if can_apply:
    p2.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "example_p2_larger_graph_after.png"))