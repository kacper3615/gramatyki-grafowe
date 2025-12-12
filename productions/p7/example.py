import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p7.p7 import P7

output_dir = "./productions/p7/outputs"
os.makedirs(output_dir, exist_ok=True)



# Example 1 - simple pentagon

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

graph.visualize(os.path.join(output_dir, "example_1_p7_before.png"))

can_apply, matched = production.can_apply(graph)
if can_apply:
    production.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "example_1_p7_after.png"))



# Example 2 - pentagon with hanging nodes

graph_2 = HyperGraph()

cords_2 = [(0.2, 0.2), (0.15, 0.6), (0.5, 0.95), (0.85, 0.6), (0.8, 0.2)]
nodes_2 = []
for y, x in cords_2:
    nodes_2.append(graph_2.add_node(x, y))

edges_2 = []
for i in range(5):
    n1 = nodes_2[i]
    n2 = nodes_2[(i + 1) % 5]
    e2 = graph_2.add_edge(n1, n2, label="E")
    e2.R = 0
    edges_2.append(e2)

# add one hanging node connected to each of pentagon node
center_x, center_y = 0.5, 0.55
for node in nodes_2:
    hx = center_x + 1.5 * (node.x - center_x)
    hy = center_y + 1.5 * (node.y - center_y)
    h = graph_2.add_node(hx, hy)
    graph_2.add_edge(node, h, label="E")

p2 = graph_2.add_hyperedge(nodes_2, label="P")
p2.R = 1

graph_2.visualize(os.path.join(output_dir, "example_2_p7_before.png"))

can_apply_2, matched_2 = production.can_apply(graph_2)
if can_apply_2:
    production.apply(graph_2, matched_2)

graph_2.visualize(os.path.join(output_dir, "example_2_p7_after.png"))



# Example 3 - pentagon with additional square region

graph_3 = HyperGraph()

cords_3 = [(0.1, 0.2), (0.15, 0.6), (0.45, 0.9), (0.7, 0.5), (0.7, 0.2)]
nodes_3 = []
for y, x in cords_3:
    nodes_3.append(graph_3.add_node(x, y))

edges_3 = []
for i in range(5):
    n1 = nodes_3[i]
    n2 = nodes_3[(i + 1) % 5]
    e3 = graph_3.add_edge(n1, n2, label="E")
    e3.R = 0
    edges_3.append(e3)

p3 = graph_3.add_hyperedge(nodes_3, label="P")
p3.R = 1

# additional square region attached to the right side
square_cords = [(0.9, 0.35), (0.75, 0.75), (0.6, 0.75)]
nodes_3_square = []
nodes_3_square.append(nodes_3[3]) # shared node for pentagon and square
for y, x in square_cords:
    nodes_3_square.append(graph_3.add_node(x, y))

for i in range(4):
    n1 = nodes_3_square[i]
    n2 = nodes_3_square[(i + 1) % 4]
    graph_3.add_edge(n1, n2, label="E")

graph_3.add_hyperedge(nodes_3_square, label="Q")

graph_3.visualize(os.path.join(output_dir, "example_3_p7_before.png"))

can_apply_3, matched_3 = production.can_apply(graph_3)
if can_apply_3:
    production.apply(graph_3, matched_3)

graph_3.visualize(os.path.join(output_dir, "example_3_p7_after.png"))



# Example 4 - pentagon with additional 2 quadrangle region

graph_4 = HyperGraph()

cords_4 = [(0.1, 0.1), (0.1, 0.5), (0.5, 0.5), (0.9, 0.3), (0.5, 0.1)]
nodes_4 = []
for y, x in cords_4:
    nodes_4.append(graph_4.add_node(x, y))

edges_4 = []
for i in range(5):
    n1 = nodes_4[i]
    n2 = nodes_4[(i + 1) % 5]
    e4 = graph_4.add_edge(n1, n2, label="E")
    e4.R = 0
    if i in [4, 3, 0]: e4.B = 1
    edges_4.append(e4)

p4 = graph_4.add_hyperedge(nodes_4, label="P")
p4.R = 1

n1 = graph_4.add_node(0.8, 0.8)
n2 = graph_4.add_node(0.9, 0.5)
n3 = nodes_4[2] 
n4 = nodes_4[3] 

e = graph_4.add_edge(n1, n2, label="E")
e.B = 1
edges_4.append(e)
edges_4.append(graph_4.add_edge(n2, n3, label="E"))
e = graph_4.add_edge(n1, n4, label="E")
e.B = 1
edges_4.append(e)

nodes_quad_1 = [n1, n2, n3, n4]
p4 = graph_4.add_hyperedge(nodes_quad_1, label="Q")

n1 = graph_4.add_node(0.9, 0.1)
n2 = nodes_4[1] 
n3 = nodes_4[2]
n4 = nodes_quad_1[1]

e = graph_4.add_edge(n1, n2, label="E")
e.B = 1
edges_4.append(e)
e = graph_4.add_edge(n1, n4, label="E")
e.B = 1
edges_4.append(e)
edges_4.append(graph_4.add_edge(n3, n4, label="E"))

nodes_quad_2 = [n1, n2, n3, n4]
p4 = graph_4.add_hyperedge(nodes_quad_2, label="Q")

graph_4.visualize(os.path.join(output_dir, "example_4_p7_before.png"))
can_apply_4, matched_4 = production.can_apply(graph_4)
if can_apply_4:
    production.apply(graph_4, matched_4)

graph_4.visualize(os.path.join(output_dir, "example_4_p7_after.png"))
