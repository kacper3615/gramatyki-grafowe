import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from hypergraph.hypergraph import HyperGraph
from productions.p12.p12 import P12


class TestP12(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P12()

    def test_can_apply_correct_heptagonal(self):
        """Test P2 can be applied to a correct quadrilateral."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply, "Production P12 should be applicable to correct heptagon")
        self.assertIsNotNone(matched, "Matched elements should not be None")
        self.assertEqual(matched['hyperedge'], heptagon)
        self.assertEqual(len(matched['nodes']), 7)
        self.assertEqual(len(matched['edges']), 7)

    def test_cannot_apply_missing_node_heptagon(self):
        """Test P12 cannot be applied when a node is missing in heptagon."""
        # Only 6 nodes
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n1, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="T")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P12 should not apply to incomplete heptagon")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_missing_edge_heptagon(self):
        """Test P12 cannot be applied when an edge is missing in heptagon."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        #missing: self.graph.add_edge(n7, n1, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P12 should not apply when edge is missing")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_wrong_label_heptagon(self):
        """Test P12 cannot be applied with wrong hyperedge label."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P12 should not apply with wrong label")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_already_marked_heptagon(self):
        """Test P12 cannot be applied when hyperedge is already marked (R=1)."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")
        heptagon.R = 1  # Already marked

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P12 should not apply when R=1")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_apply_marks_element_heptagon(self):
        """Test that applying P12 correctly marks the heptagon (R: 0 -> 1)."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        self.assertEqual(heptagon.R, 0, "Initial R should be 0")

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        self.assertEqual(heptagon.R, 1, "R should be 1 after applying P12")
        self.assertEqual(result['marked_hyperedge'].R, 1)

    def test_apply_preserves_graph_structure_heptagon(self):
        """Test that applying P12 doesn't damage surrounding graph structure."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)
        # Extra node
        n8 = self.graph.add_node(4, 1)

        # Heptagon edges
        e1 = self.graph.add_edge(n1, n2, is_border=True)
        e2 = self.graph.add_edge(n2, n3, is_border=True)
        e3 = self.graph.add_edge(n3, n4, is_border=True)
        e4 = self.graph.add_edge(n4, n5, is_border=True)
        e5 = self.graph.add_edge(n5, n6, is_border=True)
        e6 = self.graph.add_edge(n6, n7, is_border=True)
        e7 = self.graph.add_edge(n7, n1, is_border=True)
        # Extra edge
        e8 = self.graph.add_edge(n4, n8, is_border=False)

        heptagon = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        initial_node_count = len(self.graph.nodes)
        initial_edge_count = len(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P12 should be applicable")
        self.production.apply(self.graph, matched)

        # Verify graph structure is preserved
        self.assertEqual(len(self.graph.nodes), initial_node_count, "Node count should not change")
        self.assertEqual(len(self.graph.edges), initial_edge_count, "Edge count should not change")
        self.assertIn(e8, self.graph.edges, "Extra edge should still exist")
        self.assertIn(n8, self.graph.nodes, "Extra node should still exist")

    def test_visualization_before_after_heptagon(self):
        """Test visualization of heptagon before and after applying P12."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
        os.makedirs(output_dir, exist_ok=True)

        before_path = os.path.join(output_dir, 'test_p12_before.png')
        self.graph.visualize(before_path)
        self.assertTrue(os.path.exists(before_path), "Before visualization should be created")

        # Apply production
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P12 should be applicable")
        self.production.apply(self.graph, matched)

        # Visualize after
        after_path = os.path.join(output_dir, 'test_p12_after.png')
        self.graph.visualize(after_path)
        self.assertTrue(os.path.exists(after_path), "After visualization should be created")

    def test_in_larger_graph_heptagons(self):
        """Test P12 can find and mark heptagon embedded in larger graph with shared nodes."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon1 = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        # Second heptagon sharing nodes n3, n4, n5
        n8 = self.graph.add_node(4, 1.5)
        n9 = self.graph.add_node(5, 1)
        n10 = self.graph.add_node(4.5, 0)
        n11 = self.graph.add_node(3.5, -0.5)
        n12 = self.graph.add_node(2.5, 0.5)

        self.graph.add_edge(n3, n8, is_border=True)
        self.graph.add_edge(n8, n9, is_border=True)
        self.graph.add_edge(n9, n10, is_border=True)
        self.graph.add_edge(n10, n11, is_border=True)
        self.graph.add_edge(n11, n12, is_border=True)
        self.graph.add_edge(n12, n4, is_border=True)
        self.graph.add_edge(n4, n3, is_border=True)

        heptagon2 = self.graph.add_hyperedge([n3, n8, n9, n10, n11, n12, n4], label="T")

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Should find at least one heptagon in the larger graph")

    def test_apply_to_multiple_heptagons(self):
        """Test P12 can be applied to multiple heptagons in a larger graph."""
        n1 = self.graph.add_node(0, 1)
        n2 = self.graph.add_node(1, 2)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(3, 1)
        n5 = self.graph.add_node(2.5, 0)
        n6 = self.graph.add_node(1.5, -0.5)
        n7 = self.graph.add_node(0.5, 0)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n7, is_border=True)
        self.graph.add_edge(n7, n1, is_border=True)

        heptagon1 = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6, n7], label="T")

        # Second heptagon sharing some nodes
        n8 = self.graph.add_node(4, 1.5)
        n9 = self.graph.add_node(5, 1)
        n10 = self.graph.add_node(4.5, 0)
        n11 = self.graph.add_node(3.5, -0.5)
        n12 = self.graph.add_node(2.5, 0.5)

        self.graph.add_edge(n3, n8, is_border=True)
        self.graph.add_edge(n8, n9, is_border=True)
        self.graph.add_edge(n9, n10, is_border=True)
        self.graph.add_edge(n10, n11, is_border=True)
        self.graph.add_edge(n11, n12, is_border=True)
        self.graph.add_edge(n12, n4, is_border=True)
        self.graph.add_edge(n4, n3, is_border=True)

        heptagon2 = self.graph.add_hyperedge([n3, n8, n9, n10, n11, n12, n4], label="T")

        # Apply production to first heptagon
        can_apply1, matched1 = self.production.can_apply(self.graph)
        self.assertTrue(can_apply1, "Should find at least one heptagon")
        self.production.apply(self.graph, matched1)

        self.assertEqual(heptagon1.R, 1, "First heptagon should be marked after application")

        # Apply production again to find the second heptagon
        can_apply2, matched2 = self.production.can_apply(self.graph)
        self.assertTrue(can_apply2, "Should find second heptagon")
        self.production.apply(self.graph, matched2)

        self.assertEqual(heptagon2.R, 1, "Second heptagon should be marked after application")


if __name__ == '__main__':
    unittest.main(verbosity=2)
