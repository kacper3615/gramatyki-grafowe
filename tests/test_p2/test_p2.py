import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p2.p2 import P2


class TestP2(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P2()

    def test_can_apply_correct_configuration(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "E"
        target_edge.R = 1

        self.graph.add_edge(n1, n3, is_border=False)
        self.graph.add_edge(n2, n3, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["edge_to_remove"], target_edge)
        self.assertEqual(len(matched["neighbor_edges"]), 2)

    def test_apply_removes_edge_and_resets_neighbors(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "E"
        target_edge.R = 1

        e1 = self.graph.add_edge(n1, n3, is_border=False)
        e1.label = "E"
        e1.R = 1

        e2 = self.graph.add_edge(n2, n3, is_border=False)
        e2.label = "E"

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertNotIn(target_edge, self.graph.edges)
        self.assertEqual(e1.R, 0)
        self.assertEqual(e2.R, 0)

    def test_cannot_apply_on_border_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=True)
        target_edge.label = "E"
        target_edge.R = 1

        self.graph.add_edge(n1, n3, is_border=False)
        self.graph.add_edge(n2, n3, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_if_r_is_zero(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "E"
        target_edge.R = 0

        self.graph.add_edge(n1, n3, is_border=False)
        self.graph.add_edge(n2, n3, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_wrong_label(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "Q"
        target_edge.R = 1

        self.graph.add_edge(n1, n3, is_border=False)
        self.graph.add_edge(n2, n3, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_no_common_neighbor_node(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(1, -1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "E"
        target_edge.R = 1

        self.graph.add_edge(n1, n3, is_border=False)
        self.graph.add_edge(n2, n4, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_if_only_one_neighbor_edge_exists(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(1, 1)

        target_edge = self.graph.add_edge(n1, n2, is_border=False)
        target_edge.label = "E"
        target_edge.R = 1

        self.graph.add_edge(n1, n3, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)


if __name__ == "__main__":
    unittest.main(verbosity=2)