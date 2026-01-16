import math
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p12.p12 import P12

output_dir = "./productions/p12/outputs"
os.makedirs(output_dir, exist_ok=True)

# Test 1: Simple heptagon

graph1 = HyperGraph()
production = P12()

n1 = graph1.add_node(0, 1)
n2 = graph1.add_node(1, 2)
n3 = graph1.add_node(2, 2)
n4 = graph1.add_node(3, 1)
n5 = graph1.add_node(2.5, 0)
n6 = graph1.add_node(1.5, -0.5)
n7 = graph1.add_node(0.5, 0)

graph1.add_edge(n1, n2, is_border=True)
graph1.add_edge(n2, n3, is_border=True)
graph1.add_edge(n3, n4, is_border=True)
graph1.add_edge(n4, n5, is_border=True)
graph1.add_edge(n5, n6, is_border=True)
graph1.add_edge(n6, n7, is_border=True)
graph1.add_edge(n7, n1, is_border=True)

heptagon = graph1.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

# Before
graph1.visualize(os.path.join(output_dir, "example_p12_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "example_p12_after.png"))

# Test 2: two heptagons sharing nodes

graph2 = HyperGraph()
production2 = P12()

# First heptagon
n1 = graph2.add_node(0, 1)
n2 = graph2.add_node(1, 2)
n3 = graph2.add_node(2, 2)
n4 = graph2.add_node(3, 1)
n5 = graph2.add_node(2.5, 0)
n6 = graph2.add_node(1.5, -0.5)
n7 = graph2.add_node(0.5, 0)

graph2.add_edge(n1, n2, is_border=True)
graph2.add_edge(n2, n3, is_border=True)
graph2.add_edge(n3, n4, is_border=True)
graph2.add_edge(n4, n5, is_border=True)
graph2.add_edge(n5, n6, is_border=True)
graph2.add_edge(n6, n7, is_border=True)
graph2.add_edge(n7, n1, is_border=True)

heptagon1 = graph2.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

# Second heptagon sharing some nodes (n3, n4, n5)
n8 = graph2.add_node(4, 1.5)
n9 = graph2.add_node(5, 1)
n10 = graph2.add_node(4.5, 0)
n11 = graph2.add_node(3.5, -0.5)
n12 = graph2.add_node(3, 0)
# n13 = n4  # shared node
# n14 = n3  # shared node

graph2.add_edge(n3, n8, is_border=True)
graph2.add_edge(n8, n9, is_border=True)
graph2.add_edge(n9, n10, is_border=True)
graph2.add_edge(n10, n11, is_border=True)
graph2.add_edge(n11, n12, is_border=True)
graph2.add_edge(n12, n4, is_border=True)
graph2.add_edge(n4, n3, is_border=True)

heptagon2 = graph2.add_hyperedge([n3, n8, n9, n10, n11, n12, n4], label="T")

# Visualize
graph2.visualize(os.path.join(output_dir, "example_p12_two_heptagons_before.png"))

can_apply, matched = production2.can_apply(graph2)
if can_apply:
    production2.apply(graph2, matched)

graph2.visualize(os.path.join(output_dir, "example_p12_two_heptagons_after_1.png"))

can_apply, matched = production2.can_apply(graph2)
if can_apply:
    production2.apply(graph2, matched)

graph2.visualize(os.path.join(output_dir, "example_p12_two_heptagons_after_2.png"))
