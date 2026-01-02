import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
output_dir = "./productions/p1/outputs"

sys.path.insert(0, project_root)
os.makedirs(output_dir, exist_ok=True)

from hypergraph.hypergraph import HyperGraph
from productions.p1.p1 import P1

# Test 1
graph1 = HyperGraph()
production = P1()

n1 = graph1.add_node(0, 0)
n2 = graph1.add_node(1, 0)
n3 = graph1.add_node(1, 1)
n4 = graph1.add_node(0, 1)

graph1.add_edge(n1, n2, is_border=True)
graph1.add_edge(n2, n3, is_border=True)
graph1.add_edge(n3, n4, is_border=True)
graph1.add_edge(n4, n1, is_border=True)

q = graph1.add_hyperedge([n1, n2, n3, n4], label="Q")
q.R = 1

graph1.visualize(os.path.join(output_dir, "example_P1_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "example_P1_after.png"))

# Test 2
graph2 = HyperGraph()
production2 = P1()

n1 = graph2.add_node(0, 0)
n2 = graph2.add_node(1, 0)
n3 = graph2.add_node(1, 1)
n4 = graph2.add_node(0, 1)

graph2.add_edge(n1, n2, is_border=True)
graph2.add_edge(n2, n3, is_border=False)  # Shared edge
graph2.add_edge(n3, n4, is_border=True)
graph2.add_edge(n4, n1, is_border=True)

q1 = graph2.add_hyperedge([n1, n2, n3, n4], label="Q")
q1.R = 1 

n5 = graph2.add_node(2, 0)
n6 = graph2.add_node(2, 1)

graph2.add_edge(n2, n5, is_border=True)
graph2.add_edge(n5, n6, is_border=True)
graph2.add_edge(n6, n3, is_border=True)

q2 = graph2.add_hyperedge([n2, n5, n6, n3], label="Q")
q2.R = 1

graph2.visualize(os.path.join(output_dir, "example_P1_larger_graph_before.png"))

can_apply, matched = production2.can_apply(graph2)
if can_apply:
    production2.apply(graph2, matched)
    matched_q = matched['hyperedge']
    other_q = q2 if matched_q == q1 else q1

graph2.visualize(os.path.join(output_dir, "example_P1_larger_graph_after.png"))

# Test 3
graph3 = HyperGraph()
production3 = P1()

n1 = graph3.add_node(0, 0)
n2 = graph3.add_node(2, 0)
n3 = graph3.add_node(2, 2)
n4 = graph3.add_node(0, 2)

graph3.add_edge(n1, n2, is_border=True)
graph3.add_edge(n2, n3, is_border=True)
graph3.add_edge(n3, n4, is_border=True)
graph3.add_edge(n4, n1, is_border=True)

q = graph3.add_hyperedge([n1, n2, n3, n4], label="Q")
q.R = 1

graph3.visualize(os.path.join(output_dir, "example_P1_node_positions_before.png"))

can_apply, matched = production3.can_apply(graph3)
if can_apply:
    production3.apply(graph3, matched)

graph3.visualize(os.path.join(output_dir, "example_P1_node_positions_after.png"))

# Test 4
graph4 = HyperGraph()
production4 = P1()

n1 = graph4.add_node(0, 0)
n2 = graph4.add_node(2, 0)
n3 = graph4.add_node(2, 2)
n4 = graph4.add_node(0, 2)
n5 = graph4.add_node(-1, 1)
n6 = graph4.add_node(1, 3)
n7 = graph4.add_node(3, 1)
n8 = graph4.add_node(1, -1)

graph4.add_edge(n1, n2)
graph4.add_edge(n2, n3)
graph4.add_edge(n3, n4)
graph4.add_edge(n4, n1)
graph4.add_edge(n1, n5, is_border=True)
graph4.add_edge(n4, n6, is_border=True)
graph4.add_edge(n2, n7, is_border=True)
graph4.add_edge(n1, n8, is_border=True)
graph4.add_edge(n5, n4, is_border=True)
graph4.add_edge(n6, n3, is_border=True)
graph4.add_edge(n7, n3, is_border=True)
graph4.add_edge(n8, n2, is_border=True)

q = graph4.add_hyperedge([n1, n2, n3, n4], label="Q")
q.R = 1

graph4.visualize(os.path.join(output_dir, "example_P1_big.png"))

can_apply, matched = production4.can_apply(graph4)
if can_apply:
    production4.apply(graph4, matched)

graph4.visualize(os.path.join(output_dir, "example_P1_big_after.png"))