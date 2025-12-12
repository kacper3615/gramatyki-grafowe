from productions.production_base import Production

class P12(Production):
    """Production P12: Mark heptagonal element for refinement.
    It sets value of attribute R of the hyperedge with label T to 1
    """

    def __init__(self):
        super().__init__(
            name="P12",
            description="Mark heptagonal element for refinement"
        )

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """Check if P12 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            # Check if it's a heptagon (label T and 7 nodes)
            if edge.label != "T" or len(edge.nodes) != 7:
                continue

            # Check if R = 0 (not yet marked for refinement)
            if edge.R != 0:
                continue

            # Check refinement criterion
            if not refinement_criterion:
                continue

            # Find the 7 edges connecting the nodes
            nodes = edge.nodes
            edges_found = []

            for i in range(7):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 7]
                found_edge = graph.get_edge_between(node1, node2)
                if found_edge is None:
                    break
                edges_found.append(found_edge)

            if len(edges_found) == 7:
                return True, {
                    'hyperedge': edge,
                    'nodes': nodes,
                    'edges': edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """Apply P12 to mark the heptagon for refinement."""
        hyperedge = matched_elements['hyperedge']

        # Mark the hyperedge for refinement
        hyperedge.R = 1

        print(f"[{self.name}] Marked heptagonal hyperedge for refinement (R: 0 -> 1)")
        print(f"[{self.name}] Hyperedge: {hyperedge}")

        return {
            'marked_hyperedge': hyperedge,
            'nodes': matched_elements['nodes'],
            'edges': matched_elements['edges']
        }
