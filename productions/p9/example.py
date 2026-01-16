import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p9.p9 import P9

output_dir = "./productions/p9/outputs"
os.makedirs(output_dir, exist_ok=True)

# Test 1: Simple hexagon

graph1 = HyperGraph()
production = P9()

coords = [(-3, 0), (-1.5, 2.6),(1.5, 2.6), (3, 0), (1.5, -2.6), (-1.5, -2.6)]

n1, n2, n3, n4, n5, n6 = [
    graph1.add_node(x, y)
    for x, y in coords
]
borders = {(n1, n2), (n2, n3), (n3, n4), (n4, n5), (n5, n6), (n6, n1)}
edges = []
for i in borders:
    e = graph1.add_edge(i[0], i[1])
    e.R = 0
    edges.append(e)

h = graph1.add_hyperedge([n1,n2,n3,n4,n5,n6], label="S")
h.R = 0
# Before
graph1.visualize(os.path.join(output_dir, "example_p9_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "example_p9_after.png"))

# Test 2: Hexagon embedded in slightly larger structure (with two extra quadrilaterals)
graph2 = HyperGraph()
production = P9()



coords = [(-3, 0), (-1.5, 2.6),(1.5, 2.6), (3, 0), (1.5, -2.6), (-1.5, -2.6), (6, 2.6), (6,0), (6, -2.6)]

n1, n2, n3, n4, n5, n6, n7, n8, n9 = [
    graph2.add_node(x, y)
    for x, y in coords
]
borders = {(n1, n2), (n2, n3), (n3, n7), (n7, n8), (n8, n9), (n9, n5), (n5, n6), (n6, n1)}
inner = {(n4, n5), (n3, n4), (n4, n8)}
edges = []
for i in borders:
    e = graph2.add_edge(i[0], i[1])
    e.R = 0
    edges.append(e)

for i in inner:
    e = graph2.add_edge(i[0], i[1], is_border=False, label="E")
    e.R = 0
    edges.append(e)

h = graph2.add_hyperedge([n1,n2,n3,n4,n5,n6], label="S")
h.R = 0



q1 = graph2.add_hyperedge([n3,n4,n8,n7], label="Q")
q2 = graph2.add_hyperedge([n4,n5,n9,n8], label="Q")
q1.R =0
q2.R =0

# Before applying
graph2.visualize(os.path.join(output_dir, "example_p9_larger_graph_before.png"))

# Apply production (will mark one quadrilateral)
can_apply, matched = production.can_apply(graph2)
if can_apply:
    production.apply(graph2, matched)
    matched_q = matched['hyperedge']
    other_q = q2 if matched_q == q1 else q1

# After applying
graph2.visualize(os.path.join(output_dir, "example_p9_larger_graph_after.png"))
