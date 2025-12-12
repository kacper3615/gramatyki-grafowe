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

    def test_can_apply_with_hanging_node(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        h_node = self.graph.add_node(1, 0, is_hanging=True)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched['edge'], e_shared)
        self.assertEqual(matched['hanging_node'], h_node)

    def test_cannot_apply_without_hanging_node(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_on_border_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)

        e = self.graph.add_edge(n1, n2, is_border=True)
        e.R = 1

        self.graph.add_node(1, 0, is_hanging=True)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_unmarked_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)

        e = self.graph.add_edge(n1, n2, is_border=False)
        e.R = 0

        self.graph.add_node(1, 0, is_hanging=True)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_apply_fixes_hanging_node_and_splits(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        h_node = self.graph.add_node(1, 0, is_hanging=True)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertNotIn(e_shared, self.graph.edges)

        self.assertFalse(h_node.is_hanging)
        self.assertIn(h_node, self.graph.nodes)

        new_edges = result['new_edges']
        self.assertEqual(len(new_edges), 2)

        for edge in new_edges:
            self.assertIn(edge, self.graph.edges)
            self.assertEqual(edge.R, 0)
            self.assertFalse(edge.is_border)


if __name__ == '__main__':
    unittest.main(verbosity=2)
