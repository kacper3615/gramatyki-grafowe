from hypergraph.node import Node


class Edge:
    def __init__(
        self, nodes: list[Node] | tuple[Node, ...], is_border=False, label=None, R=0
    ):
        self.nodes = nodes
        self.B = is_border
        self.label = label if label else ("E" if len(self.nodes) == 2 else "Q")
        self.R = R  # Refinement flag


        if len(self.nodes) > 2:
            self.x = sum(node.x for node in self.nodes) / len(self.nodes)
            self.y = sum(node.y for node in self.nodes) / len(self.nodes)
        else:
            self.x = None
            self.y = None

    def is_hyperedge(self):
        return len(self.nodes) > 2

    def __str__(self):
        if self.is_hyperedge():
            return f"HyperEdge({self.x:.2f}, {self.y:.2f}, label={self.label}, R={self.R}, nodes={len(self.nodes)})"
        else:
            return f"Edge({self.nodes[0]} - {self.nodes[1]}, B={self.B}, R={self.R}, label={self.label})"
