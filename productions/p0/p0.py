from productions.production_base import Production

class P0(Production):
    """Production P0: Mark quadrilateral element for refinement.
    It sets value of attribute R of the hyperedge with label Q to 1
    """

    def __init__(self):
        super().__init__(
            name="P0",
            description="Mark quadrilateral element for refinement"
        )

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """Check if P0 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            # Check if it's a quadrilateral (label Q and 4 nodes)
            if edge.label != "Q" or len(edge.nodes) != 4:
                continue

            # Check if R = 0 (not yet marked for refinement)
            if edge.R != 0:
                continue

            # Check refinement criterion
            if not refinement_criterion:
                continue

            # Find the 4 edges connecting the nodes
            nodes = edge.nodes
            edges_found = []

            for i in range(4):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 4]
                found_edge = graph.get_edge_between(node1, node2)
                if found_edge is None:
                    break
                edges_found.append(found_edge)

            if len(edges_found) == 4:
                return True, {
                    'hyperedge': edge,
                    'nodes': nodes,
                    'edges': edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """Apply P0 to mark the quadrilateral for refinement."""
        hyperedge = matched_elements['hyperedge']

        # Mark the hyperedge for refinement
        hyperedge.R = 1

        print(f"[{self.name}] Marked quadrilateral hyperedge for refinement (R: 0 -> 1)")
        print(f"[{self.name}] Hyperedge: {hyperedge}")

        return {
            'marked_hyperedge': hyperedge,
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
