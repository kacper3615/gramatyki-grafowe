from productions.production_base import Production

class P10(Production):
    """
    Production P10: Marks edges of a hexagonal element marked for refinement (R=1)
    by setting the R attribute of each boundary edge (label E) to 1.
    """


    def __init__(self):
        super().__init__(
            name="P10",
            description="Mark edges of hexagonal element for breaking"
        )

    def can_apply(self, graph, hyperedge=None):
        """Check if P10 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            # Check if it's a hexagonal (label "S", 6 nodes, and already marked for refinement (R=1))
            if edge.label != "S" or len(edge.nodes) != 6 or edge.R != 1:
                continue


            # Find the 6 edges connecting the nodes
            nodes = edge.nodes
            edges_found = []

            for i in range(6):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 6]
                found_edge = graph.get_edge_between(node1, node2)
                if found_edge is None or found_edge.label != "E":
                    break
                edges_found.append(found_edge)

            if len(edges_found) == 6:
                return True, {
                    'hyperedge': edge,
                    'nodes': nodes,
                    'edges': edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """Apply P10 to mark the marked for refinement hexagonal edges for breaking."""

        for e in matched_elements["edges"]:
            e.R = 1

        print("Successfully applied P10! Marked edges for breaking.(E.R: 0 -> 1)")

        return {
            'hyperedge': matched_elements["hyperedge"],
            'nodes': matched_elements['nodes'],
            'marked_edges': matched_elements['edges']
        }
