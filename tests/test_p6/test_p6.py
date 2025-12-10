import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p6.p6 import P6


class TestP6(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P6()

    def test_can_apply_correct_pentagon(self):
        """Test P6 can be applied to a correct pentagon."""
        n = [self.graph.add_node(i, i * 0.5) for i in range(5)]

        # Create 5 edges
        for i in range(5):
            self.graph.add_edge(n[i], n[(i + 1) % 5], is_border=True)

        p = self.graph.add_hyperedge(n, label="P")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["hyperedge"], p)
        self.assertEqual(len(matched["nodes"]), 5)
        self.assertEqual(len(matched["edges"]), 5)

    def test_cannot_apply_missing_node(self):
        """Test P6 cannot be applied to hyperedge with < 5 nodes."""
        n = [self.graph.add_node(i, 0) for i in range(4)]

        for i in range(3):
            self.graph.add_edge(n[i], n[i+1], is_border=True)

        self.graph.add_hyperedge(n, label="P")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_missing_edge(self):
        """Test P6 cannot be applied when at least one required edge is missing."""
        n = [self.graph.add_node(i, i) for i in range(5)]

        # Missing last edge between node4 -> node0
        for i in range(4):
            self.graph.add_edge(n[i], n[i+1], is_border=False)

        self.graph.add_hyperedge(n, label="P")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_wrong_label(self):
        """Test P6 should not apply to non-P hyperedges."""
        n = [self.graph.add_node(i, i) for i in range(5)]

        for i in range(5):
            self.graph.add_edge(n[i], n[(i+1) % 5], is_border=True)

        self.graph.add_hyperedge(n, label="Q")  # Wrong label

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_already_marked(self):
        """Test P6 cannot be applied when hyperedge is already R=1."""
        n = [self.graph.add_node(i, i * 0.2) for i in range(5)]

        for i in range(5):
            self.graph.add_edge(n[i], n[(i+1) % 5], is_border=True)

        p = self.graph.add_hyperedge(n, label="P")
        p.R = 1

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_apply_marks_element(self):
        """Test that P6 sets R: 0 -> 1."""
        n = [self.graph.add_node(i, i * 0.3) for i in range(5)]

        for i in range(5):
            self.graph.add_edge(n[i], n[(i+1) % 5], is_border=False)

        p = self.graph.add_hyperedge(n, label="P")

        self.assertEqual(p.R, 0)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertEqual(p.R, 1)
        self.assertEqual(result["marked_hyperedge"].R, 1)

    def test_in_larger_graph(self):
        """Test P6 finds a pentagon inside a larger graph."""
        # first pentagon
        n = [self.graph.add_node(i, i * 0.5) for i in range(5)]
        for i in range(5):
            self.graph.add_edge(n[i], n[(i+1) % 5], is_border=True)
        p1 = self.graph.add_hyperedge(n, label="P")

        # extra nodes/edges
        a = self.graph.add_node(10, 10)
        b = self.graph.add_node(11, 10)
        self.graph.add_edge(a, b, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertEqual(matched["hyperedge"], p1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
