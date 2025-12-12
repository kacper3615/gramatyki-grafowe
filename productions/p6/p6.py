from productions.production_base import Production


class P6(Production):
    """
    Production P6: Mark pentagonal element for refinement.
    It sets value of attribute R of the hyperedge with label P to 1.
    """

    def __init__(self):
        super().__init__(
            name="P6",
            description="Mark pentagonal element for refinement"
        )

    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """
        Check if P6 can be applied to the graph.
        """

        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            # must be hyperedge
            if not edge.is_hyperedge():
                continue

            # must be pentagon (label P and 5 nodes)
            if edge.label != "P" or len(edge.nodes) != 5:
                continue

            # must not be already marked
            if edge.R != 0:
                continue

            # external refinement criterion
            if not refinement_criterion:
                continue

            # check if all 5 surrounding edges E exist
            nodes = edge.nodes
            edges_found = []

            for i in range(5):
                n1 = nodes[i]
                n2 = nodes[(i + 1) % 5]
                found_edge = graph.get_edge_between(n1, n2)
                if found_edge is None:
                    break
                edges_found.append(found_edge)

            if len(edges_found) == 5:
                return True, {
                    "hyperedge": edge,
                    "nodes": nodes,
                    "edges": edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """
        Mark the pentagon hyperedge (label P) for refinement.
        """

        hyperedge = matched_elements["hyperedge"]

        # mark for refinement
        hyperedge.R = 1

        print(f"[{self.name}] Marked pentagon hyperedge for refinement (R: 0 -> 1)")
        print(f"[{self.name}] Hyperedge: {hyperedge}")

        return {
            "marked_hyperedge": hyperedge,
            "nodes": matched_elements["nodes"],
            "edges": matched_elements["edges"]
        }
