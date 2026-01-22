from productions.production_base import Production
from hypergraph.hypergraph import HyperGraph
from typing import Dict, Optional, Tuple
import math


class P8(Production):
    def __init__(self):
        super().__init__(
            name="P8",
            description="Break pentagonal element marked for refinement into quadrilaterals"
        )
    
    def can_apply(self, graph, hyperedge=None):
        edges_to_check = graph.edges
        for edge in edges_to_check:
            if not edge.is_hyperedge():
                continue
            if edge.label != "P" or len(edge.nodes) != 5:
                continue
            if getattr(edge, 'R', 0) != 1:
                continue
            
            nodes = edge.nodes
            found_edges = []
            
            for i in range(5):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 5]
                
                found_edge = graph.get_edge_between(node1, node2)
                if found_edge is None:
                    found_edges.append(found_edge)
        

            if len(found_edges) == 5:
                return True, {
                    'pentagon_hyperedge': edge,
                    'nodes': nodes,
                    'edges': found_edges
                }
            
        return False, None
    
    def apply(self, graph, matched_elements, midpoints):

        pentagon_he = matched_elements['pentagon_hyperedge']
        nodes = matched_elements['nodes']
        edges = matched_elements['edges']
        
        graph.remove_edge(pentagon_he)

        centroid_x = sum(node.x for node in nodes) / 5
        centroid_y = sum(node.y for node in nodes) / 5
        centroid_z = sum(getattr(node, 'z', 0) for node in nodes) / 5

        # dodajemy centrale V
        centroid_node = graph.add_node(centroid_x, centroid_y, centroid_z)
            
        # dadajemy krawedz pomiedzy srodiem a midpointami
        for midpoint in midpoints:
            print("Midpoint: ", midpoint.label)
            graph.add_edge(centroid_node, midpoint, 
                        is_border=False, 
                        R=0)
        
        # dodajemy quady
        new_quads = []
        for i in range(5):
            vertex = nodes[i]
            mid_next = midpoints[i]
            mid_prev = midpoints[(i + 1) % 5]
            
            quad_nodes = [vertex, mid_next, centroid_node, mid_prev]
            quad_he = graph.add_hyperedge(quad_nodes, label="Q")
            quad_he.R = 0  
            new_quads.append(quad_he)
        
                
        return {
            'original_pentagon': pentagon_he,
            'centroid': centroid_node,
            'midpoints': midpoints,
            'new_quadrilaterals': new_quads,
            'nodes': nodes
        }