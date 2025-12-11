from productions.production_base import Production


class P2(Production):
    """
    Production P2 breaks shared edges marked for refinement, if the edge was already broken by neighboring element.
    It sets value of attribute R of each hyperedge with label E to 0.
    """

    def __init__(self):
        super().__init__("P2", "Remove broken edge")

    def can_apply(self, graph, **kwargs):
        for edge in graph.edges:
            if not edge.is_hyperedge() and edge.label == "E" and edge.R == 1 and not edge.is_border:
                n1, n2 = edge.nodes
                n1_edges = []
                n2_edges = []
                for e in graph.edges:
                    if e == edge or e.is_hyperedge():
                        continue
                    if n1 in e.nodes:
                        n1_edges.append(e)
                    elif n2 in e.nodes:
                        n2_edges.append(e)
                for n1_edge in n1_edges:
                    for n2_edge in n2_edges:
                        if len(set(n1_edge.nodes) | set(n2_edge.nodes)) == 3:
                            return True, {
                                "edge_to_remove": edge,
                                "neighbor_edges": (n1_edge, n2_edge)
                            }
        return False, None

    def apply(self, graph, matched_elements):
        edge_to_remove = matched_elements['edge_to_remove']
        neighbor_edges = matched_elements['neighbor_edges']

        graph.remove_edge(edge_to_remove)

        for e in neighbor_edges:
            if e.label == "E":
                e.R = 0

        return {
            "removed_edge": edge_to_remove,
            "neighbor_edges": neighbor_edges
        }
