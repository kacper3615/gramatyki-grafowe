from productions.production_base import Production

class P1(Production):
    """Production P1: Marks edges of quadrilateral element, marked
        for refinement, for breaking.
    """

    def __init__(self):
        super().__init__(
            name="P1",
            description="Marks edges of quadrilateral element, marked for refinement, for breaking."
        )

    def can_apply(self, graph, **kwargs):
        hyperedge = None

        for edge in graph.edges:
            if edge.label == "Q" and len(edge.nodes) == 4 and edge.R == 1:
                hyperedge = edge
  
        if not hyperedge:
            return False, None
        
        edges_found = []

        nodes = hyperedge.nodes

        for i in range(4):
            node1 = nodes[i]
            node2 = nodes[(i + 1) % 4]
            found_edge = graph.get_edge_between(node1, node2)

            if found_edge is None:
                break
            
            # Check if edge is not already marked
            if found_edge.R == 1:
                break

            edges_found.append(found_edge)
        
        if len(edges_found) != 4:
            return False, None
          
        return True, {
            'hyperedge': hyperedge,
            'nodes': hyperedge.nodes,
            'edges': edges_found
        }

    def apply(self, graph, matched_elements):
        """Apply P1 to mark the quadrilateral for refinement."""
        edges = matched_elements['edges']

        for edge in edges:
            edge.R = 1

        return {
            'marked_hyperedge': matched_elements['hyperedge'],
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
