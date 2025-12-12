import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from hypergraph.hypergraph import HyperGraph
from productions import P11


class TestP11(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P11()

    def test_can_apply_correct_hexagon(self):
        """Test P11 can be applied to a correct hexagon (isomorphic to LHS)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        self.graph.add_edge(n12, n2, is_border=True)
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n56, is_border=True)
        self.graph.add_edge(n56, n6, is_border=True)
        self.graph.add_edge(n6, n61, is_border=True)
        self.graph.add_edge(n61, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply, "Production P11 should be applicable to correct hexagon")
        self.assertIsNotNone(matched, "Matched elements should not be None")
        self.assertEqual(matched['hyperedge'], h)
        self.assertEqual(len(matched['nodes']), 12)
        self.assertEqual(len(matched['edges']), 12)
    
    def test_cannot_apply_wrong_label(self):
        """Test P11 cannot be applied with wrong hyperedge label."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        self.graph.add_edge(n12, n2, is_border=True)
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n56, is_border=True)
        self.graph.add_edge(n56, n6, is_border=True)
        self.graph.add_edge(n6, n61, is_border=True)
        self.graph.add_edge(n61, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="H")  # Wrong label
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Production P11 should not apply with wrong hyperedge label")
        self.assertIsNone(matched, "Matched elements should be None")
    
    def test_cannot_apply_to_not_marked(self):
        """Test P11 cannot be applied when element is not marked (R!=1)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        self.graph.add_edge(n12, n2, is_border=True)
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n56, is_border=True)
        self.graph.add_edge(n56, n6, is_border=True)
        self.graph.add_edge(n6, n61, is_border=True)
        self.graph.add_edge(n61, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 0  # Marked as not for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Production P11 should not apply when element is not marked (R!=1)")
        self.assertIsNone(matched, "Matched elements should be None")
    
    def test_hyperedge_marking_in_new_quadrilaterals(self):
        """Test that new quadrilaterals created by P11 has correctly marked hyperedges."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12)
        self.graph.add_edge(n12, n2)
        self.graph.add_edge(n2, n23)
        self.graph.add_edge(n23, n3)
        self.graph.add_edge(n3, n34)
        self.graph.add_edge(n34, n4)
        self.graph.add_edge(n4, n45)
        self.graph.add_edge(n45, n5)
        self.graph.add_edge(n5, n56)
        self.graph.add_edge(n56, n6)
        self.graph.add_edge(n6, n61)
        self.graph.add_edge(n61, n1)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P11 should be applicable to correct hexagon")
        
        result = self.production.apply(self.graph, matched)
        self.assertIsNotNone(result)

        quad_hyperedges = result['quadrilaterals']
        self.assertEqual(len(quad_hyperedges), 6, "There should be 6 new quadrilateral hyperedges created")
        is_marked_correctly = all(he.R == 0 for he in quad_hyperedges)
        self.assertTrue(is_marked_correctly, "All new quadrilateral hyperedges should be marked with R=0")

    def test_new_node_correct_coords(self):
        """Test that the new central node created by P11 has correct coordinates."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1.1, 0.843)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1.0002, 1.712)
        n5 = self.graph.add_node(-0.023, 1.832)
        n6 = self.graph.add_node(-0.51, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12)
        self.graph.add_edge(n12, n2)
        self.graph.add_edge(n2, n23)
        self.graph.add_edge(n23, n3)
        self.graph.add_edge(n3, n34)
        self.graph.add_edge(n34, n4)
        self.graph.add_edge(n4, n45)
        self.graph.add_edge(n45, n5)
        self.graph.add_edge(n5, n56)
        self.graph.add_edge(n56, n6)
        self.graph.add_edge(n6, n61)
        self.graph.add_edge(n61, n1)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P11 should be applicable to correct hexagon")

        result = self.production.apply(self.graph, matched)
        self.assertIsNotNone(result)
        central_node = result['central_node']
        expected_x = (n1.x + n2.x + n3.x + n4.x + n5.x + n6.x) / 6
        expected_y = (n1.y + n2.y + n3.y + n4.y + n5.y + n6.y) / 6
        expected_z = (n1.z + n2.z + n3.z + n4.z + n5.z + n6.z) / 6

        self.assertAlmostEqual(central_node.x, expected_x, places=5, msg="Central node x-coordinate is incorrect")
        self.assertAlmostEqual(central_node.y, expected_y, places=5, msg="Central node y-coordinate is incorrect")
        self.assertAlmostEqual(central_node.z, expected_z, places=5, msg="Central node z-coordinate is incorrect")

    def test_cannot_apply_missing_node(self):
        """Test P11 cannot be applied when a corner node is missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        # Missing n6

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n51 = self.graph.add_node((n5.x + n1.x) / 2, (n5.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        self.graph.add_edge(n12, n2, is_border=True)
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n51, is_border=True)
        self.graph.add_edge(n51, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5], label="S")  # Missing n6
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Production P11 should not apply when a corner node is missing")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_missing_hanging_nodes(self):
        """Test P11 cannot be applied when hanging nodes are missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        # Missing hanging nodes

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n5, is_border=True)
        self.graph.add_edge(n5, n6, is_border=True)
        self.graph.add_edge(n6, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P11 should not apply when a hanging node is missing")
        self.assertIsNone(matched, "Matched elements should be None")
    
    def test_cannot_apply_missing_edge(self):
        """Test P11 cannot be applied when an edge is missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        # Missing edge between n12 and n2
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n56, is_border=True)
        self.graph.add_edge(n56, n6, is_border=True)
        self.graph.add_edge(n6, n61, is_border=True)
        self.graph.add_edge(n61, n1, is_border=True)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Production P11 should not apply when an edge is missing")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_apply_preserves_graph_structure(self):
        """Test that applying P11 doesn't damage surrounding graph structure."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)
        n_extra = self.graph.add_node(2, 2)  # Extra node

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12, is_border=True)
        self.graph.add_edge(n12, n2, is_border=True)
        self.graph.add_edge(n2, n23, is_border=True)
        self.graph.add_edge(n23, n3, is_border=True)
        self.graph.add_edge(n3, n34, is_border=True)
        self.graph.add_edge(n34, n4, is_border=True)
        self.graph.add_edge(n4, n45, is_border=True)
        self.graph.add_edge(n45, n5, is_border=True)
        self.graph.add_edge(n5, n56, is_border=True)
        self.graph.add_edge(n56, n6, is_border=True)
        self.graph.add_edge(n6, n61, is_border=True)
        self.graph.add_edge(n61, n1, is_border=True)
        e_extra = self.graph.add_edge(n2, n_extra)  # Extra edge

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        initial_node_count = len(self.graph.nodes)
        initial_edge_count = len(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P11 should be applicable to correct hexagon")
        result = self.production.apply(self.graph, matched)
        self.assertIsNotNone(result)

        final_node_count = len(self.graph.nodes)
        final_edge_count = len(self.graph.edges)

        self.assertEqual(
            final_node_count, 
            initial_node_count + 1,         # 1 new central node created
            "Node count after applying P11 is incorrect"
        )      
        self.assertEqual(
            final_edge_count, 
            initial_edge_count + 12 - 1,    # 12 new edges created, 1 removed (the hexagon hyperedge)
            "Edge count after applying P11 is incorrect"
        )

        self.assertIn(n_extra, self.graph.nodes, "Extra node should still be in the graph after applying P11")
        self.assertIn(e_extra, self.graph.edges, "Extra edge should still be in the graph after applying P11")
    
    def test_in_larger_graph(self):
        """Test applying P11 in a larger graph context."""
        # First hexagon
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12)
        self.graph.add_edge(n12, n2)
        self.graph.add_edge(n2, n23)
        self.graph.add_edge(n23, n3)
        self.graph.add_edge(n3, n34)
        self.graph.add_edge(n34, n4)
        self.graph.add_edge(n4, n45)
        self.graph.add_edge(n45, n5)
        self.graph.add_edge(n5, n56)
        self.graph.add_edge(n56, n6)
        self.graph.add_edge(n6, n61)
        self.graph.add_edge(n61, n1)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        # Second hexagon (sharing n1 and n12)
        n7 = n12
        n8 = self.graph.add_node(1.5, 0)
        n9 = self.graph.add_node(2, -0.866)
        n10 = self.graph.add_node(1.5, -1.732)
        n11 = self.graph.add_node(0.5, -1.732)  
        n12_2 = self.graph.add_node(0, -0.866)

        n78 = n2
        n89 = self.graph.add_node((n8.x + n9.x) / 2, (n8.y + n9.y) / 2, is_hanging=True)
        n910 = self.graph.add_node((n9.x + n10.x) / 2, (n9.y + n10.y) / 2, is_hanging=True)
        n1011 = self.graph.add_node((n10.x + n11.x) / 2, (n10.y + n11.y) / 2, is_hanging=True)
        n1112 = self.graph.add_node((n11.x + n12_2.x) / 2, (n11.y + n12_2.y) / 2, is_hanging=True)
        n127 = self.graph.add_node((n12_2.x + n7.x) / 2, (n12_2.y + n7.y) / 2, is_hanging=True)

        self.graph.add_edge(n7, n78)
        self.graph.add_edge(n78, n8)
        self.graph.add_edge(n8, n89)
        self.graph.add_edge(n89, n9)
        self.graph.add_edge(n9, n910)
        self.graph.add_edge(n910, n10)
        self.graph.add_edge(n10, n1011)
        self.graph.add_edge(n1011, n11)
        self.graph.add_edge(n11, n1112)
        self.graph.add_edge(n1112, n12_2)
        self.graph.add_edge(n12_2, n127)
        self.graph.add_edge(n127, n7)

        h2 = self.graph.add_hyperedge([n7, n8, n9, n10, n11, n12_2], label="S")
        h2.R = 1  # Mark for refinement

        # Some extra nodes and edges in the graph
        n_extra1 = self.graph.add_node(-3, 3)
        n_extra2 = self.graph.add_node(-1, -1)
        e_extra1 = self.graph.add_edge(n_extra1, n_extra2)
        e_extra2 = self.graph.add_edge(n56, n_extra1)
        e_extra3 = self.graph.add_edge(n1112, n_extra2)

        initial_node_count = len(self.graph.nodes)
        initial_edge_count = len(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply, "Production P11 should be applicable in larger graph context")
        result = self.production.apply(self.graph, matched)
        self.assertIsNotNone(result)

        final_node_count = len(self.graph.nodes)
        final_edge_count = len(self.graph.edges)

        # Verify that the graph structure is intact

        self.assertIn(n_extra1, self.graph.nodes, "Extra node 1 should still be in the graph after applying P11")
        self.assertIn(n_extra2, self.graph.nodes, "Extra node 2 should still be in the graph after applying P11")

        self.assertIn(e_extra1, self.graph.edges, "Extra edge 1 should still be in the graph after applying P11")
        self.assertIn(e_extra2, self.graph.edges, "Extra edge 2 should still be in the graph after applying P11")
        self.assertIn(e_extra3, self.graph.edges, "Extra edge 3 should still be in the graph after applying P11")
        
        self.assertEqual(
            final_node_count, 
            initial_node_count + 1,         # 1 new central node created
            "Node count after applying P11 is incorrect"
        )      
        self.assertEqual(
            final_edge_count, 
            initial_edge_count + 12 - 1,    # 12 new edges created, 1 removed (the hexagon hyperedge)
            "Edge count after applying P11 is incorrect"
        )

        remained_hexagons = len(list(filter(lambda e: e.label == "S", self.graph.edges)))
        self.assertEqual(remained_hexagons, 1, "One hexagon hyperedge should remain after applying P11 once")

    def test_visualization_before_after(self):
        """Test visualization of graph before and after applying P11."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1.5, 0.866)
        n4 = self.graph.add_node(1, 1.732)
        n5 = self.graph.add_node(0, 1.732)
        n6 = self.graph.add_node(-0.5, 0.866)

        n12 = self.graph.add_node((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, is_hanging=True)
        n23 = self.graph.add_node((n2.x + n3.x) / 2, (n2.y + n3.y) / 2, is_hanging=True)
        n34 = self.graph.add_node((n3.x + n4.x) / 2, (n3.y + n4.y) / 2, is_hanging=True)
        n45 = self.graph.add_node((n4.x + n5.x) / 2, (n4.y + n5.y) / 2, is_hanging=True)
        n56 = self.graph.add_node((n5.x + n6.x) / 2, (n5.y + n6.y) / 2, is_hanging=True)
        n61 = self.graph.add_node((n6.x + n1.x) / 2, (n6.y + n1.y) / 2, is_hanging=True)

        self.graph.add_edge(n1, n12)
        self.graph.add_edge(n12, n2)
        self.graph.add_edge(n2, n23)
        self.graph.add_edge(n23, n3)
        self.graph.add_edge(n3, n34)
        self.graph.add_edge(n34, n4)
        self.graph.add_edge(n4, n45)
        self.graph.add_edge(n45, n5)
        self.graph.add_edge(n5, n56)
        self.graph.add_edge(n56, n6)
        self.graph.add_edge(n6, n61)
        self.graph.add_edge(n61, n1)

        h = self.graph.add_hyperedge([n1, n2, n3, n4, n5, n6], label="S")
        h.R = 1  # Mark for refinement

        output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
        os.makedirs(output_dir, exist_ok=True)

        before_path = os.path.join(output_dir, 'test_p11_before.png')
        self.graph.visualize(before_path)
        self.assertTrue(os.path.exists(before_path), "Before visualization should be created")

        # Apply production
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        # Visualize after
        after_path = os.path.join(output_dir, 'test_p11_after.png')
        self.graph.visualize(after_path)
        self.assertTrue(os.path.exists(after_path), "After visualization should be created")


if __name__ == '__main__':
    unittest.main(verbosity=2)