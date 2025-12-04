import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from hypergraph.hypergraph import HyperGraph
from productions import P0


class TestP0(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P0()

    def test_can_apply_correct_quadrilateral(self):
        """Test P0 can be applied to a correct quadrilateral (isomorphic to LHS)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply, "Production P0 should be applicable to correct quadrilateral")
        self.assertIsNotNone(matched, "Matched elements should not be None")
        self.assertEqual(matched['hyperedge'], q)
        self.assertEqual(len(matched['nodes']), 4)
        self.assertEqual(len(matched['edges']), 4)

    def test_cannot_apply_missing_node(self):
        """Test P0 cannot be applied when a node is missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)

        # Create hyperedge with only 3 nodes (should not match Q)
        self.graph.add_hyperedge([n1, n2, n3], label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P0 should not apply to incomplete quadrilateral")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_missing_edge(self):
        """Test P0 cannot be applied when an edge is missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        # missing edge between n4 and n1
        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P0 should not apply when edge is missing")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_wrong_label(self):
        """Test P0 cannot be applied with wrong hyperedge label."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3, n4], label="P")  # Wrong label

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P0 should not apply with wrong label")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_already_marked(self):
        """Test P0 cannot be applied when element is already marked (R=1)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1  # Already marked

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P0 should not apply when R=1")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_apply_marks_element(self):
        """Test that applying P0 correctly marks the element (R: 0 -> 1)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        self.assertEqual(q.R, 0, "Initial R should be 0")

        
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertEqual(q.R, 1, "R should be 1 after applying P0")
        self.assertEqual(result['marked_hyperedge'].R, 1)

    def test_apply_preserves_graph_structure(self):
        """Test that applying P0 doesn't damage surrounding graph structure."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)
        n5 = self.graph.add_node(2, 0)  # Extra node

        e1 = self.graph.add_edge(n1, n2, is_border=True)
        e2 = self.graph.add_edge(n2, n3, is_border=True)
        e3 = self.graph.add_edge(n3, n4, is_border=True)
        e4 = self.graph.add_edge(n4, n1, is_border=True)
        e5 = self.graph.add_edge(n2, n5, is_border=False)  # Extra edge

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        initial_node_count = len(self.graph.nodes)
        initial_edge_count = len(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        # Verify graph structure is preserved
        self.assertEqual(len(self.graph.nodes), initial_node_count, "Node count should not change")
        self.assertEqual(len(self.graph.edges), initial_edge_count, "Edge count should not change")
        self.assertIn(e5, self.graph.edges, "Extra edge should still exist")
        self.assertIn(n5, self.graph.nodes, "Extra node should still exist")

    def test_visualization_before_after(self):
        """Test visualization of graph before and after applying P0."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
        os.makedirs(output_dir, exist_ok=True)

        before_path = os.path.join(output_dir, 'test_p0_before.png')
        self.graph.visualize(before_path)
        self.assertTrue(os.path.exists(before_path), "Before visualization should be created")

        # Apply production
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        # Visualize after
        after_path = os.path.join(output_dir, 'test_p0_after.png')
        self.graph.visualize(after_path)
        self.assertTrue(os.path.exists(after_path), "After visualization should be created")

    def test_in_larger_graph(self):
        """Test P0 can find and mark quadrilateral embedded in larger graph."""
        # Create multiple quadrilaterals
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=False)  # Shared edge
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        q1 = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")

        # sharing edge with first
        n5 = self.graph.add_node(2, 0)
        n6 = self.graph.add_node(2, 1)

        self.graph.add_edge(n2, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n3, is_border=True)

        q2 = self.graph.add_hyperedge([n2, n5, n6, n3], label="Q")

        # Both should be applicable
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Should find at least one quadrilateral")


if __name__ == '__main__':
    unittest.main(verbosity=2)
