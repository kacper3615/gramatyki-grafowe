import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p3.p3 import P3

output_dir = "./productions/p3/outputs"
os.makedirs(output_dir, exist_ok=True)

# Create graph with a shared edge marked for refinement
graph = HyperGraph()
prod = P3()

n1 = graph.add_node(0, 0)
n2 = graph.add_node(1, 0)
n3 = graph.add_node(1, 1)

# create edges: n1-n2 is shared and marked
e1 = graph.add_edge(n1, n2, is_border=False)
e1.R = 1
# other edges
graph.add_edge(n2, n3, is_border=True)
graph.add_edge(n3, n1, is_border=True)

# visualize before
graph.visualize(os.path.join(output_dir, 'before_p3.png'))

can_apply, matched = prod.can_apply(graph)
if can_apply:
    prod.apply(graph, matched)

# visualize after
graph.visualize(os.path.join(output_dir, 'after_p3.png'))

