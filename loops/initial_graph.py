import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from hypergraph.hypergraph import HyperGraph

output_dir = "./loops/"
os.makedirs(output_dir, exist_ok=True)

def create_initial_graph():
    graph = HyperGraph()
    
    rect_width = 2.0
    rect_height = 1.0
    
    c1 = graph.add_node(-rect_width/2, -rect_height/2, label="V")
    c2 = graph.add_node(rect_width/2, -rect_height/2, label="V")
    c3 = graph.add_node(rect_width/2, rect_height/2, label="V")
    c4 = graph.add_node(-rect_width/2, rect_height/2, label="V")
    
    graph.add_edge(c1, c2, is_border=False, label="E")
    graph.add_edge(c2, c3, is_border=False, label="E")
    graph.add_edge(c3, c4, is_border=False, label="E")
    graph.add_edge(c4, c1, is_border=False, label="E")
    
    q1 = graph.add_hyperedge([c1, c2, c3, c4], label="Q")
    
    trap_height = 0.8
    trap_base_extra = 0.5
    
    bt1 = graph.add_node(-rect_width/2 - trap_base_extra, -rect_height/2 - trap_height, label="V")
    bt2 = graph.add_node(rect_width/2 + trap_base_extra, -rect_height/2 - trap_height, label="V")
    
    graph.add_edge(bt1, bt2, is_border=True, label="E")
    
    q2 = graph.add_hyperedge([bt1, bt2, c2, c1], label="Q")
    
    tt1 = graph.add_node(-rect_width/2 - trap_base_extra, rect_height/2 + trap_height, label="V")
    tt2 = graph.add_node(rect_width/2 + trap_base_extra, rect_height/2 + trap_height, label="V")
    
    graph.add_edge(tt1, tt2, is_border=True, label="E")
    
    q3 = graph.add_hyperedge([c4, tt1, tt2, c3], label="Q")
    
    hex_width = 0.8
    
    lh1 = graph.add_node(-rect_width/2 - hex_width - trap_base_extra, -rect_height/2 - trap_height/2, label="V")
    lh2 = graph.add_node(-rect_width/2 - hex_width - trap_base_extra, rect_height/2 + trap_height/2, label="V")
    
    graph.add_edge(bt1, lh1, is_border=True, label="E")
    graph.add_edge(lh1, lh2, is_border=True, label="E")
    graph.add_edge(lh2, tt1, is_border=True, label="E")
    graph.add_edge(tt1, c4, is_border=False, label="E")
    graph.add_edge(c1, bt1, is_border=False, label="E")
    
    q4 = graph.add_hyperedge([bt1, lh1, lh2, tt1, c4, c1], label="Q")
    
    rh1 = graph.add_node(rect_width/2 + hex_width + trap_base_extra, -rect_height/2 - trap_height/2, label="V")
    rh2 = graph.add_node(rect_width/2 + hex_width + trap_base_extra, rect_height/2 + trap_height/2, label="V")
    
    graph.add_edge(c2, bt2, is_border=False, label="E")
    graph.add_edge(bt2, rh1, is_border=True, label="E")
    graph.add_edge(rh1, rh2, is_border=True, label="E")
    graph.add_edge(rh2, tt2, is_border=True, label="E")
    graph.add_edge(tt2, c3, is_border=False, label="E")
    
    q5 = graph.add_hyperedge([c2, bt2, rh1, rh2, tt2, c3], label="Q")
    
    return graph


if __name__ == "__main__":
    print("Creating initial graph structure...")
    graph = create_initial_graph()
    
    print("\nGraph structure:")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len([e for e in graph.edges if not e.is_hyperedge()])}")
    print(f"Hyperedges: {len([e for e in graph.edges if e.is_hyperedge()])}")
    
    print("\nVisualizing graph...")
    graph.visualize(os.path.join(output_dir, "initial_graph.png"))
    
    print(f"\nGraph saved to: {os.path.join(output_dir, 'initial_graph.png')}")
    print("Done!")
