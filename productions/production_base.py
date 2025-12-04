class Production:
    """Base class for hypergraph grammar productions.

    Each production represents a graph transformation rule with:
    - Left-hand side (LHS): pattern to match
    - Right-hand side (RHS): replacement pattern
    """

    def __init__(self, name, description):
        """Initialize production.

        Args:
            name: Production identifier (eg, "P0", "P1")
            description: Human-readable description of the production
        """
        self.name = name
        self.description = description

    def can_apply(self, graph, **kwargs):
        """Check if production can be applied to the graph.

        Args:
            graph: HyperGraph instance
            **kwargs: Additional parameters for pattern matching

        Returns:
            tuple: (can_apply: bool, matched_elements: dict or None)
                  - can_apply: True if pattern matches, False otherwise
                  - matched_elements: Dictionary of matched graph elements if True, None otherwise
        """
        raise NotImplementedError(f"Production {self.name} must implement can_apply()")

    def apply(self, graph, matched_elements):
        """Apply the production transformation to the graph.

        Args:
            graph: HyperGraph instance
            matched_elements: Dictionary of matched elements from can_apply()

        Returns:
            dict: Dictionary containing the transformed/created elements
        """
        raise NotImplementedError(f"Production {self.name} must implement apply()")

    def __str__(self):
        return f"Production {self.name}: {self.description}"
