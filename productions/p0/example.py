import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p0.p0 import P0

output_dir = "./productions/p0/outputs"
os.makedirs(output_dir, exist_ok=True)

# Test 1: Simple quadrilateral

graph1 = HyperGraph()
production = P0()

n1 = graph1.add_node(0, 0)
n2 = graph1.add_node(1, 0)
n3 = graph1.add_node(1, 1)
n4 = graph1.add_node(0, 1)

graph1.add_edge(n1, n2, is_border=True)
graph1.add_edge(n2, n3, is_border=True)
graph1.add_edge(n3, n4, is_border=True)
graph1.add_edge(n4, n1, is_border=True)

q = graph1.add_hyperedge([n1, n2, n3, n4], label="Q")

# Before
graph1.visualize(os.path.join(output_dir, "example_p0_before.png"))

can_apply, matched = production.can_apply(graph1)
if can_apply:
    production.apply(graph1, matched)

graph1.visualize(os.path.join(output_dir, "example_p0_after.png"))

# Test 2: Quadrilateral embedded in larger structure
graph2 = HyperGraph()
production2 = P0()

n1 = graph2.add_node(0, 0)
n2 = graph2.add_node(1, 0)
n3 = graph2.add_node(1, 1)
n4 = graph2.add_node(0, 1)

graph2.add_edge(n1, n2, is_border=True)
graph2.add_edge(n2, n3, is_border=False)  # Shared edge
graph2.add_edge(n3, n4, is_border=True)
graph2.add_edge(n4, n1, is_border=True)

q1 = graph2.add_hyperedge([n1, n2, n3, n4], label="Q")

n5 = graph2.add_node(2, 0)
n6 = graph2.add_node(2, 1)

graph2.add_edge(n2, n5, is_border=True)
graph2.add_edge(n5, n6, is_border=True)
graph2.add_edge(n6, n3, is_border=True)

q2 = graph2.add_hyperedge([n2, n5, n6, n3], label="Q")

# Before applying
graph2.visualize(os.path.join(output_dir, "example_p0_larger_graph_before.png"))

# Apply production (will mark one quadrilateral)
can_apply, matched = production2.can_apply(graph2)
if can_apply:
    production2.apply(graph2, matched)
    matched_q = matched['hyperedge']
    other_q = q2 if matched_q == q1 else q1

# After applying
graph2.visualize(os.path.join(output_dir, "example_p0_larger_graph_after.png"))


# Test 3: Verification of node positions
print("\n3. Generating Test 3: Node position verification...")

graph3 = HyperGraph()
production3 = P0()

# Create larger quadrilateral with specific coordinates
n1 = graph3.add_node(0, 0)
n2 = graph3.add_node(2, 0)
n3 = graph3.add_node(2, 2)
n4 = graph3.add_node(0, 2)

graph3.add_edge(n1, n2, is_border=True)
graph3.add_edge(n2, n3, is_border=True)
graph3.add_edge(n3, n4, is_border=True)
graph3.add_edge(n4, n1, is_border=True)

q = graph3.add_hyperedge([n1, n2, n3, n4], label="Q")

# Before
graph3.visualize(os.path.join(output_dir, "example_p0_node_positions_before.png"))

# Store coordinates before
coords_before = [(n.x, n.y) for n in [n1, n2, n3, n4]]

# Apply production
can_apply, matched = production3.can_apply(graph3)
if can_apply:
    production3.apply(graph3, matched)

# After
coords_after = [(n.x, n.y) for n in [n1, n2, n3, n4]]

graph3.visualize(os.path.join(output_dir, "example_p0_node_positions_after.png"))
