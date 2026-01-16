import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph
from productions.p5.p5 import P5

output_dir = "./productions/p5/outputs"
os.makedirs(output_dir, exist_ok=True)

graph = HyperGraph()
production = P5()

n1 = graph.add_node(0, 0, label="1")
n2 = graph.add_node(2, 0, label="2")
n3 = graph.add_node(2, 2, label="3")
n4 = graph.add_node(0, 2, label="4")

n5 = graph.add_node(1, 0, label="5")
n6 = graph.add_node(2, 1, label="6")
n7 = graph.add_node(1, 2, label="7")
n8 = graph.add_node(0, 1, label="8")

graph.add_edge(n1, n5, is_border=True)
graph.add_edge(n5, n2, is_border=True)
graph.add_edge(n2, n6, is_border=True)
graph.add_edge(n6, n3, is_border=True)
graph.add_edge(n3, n7, is_border=True)
graph.add_edge(n7, n4, is_border=True)
graph.add_edge(n4, n8, is_border=True)
graph.add_edge(n8, n1, is_border=True)


q = graph.add_hyperedge([n1, n2, n3, n4], label="Q")
q.R = 1 

graph.visualize(os.path.join(output_dir, "p5_before.png"))

can_apply, matched = production.can_apply(graph)
if can_apply:
    production.apply(graph, matched)    
    graph.visualize(os.path.join(output_dir, "p5_after.png"))
