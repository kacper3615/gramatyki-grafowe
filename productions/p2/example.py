import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p2.p2 import P2

output_dir = "./productions/p2/outputs"
os.makedirs(output_dir, exist_ok=True)

graph = HyperGraph()
p2 = P2()

n1 = graph.add_node(0, 0, label="1")
n2 = graph.add_node(10, 0, label="2")

edge = graph.add_edge(n1, n2, is_border=False, label="E")
edge.R = 1

mid_x = (n1.x + n2.x) / 2
mid_y = (n1.y + n2.y) / 2
hanging_node = graph.add_node(mid_x, mid_y, is_hanging=True, label="h")

graph.visualize(os.path.join(output_dir, "example_p2_before.png"))

can_apply, matched = p2.can_apply(graph)

if can_apply:
    p2.apply(graph, matched)

graph.visualize(os.path.join(output_dir, "example_p2_after.png"))