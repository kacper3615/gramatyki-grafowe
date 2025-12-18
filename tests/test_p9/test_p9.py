import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p9.p9 import P9


class TestP9(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P9()

    def test_can_apply_correct_hexagon(self):
        """Test P9 can be applied to a correct hexagon with label 'S'."""
        n = [self.graph.add_node(i, i * 0.5) for i in range(6)]

        # Create 6 border edges forming a cycle
        for i in range(6):
            self.graph.add_edge(n[i], n[(i + 1) % 6], is_border=True)

        # Correct label: "S" for hexagonal element
        p = self.graph.add_hyperedge(n, label="S")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["hyperedge"], p)
        self.assertEqual(len(matched["nodes"]), 6)
        self.assertEqual(len(matched["edges"]), 6)

    def test_cannot_apply_wrong_label(self):
        """Test P9 cannot be applied when hyperedge has wrong label (not 'S')."""
        n = [self.graph.add_node(i, i) for i in range(6)]

        for i in range(6):
            self.graph.add_edge(n[i], n[(i + 1) % 6], is_border=True)

        self.graph.add_hyperedge(n, label="P")  # Wrong label

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_too_few_nodes(self):
        """Test P9 cannot be applied to hyperedge with fewer than 6 nodes."""
        n = [self.graph.add_node(i, 0) for i in range(5)]

        for i in range(5):
            self.graph.add_edge(n[i], n[(i + 1) % 5], is_border=True)

        self.graph.add_hyperedge(n, label="S")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_missing_edge(self):
        """Test P9 cannot be applied when at least one boundary edge is missing."""
        n = [self.graph.add_node(i, i) for i in range(6)]

        # Intentionally missing one edge (between n[5] and n[0])
        for i in range(5):
            self.graph.add_edge(n[i], n[i + 1], is_border=False)

        self.graph.add_hyperedge(n, label="S")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_already_marked(self):
        """Test P9 cannot be applied when hyperedge is already marked (R=1)."""
        n = [self.graph.add_node(i, i * 0.2) for i in range(6)]

        for i in range(6):
            self.graph.add_edge(n[i], n[(i + 1) % 6], is_border=True)

        p = self.graph.add_hyperedge(n, label="S")
        p.R = 1  # Already marked

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_apply_marks_element(self):
        """Test that applying P9 sets R from 0 to 1."""
        n = [self.graph.add_node(i, i * 0.3) for i in range(6)]

        for i in range(6):
            self.graph.add_edge(n[i], n[(i + 1) % 6], is_border=False)

        p = self.graph.add_hyperedge(n, label="S")

        self.assertEqual(p.R, False)  # Default is False (equivalent to 0)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertEqual(p.R, True)
        self.assertEqual(result["marked_hyperedge"].R, True)

    def test_in_larger_graph(self):
        """Test P9 correctly finds and can be applied to a hexagon inside a larger graph."""
        # Correct hexagon with label "S"
        n = [self.graph.add_node(i, i * 0.6) for i in range(6)]
        for i in range(6):
            self.graph.add_edge(n[i], n[(i + 1) % 6], is_border=True)
        p1 = self.graph.add_hyperedge(n, label="S")

        # Extra unrelated elements
        a = self.graph.add_node(10, 10)
        b = self.graph.add_node(11, 10)
        self.graph.add_edge(a, b, is_border=False)

        # Another hyperedge that should be ignored
        extra_nodes = [self.graph.add_node(20 + i, 20 + i) for i in range(5)]
        self.graph.add_hyperedge(extra_nodes, label="S")

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        # It should find one of the valid hexagons (the first one in this case)
        self.assertIn(matched["hyperedge"], {p1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
