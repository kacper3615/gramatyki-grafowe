import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from hypergraph.hypergraph import HyperGraph
from productions import P3


class TestP3(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P3()

    def test_can_apply_on_marked_shared_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n1, is_border=True)

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched['edge'], e_shared)

    def test_cannot_apply_on_border_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_edge(n1, n2, is_border=True)
        e.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_unmarked_edge(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)

        e = self.graph.add_edge(n1, n2, is_border=False)
        e.R = 0

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_apply_splits_edge_and_creates_hanging_node(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 1)
        n1.z = 5.0
        n2.z = 2.0

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n1, is_border=True)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        # original edge should be kept
        self.assertIn(result['original_edge'], self.graph.edges)

        # midpoint node created
        mid = result['midpoint_node']
        self.assertIn(mid, self.graph.nodes)

        # two new edges exist
        e1, e2 = result['new_edges']
        self.assertIn(e1, self.graph.edges)
        self.assertIn(e2, self.graph.edges)

        # midpoint coordinates
        self.assertEqual(mid.x, 1.0)
        self.assertEqual(mid.y, 0.0)
        self.assertEqual(mid.z, 3.5)

    def test_cannot_apply_if_already_broken(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 1)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        # Simulate already broken: create midpoint and two edges
        mid = self.graph.add_node(1, 0)
        self.graph.remove_edge(e_shared)
        self.graph.add_edge(n1, mid, is_border=False)
        self.graph.add_edge(mid, n2, is_border=False)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_visualization_before_after(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 1)

        e_shared = self.graph.add_edge(n1, n2, is_border=False)
        e_shared.R = 1

        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n1, is_border=True)

        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
        os.makedirs(output_dir, exist_ok=True)

        before_path = os.path.join(output_dir, 'test_p3_before.png')
        self.graph.visualize(before_path)
        self.assertTrue(os.path.exists(before_path))

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        after_path = os.path.join(output_dir, 'test_p3_after.png')
        self.graph.visualize(after_path)
        self.assertTrue(os.path.exists(after_path))


if __name__ == '__main__':
    unittest.main(verbosity=2)
