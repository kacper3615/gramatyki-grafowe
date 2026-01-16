import unittest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p1.p1 import P1


class TestP1(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P1()

    def test_can_apply_correctly(self):
        """Test P1 can be applied to a quadrilateral with R=1."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        e1 = self.graph.add_edge(n1, n2, is_border=False)
        e2 = self.graph.add_edge(n2, n3, is_border=False)
        e3 = self.graph.add_edge(n3, n4, is_border=False)
        e4 = self.graph.add_edge(n4, n1, is_border=False)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1 # Marked for refinement

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply, "Production P1 should be applicable to marked quadrilateral")
        self.assertIsNotNone(matched)
        self.assertEqual(matched['hyperedge'], q)
        self.assertEqual(len(matched['edges']), 4)

    def test_cannot_apply_unmarked_hyperedge(self):
        """Test P1 cannot be applied if R=0."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=False)
        self.graph.add_edge(n2, n3, is_border=False)
        self.graph.add_edge(n3, n4, is_border=False)
        self.graph.add_edge(n4, n1, is_border=False)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 0 # Not marked

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P1 should not apply to unmarked quadrilateral")
        self.assertIsNone(matched)

    def test_cannot_apply_missing_node(self):
        """Test P1 cannot be applied if a node is missing (structure broken)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n1, n3, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)

        self.graph.add_hyperedge([n1, n2, n3], label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply, "Production P1 should not apply to incomplete quadrilateral")
        self.assertIsNone(matched, "Matched elements should be None")

    def test_cannot_apply_missing_edge(self):
        """Test P1 cannot be applied if a border edge is missing."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Should not apply if border edge is missing")

    def test_cannot_apply_wrong_label(self):
        """Test P1 checks for label 'Q'."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2)
        self.graph.add_edge(n2, n3)
        self.graph.add_edge(n3, n4)
        self.graph.add_edge(n4, n1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="P") # Wrong label
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Should not apply if label is not Q")

    def test_in_larger_graph(self):
        """Test P1 applies correctly when embedded in a larger graph."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        # Extra nodes/edges
        n5 = self.graph.add_node(2, 2)
        self.graph.add_edge(n3, n5)

        self.graph.add_edge(n1, n2)
        self.graph.add_edge(n2, n3)
        self.graph.add_edge(n3, n4)
        self.graph.add_edge(n4, n1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.assertEqual(matched['hyperedge'], q)

    def test_apply_marks_edges(self):
        """Test that applying P1 marks all 4 border edges."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        e1 = self.graph.add_edge(n1, n2, is_border=False)
        e2 = self.graph.add_edge(n2, n3, is_border=False)
        e3 = self.graph.add_edge(n3, n4, is_border=False)
        e4 = self.graph.add_edge(n4, n1, is_border=False)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.production.apply(self.graph, matched)

        self.assertEqual(e1.R, 1)
        self.assertEqual(e2.R, 1)
        self.assertEqual(e3.R, 1)
        self.assertEqual(e4.R, 1)

    def test_apply_does_not_damage_graph(self):
        """Test that applying P1 does not remove nodes/edges or change others."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)
        n5 = self.graph.add_node(2, 2)

        e1 = self.graph.add_edge(n1, n2)
        e2 = self.graph.add_edge(n2, n3)
        e3 = self.graph.add_edge(n3, n4)
        e4 = self.graph.add_edge(n4, n1)
        e5 = self.graph.add_edge(n3, n5)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        initial_nodes = set(self.graph.nodes)
        initial_edges = set(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.production.apply(self.graph, matched)

        final_nodes = set(self.graph.nodes)
        final_edges = set(self.graph.edges)

        self.assertEqual(initial_nodes, final_nodes)
        self.assertEqual(initial_edges, final_edges)
        
        self.assertEqual(e5.R, 0) 

if __name__ == '__main__':
    unittest.main()
