from productions.production_base import Production


class P2(Production):
    """
    Production P2 breaks shared edges marked for refinement, if the edge was already broken by neighboring element
    it sets value of attribute R of each hyperedge with label E to 0
    """

    def __init__(self):
        super().__init__("P2", "Break shared edge with hanging node")

    def can_apply(self, graph, **kwargs):
        for edge in graph.edges:
            if edge.is_hyperedge() or edge.label != "E" or edge.R != 1 or edge.is_border:
                continue

            n1, n2 = edge.nodes
            hanging_node = self._find_hanging_node_on_edge(graph, n1, n2)

            if hanging_node is not None:
                return True, {
                    "edge": edge,
                    "hanging_node": hanging_node
                }

        return False, None

    def apply(self, graph, matched_elements):
        old_edge = matched_elements['edge']
        hanging_node = matched_elements['hanging_node']
        n1, n2 = old_edge.nodes

        graph.remove_edge(old_edge)
        hanging_node.is_hanging = False

        e1 = graph.add_edge(n1, hanging_node, is_border=False, label="E")
        e2 = graph.add_edge(hanging_node, n2, is_border=False, label="E")

        e1.R = 0
        e2.R = 0

        return {"new_edges": [e1, e2], "fixed_node": hanging_node}

    def _find_hanging_node_on_edge(self, graph, n1, n2):
        EPSILON = 1e-5

        for node in graph.nodes:
            if not node.is_hanging:
                continue

            mid_x = (n1.x + n2.x) / 2
            mid_y = (n1.y + n2.y) / 2

            if abs(node.x - mid_x) < EPSILON and abs(node.y - mid_y) < EPSILON:
                return node

        return None
