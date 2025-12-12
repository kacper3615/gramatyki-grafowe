from productions.production_base import Production

class P11(Production):
    """Production P11: Break the hexagonal element marked for refinement, if all its edges are broken.
    It sets value of attribute R of new hyperedges with label Q to 0.
    """

    def __init__(self):
        super().__init__(
            name="P11",
            description="Break the hexagonal element marked for refinement, if all its edges are broken."
        )
    
    def _get_node_between(self, graph, node1, node2, desired_R=None):
        """
        Find and return a node between node1 and node2 [that is a hanging node].
        Args:
            graph: HyperGraph instance
            node1: First node
            node2: Second node
            desired_R: Desired refinement flag of the edges connecting to the node
        Returns:
            Node instance if found, None otherwise
        """
        for node in graph.nodes:
            
            if node == node1 or node == node2:
                continue

            # if not node.is_hanging:
            #     continue

            edge1 = graph.get_edge_between(node1, node)
            edge2 = graph.get_edge_between(node, node2)
            if not edge1 or not edge2:
                continue

            if (desired_R is None or (edge1.R == desired_R and edge2.R == desired_R)):
                return node
        
        return None


    def can_apply(self, graph, hyperedge=None, refinement_criterion=True):
        """Check if P11 can be applied to the graph.

        Args:
            refinement_criterion: External condition (e.g., error estimate) to decide if element should be refined
        """
        hyperedges_to_check = [hyperedge] if hyperedge else graph.edges
        if hyperedge and not refinement_criterion:
            return False, None

        for edge in hyperedges_to_check:
            if not edge.is_hyperedge():
                continue

            # Check if it's a hexagonal (label S and 6 nodes)
            if edge.label != "S" or len(edge.nodes) != 6:
                continue

            # Check if R = 1 (marked for refinement)
            if edge.R != 1:
                continue

            nodes = edge.nodes
            nodes_found = []
            edges_found = []
            
            for i in range(6):
                nodeA = nodes[i]
                nodeB = nodes[(i + 1) % 6]
                nodes_found.append(nodeA)

                # Get node between node1 and node2 (A -- C -- B)
                nodeC = self._get_node_between(graph, nodeA, nodeB, desired_R=0)
                if not nodeC:
                    break
                nodes_found.append(nodeC)
                
                edgeAC = graph.get_edge_between(nodeA, nodeC)
                edgeCB = graph.get_edge_between(nodeC, nodeB)
                if not edgeAC or not edgeCB:
                    break
                edges_found.append(edgeAC)
                edges_found.append(edgeCB)

            if len(nodes_found) == 12 and len(edges_found) == 12:
                return True, {
                    'hyperedge': edge,
                    'nodes': nodes_found,   # Even indices are original nodes, odd indices are hanging nodes
                    'edges': edges_found
                }

        return False, None

    def apply(self, graph, matched_elements):
        """Apply P11 to break the hexagonal element marked"""
        hexa_hyperedge = matched_elements['hyperedge']
        hexa_nodes = matched_elements['nodes']
        hexa_edges = matched_elements['edges']

        new_quadrilaterals = []

        # Indices of original corner nodes in the hexa_nodes list
        convex_hull_nodes_indices = [i for i in range(0, len(hexa_nodes)) if i % 2 == 0]
        assert len(convex_hull_nodes_indices) == 6, "There should be 6 corner nodes in the hexagon."

        # I. Create new central node
        new_node = graph.add_node(
            x=sum(hexa_nodes[i].x for i in convex_hull_nodes_indices) / 6,
            y=sum(hexa_nodes[i].y for i in convex_hull_nodes_indices) / 6,
            # z=sum(hexa_nodes[i].z for i in convex_hull_nodes_indices) / 6,
            is_hanging=False,
            label="V"
        )

        # II. Create 6 new quadrilateral hyperedges with R=0
        for i in range(6):
            n3_idx = i * 2  # Index of the corner node in hexa_nodes

            n1 = new_node
            n2 = hexa_nodes[((n3_idx - 1) + 12) % 12]   # before corner node
            n3 = hexa_nodes[n3_idx]
            n4 = hexa_nodes[(n3_idx + 1) % 12]          # after corner node

            quad_hyperedge = graph.add_hyperedge(
                nodes=[n1, n2, n3, n4],
                label="Q"
            )
            quad_hyperedge.R = 0
            new_quadrilaterals.append(quad_hyperedge)
        
        # III. Create edges connecting new central node to hanging nodes
        for i in range(6):
            n2_idx = i * 2 + 1  # Index of the hanging node in hexa_nodes
            
            n1 = new_node
            n2 = hexa_nodes[n2_idx]
            graph.add_edge(n1, n2, is_border=False, label="E")

            #* Mark hanging node as non-hanging
            hexa_nodes[n2_idx].is_hanging = False            

        # IV. Remove the original hyperedge
        graph.remove_edge(hexa_hyperedge)

        print(f"[{self.name}] Broken hexagonal hyperedge into 6 quadrilateral hyperedges.")
        print(f"[{self.name}] Hyperedge: {hexa_hyperedge} - but it's already removed.")

        return {
            'central_node': new_node,
            'quadrilaterals': new_quadrilaterals,
        }
