from productions.production_base import Production
from hypergraph.node import Node

EPSILON = 1e-6

class P5(Production):
    """Production P5: breaks the quadrilateral element marked for refinement, if all its edges are broken
    it sets value of attribute R of new hyperedges with label Q to 0
    """

    def __init__(self):
        super().__init__(
            name="P5",
            description="Break quadrilateral element if all its edges are broken"
        )

    def can_apply(self, graph):
        """Check if P5 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """

        for hyperedge in graph.edges:
            if hyperedge.label == "Q" and len(hyperedge.nodes) == 4 and hyperedge.R == 1:
                nodes = hyperedge.nodes

                edges = []
                for i in range(4):
                    node_a = nodes[i]
                    node_b = nodes[(i + 1) % 4]
                    
                    mid_x, mid_y = (node_a.x + node_b.x) / 2, (node_a.y + node_b.y) / 2
                    
                    found_mid = None
                    for node in graph.nodes:
                        if abs(node.x - mid_x) < EPSILON and abs(node.y - mid_y) < EPSILON:
                            found_mid = node
                            break
                    
                    if not found_mid:
                        break 

                    edges.append(found_mid)

                if len(edges) == 4:
                    return True, {
                        'hyperedge': hyperedge,
                        'nodes': nodes,
                        'edges': edges 
                    }
        
        return False, None

    def apply(self, graph, matched_elements):
        hyperedge = matched_elements['hyperedge']
        n = matched_elements['nodes']
        m = matched_elements['edges']

        graph.remove_edge(hyperedge)

        center_node = graph.add_node(hyperedge.x, hyperedge.y)

        edges = []

        for i in range(4):
            edge = graph.add_edge(m[i], center_node)
            edges.append(edge)

        graph.add_hyperedge([n[0], m[0], center_node, m[3]], label="Q")
        graph.add_hyperedge([m[0], n[1], m[1], center_node], label="Q")
        graph.add_hyperedge([center_node, m[1], n[2], m[2]], label="Q")
        graph.add_hyperedge([m[3], center_node, m[2], n[3]], label="Q")
        
        print(f"[{self.name}] Broke quadrilateral hyperedge into 4 smaller quadrilaterals.")
        print(f"[{self.name}] Hyperedge R set to 0: {edges}")

        return {
            'marked_hyperedge': matched_elements['hyperedge'],
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }

