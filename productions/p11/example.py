import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p11.p11 import P11

output_dir = "./productions/p11/outputs"
os.makedirs(output_dir, exist_ok=True)

production = P11()

# Test 1: Simple hexagonal element marked for refinement
graph1 = HyperGraph()

n1 = graph1.add_node(0, 0)
n2 = graph1.add_node(-0.5, 0.866)
n3 = graph1.add_node(0, 1.732)
n4 = graph1.add_node(1, 1.732)
n5 = graph1.add_node(1.5, 0.866)
n6 = graph1.add_node(1, 0)

n12 = graph1.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
n23 = graph1.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
n34 = graph1.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
n45 = graph1.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
n56 = graph1.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
n61 = graph1.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

graph1.add_edge(n1, n12, is_border=True)
graph1.add_edge(n12, n2, is_border=True)
graph1.add_edge(n2, n23, is_border=True)
graph1.add_edge(n23, n3, is_border=True)
graph1.add_edge(n3, n34, is_border=True)
graph1.add_edge(n34, n4, is_border=True)
graph1.add_edge(n4, n45, is_border=True)
graph1.add_edge(n45, n5, is_border=True)
graph1.add_edge(n5, n56, is_border=True)
graph1.add_edge(n56, n6, is_border=True)
graph1.add_edge(n6, n61, is_border=True)
graph1.add_edge(n61, n1, is_border=True)

hexa = graph1.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
hexa.R = 1  # Marked for refinement

# Before
graph1.visualize(os.path.join(output_dir, "example_p11_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)
else:
    print("[Simple hexagon] Production P11 cannot be applied.")

# After
graph1.visualize(os.path.join(output_dir, "example_p11_after.png"))


# Test 2: Hexagonal element embedded in slightly larger structure (with two extra quadrilaterals)
graph2 = HyperGraph()

n1 = graph2.add_node(0, 0, is_hanging=False)
n2 = graph2.add_node(-0.5, 0.866, is_hanging=False)
n3 = graph2.add_node(0, 1.732, is_hanging=False)
n4 = graph2.add_node(1, 1.732, is_hanging=False)
n5 = graph2.add_node(1.5, 0.866, is_hanging=False)
n6 = graph2.add_node(1, 0, is_hanging=False)

n12 = graph2.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
n23 = graph2.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
n34 = graph2.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
n45 = graph2.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
n56 = graph2.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
n61 = graph2.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

graph2.add_edge(n1, n12, is_border=True)
graph2.add_edge(n12, n2, is_border=True)
graph2.add_edge(n2, n23, is_border=True)
graph2.add_edge(n23, n3, is_border=True)
graph2.add_edge(n3, n34, is_border=True)
graph2.add_edge(n34, n4, is_border=True)
graph2.add_edge(n4, n45, is_border=True)
graph2.add_edge(n45, n5, is_border=True)
graph2.add_edge(n5, n56, is_border=True)
graph2.add_edge(n56, n6, is_border=True)
graph2.add_edge(n6, n61, is_border=False)
graph2.add_edge(n61, n1, is_border=False)

hexa2 = graph2.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
hexa2.R = 1  # Marked for refinement

nq1 = graph2.add_node(0.5, -0.5, is_hanging=False)
nq2 = graph2.add_node(0, -0.5, is_hanging=False)
graph2.add_edge(n61, nq1, is_border=True)
graph2.add_edge(nq1, nq2, is_border=True)
graph2.add_edge(nq2, n1, is_border=True)
graph2.add_hyperedge([n61, nq1, nq2, n1], label="Q")

nq3 = graph2.add_node(1, -0.5, is_hanging=False)
graph2.add_edge(n6, nq3, is_border=True)
graph2.add_edge(nq3, nq1, is_border=True)
graph2.add_hyperedge([n6, nq3, nq1, n61], label="Q")

# Before
graph2.visualize(os.path.join(output_dir, "example_p11_slightly_larger_graph_before.png"))

can_apply, matched = production.can_apply(graph2)
if can_apply:
    production.apply(graph2, matched)
else:
    print("[Slightly larger graph] Production P11 cannot be applied.")

# After
graph2.visualize(os.path.join(output_dir, "example_p11_slightly_larger_graph_after.png"))


# Test 3: Two hexagonal elements marked for refinement and few extra nodes/edges
graph3 = HyperGraph()

# First hexagon
n1 = graph3.add_node(0, 0)
n2 = graph3.add_node(1, 0)
n3 = graph3.add_node(1.5, 0.866)
n4 = graph3.add_node(1, 1.732)
n5 = graph3.add_node(0, 1.732)
n6 = graph3.add_node(-0.5, 0.866)

n12 = graph3.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
n23 = graph3.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
n34 = graph3.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
n45 = graph3.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
n56 = graph3.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
n61 = graph3.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

graph3.add_edge(n1, n12)
graph3.add_edge(n12, n2)
graph3.add_edge(n2, n23)
graph3.add_edge(n23, n3)
graph3.add_edge(n3, n34)
graph3.add_edge(n34, n4)
graph3.add_edge(n4, n45)
graph3.add_edge(n45, n5)
graph3.add_edge(n5, n56)
graph3.add_edge(n56, n6)
graph3.add_edge(n6, n61)
graph3.add_edge(n61, n1)

h = graph3.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
h.R = 1  # Mark for refinement

# Second hexagon (sharing n1 and n12)
n7 = n12
n8 = graph3.add_node(1.5, 0)
n9 = graph3.add_node(2, -0.866)
n10 = graph3.add_node(1.5, -1.732)
n11 = graph3.add_node(0.5, -1.732)  
n12_2 = graph3.add_node(0, -0.866)
n78 = n2
n89 = graph3.add_node((n8.x + n9.x) / 2, (n8.y + n9.y) / 2, is_hanging=True)
n910 = graph3.add_node((n9.x + n10.x) / 2, (n9.y + n10.y) / 2, is_hanging=True)
n1011 = graph3.add_node((n10.x + n11.x) / 2, (n10.y + n11.y) / 2, is_hanging=True)
n1112 = graph3.add_node((n11.x + n12_2.x) / 2, (n11.y + n12_2.y) / 2, is_hanging=True)
n127 = graph3.add_node((n12_2.x + n7.x) / 2, (n12_2.y + n7.y) / 2, is_hanging=True)
graph3.add_edge(n7, n78)
graph3.add_edge(n78, n8)
graph3.add_edge(n8, n89)
graph3.add_edge(n89, n9)
graph3.add_edge(n9, n910)
graph3.add_edge(n910, n10)
graph3.add_edge(n10, n1011)
graph3.add_edge(n1011, n11)
graph3.add_edge(n11, n1112)
graph3.add_edge(n1112, n12_2)
graph3.add_edge(n12_2, n127)
graph3.add_edge(n127, n7)

h2 = graph3.add_hyperedge([n7, n8, n9, n10, n11, n12_2], label="S")
h2.R = 1  # Mark for refinement

# Some extra nodes and edges in the graph
n_extra1 = graph3.add_node(-1.5, 1)
n_extra2 = graph3.add_node(-1, -1)
graph3.add_edge(n_extra1, n_extra2)
graph3.add_edge(n56, n_extra1)
graph3.add_edge(n1112, n_extra2)

# Before
graph3.visualize(os.path.join(output_dir, "example_p11_two_hexagonals_before.png"))

can_apply, matched = production.can_apply(graph3)
if can_apply:
    production.apply(graph3, matched)
else:
    print("[Two hexagonals] Production P11 cannot be applied.")

# After
graph3.visualize(os.path.join(output_dir, "example_p11_two_hexagonals_after1.png"))

# Second application
can_apply, matched = production.can_apply(graph3)
if can_apply:
    production.apply(graph3, matched)
else:
    print("[Two hexagonals] Production P11 cannot be applied.")
# After
graph3.visualize(os.path.join(output_dir, "example_p11_two_hexagonals_after2.png"))


# Test 4: Uglier shaped hexagonal element
graph4 = HyperGraph()

n1 = graph4.add_node(0, 0)
n2 = graph4.add_node(2, 1)
n3 = graph4.add_node(1.5, 3)
n4 = graph4.add_node(0, 4)
n5 = graph4.add_node(-1.5, 2.5)
n6 = graph4.add_node(-1, 1)

n12 = graph4.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
n23 = graph4.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
n34 = graph4.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
n45 = graph4.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
n56 = graph4.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
n61 = graph4.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

graph4.add_edge(n1, n12, is_border=True)
graph4.add_edge(n12, n2, is_border=True)
graph4.add_edge(n2, n23, is_border=True)
graph4.add_edge(n23, n3, is_border=True)
graph4.add_edge(n3, n34, is_border=True)
graph4.add_edge(n34, n4, is_border=True)
graph4.add_edge(n4, n45, is_border=True)
graph4.add_edge(n45, n5, is_border=True)
graph4.add_edge(n5, n56, is_border=True)
graph4.add_edge(n56, n6, is_border=True)
graph4.add_edge(n6, n61, is_border=True)
graph4.add_edge(n61, n1, is_border=True)

hexa4 = graph4.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
hexa4.R = 1  # Marked for refinement

# Before
graph4.visualize(os.path.join(output_dir, "example_p11_ugly_hexagon_before.png"))
can_apply, matched = production.can_apply(graph4)
if can_apply:
    production.apply(graph4, matched)
else:
    print("[Ugly hexagon] Production P11 cannot be applied.")

# After
graph4.visualize(os.path.join(output_dir, "example_p11_ugly_hexagon_after.png"))