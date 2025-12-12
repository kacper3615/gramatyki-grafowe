from productions.production_base import Production


class P7(Production):

    '''
    Production P7: marks edges of pentagonal element, 
    marked for refinement, for breaking,
    it sets value of attribute R of each hyperedge with label E to 1
    '''

    def __init__(self):
        super().__init__(
            name="P7",
            description="Mark edges of pentagonal element for breaking",
        )

    def can_apply(self, graph, hyperedge=None):

        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            if edge.label != "P" or len(edge.nodes) != 5 or edge.R != 1:
                continue

            nodes = edge.nodes
            edges_found = []

            for i in range(5):
                node1 = nodes[i]
                node2 = nodes[(i + 1) % 5]
                found_edge = graph.get_edge_between(node1, node2)
                if found_edge is None or found_edge.label != "E":
                    break
                edges_found.append(found_edge)

            if len(edges_found) == 5:
                return True, {
                    "hyperedge": edge,
                    "nodes": nodes,
                    "edges": edges_found,
                }

        return False, None

    def apply(self, graph, matched_elements):

        for e in matched_elements["edges"]:
            e.R = 1

        print("Successfully applied P7")

        return {
            "hyperedge": matched_elements["hyperedge"],
            "nodes": matched_elements["nodes"],
            "marked_edges": matched_elements["edges"],
        }
