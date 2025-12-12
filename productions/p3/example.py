import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p3.p3 import P3

output_dir = "./productions/p3/outputs"
os.makedirs(output_dir, exist_ok=True)

#Example 1 - simple triangle

graph = HyperGraph()
prod = P3()

n1 = graph.add_node(0, 0)
n2 = graph.add_node(1, 0)
n3 = graph.add_node(1, 1)

e1 = graph.add_edge(n1, n2, is_border=False)
e1.R = 1
graph.add_edge(n2, n3, is_border=True)
graph.add_edge(n3, n1, is_border=True)

graph.visualize(os.path.join(output_dir, 'example_1_p3_before.png'))

can_apply, matched = prod.can_apply(graph)
if can_apply:
    prod.apply(graph, matched)

graph.visualize(os.path.join(output_dir, 'example_1_p3_after.png'))

#Example 2 - four connected squares

graph = HyperGraph()
prod = P3()

n1 = graph.add_node(0, 0)
n2 = graph.add_node(1, 0)
n3 = graph.add_node(2, 0)
n4 = graph.add_node(0, 1)
n5 = graph.add_node(1, 1)
n6 = graph.add_node(2, 1)
n7 = graph.add_node(0, 2)
n8 = graph.add_node(1, 2)
n9 = graph.add_node(2, 2)

e1 = graph.add_edge(n1, n2, is_border=True)
e1.R = 1
e2 = graph.add_edge(n2, n3, is_border=True)
e2.R = 1
e3 = graph.add_edge(n1, n4, is_border=True)
e3.R = 1
e4 = graph.add_edge(n3, n6, is_border=True)
e4.R = 1
e5 = graph.add_edge(n4, n7, is_border=True)
e5.R = 1
e6 = graph.add_edge(n6, n9, is_border=True)
e6.R = 1
e7 = graph.add_edge(n7, n8, is_border=True)
e7.R = 1
e8 = graph.add_edge(n8, n9, is_border=True)
e8.R = 1

e9 = graph.add_edge(n2, n5, is_border=False)
e9.R = 0
e10 = graph.add_edge(n4, n5, is_border=False)
e10.R = 0
e11 = graph.add_edge(n5, n6, is_border=False)
e11.R = 0
e12 = graph.add_edge(n5, n8, is_border=False)
e12.R = 1

graph.add_hyperedge([n1, n2, n4, n5])
graph.add_hyperedge([n2, n3, n5, n6])
graph.add_hyperedge([n4, n5, n7, n8])
graph.add_hyperedge([n5, n6, n8, n9])

graph.visualize(os.path.join(output_dir, 'example_2_p3_before.png'))

can_apply, matched = prod.can_apply(graph)
if can_apply:
    prod.apply(graph, matched)

graph.visualize(os.path.join(output_dir, 'example_2_p3_after.png'))

