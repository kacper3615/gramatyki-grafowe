from productions.production_base import Production


class P3(Production):
    """Production P3: Break a shared edge marked for refinement.

    - Finds a 2-node edge (label "E") that is shared (is_border == False) and has R == 1.
    - If the edge was not already broken (no hanging midpoint node present), it creates a
      hanging midpoint node and replaces the original edge with two edges.
    """

    def __init__(self):
        super().__init__(name="P3", description="Break shared edge marked for refinement")

    def _midpoint(self, n1, n2):
        return ( (n1.x + n2.x) / 2.0, (n1.y + n2.y) / 2.0 )

    def _has_midpoint_node(self, graph, n1, n2):
        # compute the perpendicularly shifted midpoint used when creating hanging nodes
        mx, my = self._midpoint(n1, n2)
        tol = 1e-6
        for node in graph.nodes:
            if abs(node.x - mx) <= tol and abs(node.y - my) <= tol:
                # ensure this node is connected to both endpoints
                connected_to_n1 = False
                connected_to_n2 = False
                for e in graph.edges:
                    if not e.is_hyperedge():
                        if (e.nodes[0] == n1 and e.nodes[1] == node) or (e.nodes[0] == node and e.nodes[1] == n1):
                            connected_to_n1 = True
                        if (e.nodes[0] == n2 and e.nodes[1] == node) or (e.nodes[0] == node and e.nodes[1] == n2):
                            connected_to_n2 = True
                if connected_to_n1 and connected_to_n2:
                    return True
        return False

    def can_apply(self, graph, edge=None):
        """Check if P3 can be applied.

        Args:
            graph: HyperGraph instance
            edge: optional specific 2-node edge to check

        Returns:
            (bool, dict) same convention as Production.can_apply
        """
        edges_to_check = [edge] if edge else graph.edges

        for e in edges_to_check:
            if e.is_hyperedge():
                continue

            # Must be a regular edge labeled "E"
            if e.label != "E":
                continue

            # Must be marked for refinement
            if e.R != 1:
                continue

            # Must be shared (not a border edge)
            if e.is_border:
                continue

            n1, n2 = e.nodes[0], e.nodes[1]

            # Check if it was already broken (midpoint hanging node exists)
            if self._has_midpoint_node(graph, n1, n2):
                continue

            # Found candidate
            return True, {"edge": e, "nodes": (n1, n2)}

        return False, None

    def apply(self, graph, matched_elements):
        """Apply P3: create hanging midpoint and split the edge."""
        edge = matched_elements["edge"]
        n1, n2 = matched_elements["nodes"]

        # compute midpoint coordinates
        mx, my = self._midpoint(n1, n2)

        # create hanging midpoint node
        mid = graph.add_node(mx, my)
        mid.z = (n1.z + n2.z) / 2.0

        # add two new edges; preserve original is_border flag
        e1 = graph.add_edge(n1, mid, is_border=edge.is_border)
        e2 = graph.add_edge(mid, n2, is_border=edge.is_border)

        # Reset refinement flag on new edges (default 0) and ensure new edges label is "E"
        e1.R = 0
        e2.R = 0
        e1.label = "E"
        e2.label = "E"

        # Mark the original edge as no longer marked for refinement
        edge.R = 0

        print(f"[{self.name}] Broke edge between {n1} and {n2} into two edges with midpoint {mid} (original edge kept)")

        return {
            "original_edge": edge,
            "midpoint_node": mid,
            "new_edges": (e1, e2),
        }
