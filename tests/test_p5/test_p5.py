import unittest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from hypergraph.hypergraph import HyperGraph
from productions.p5.p5 import P5

class TestP5(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P5()

    def test_can_apply_fully_broken_edges(self):
        """Test P5 applies when all 4 edges are broken (have midpoints)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1, 0)
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)
        m4 = self.graph.add_node(0, 1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply, "P5 should apply when midpoints exist")
        self.assertIsNotNone(matched)
        self.assertEqual(len(matched['edges']), 4, "Should find 4 midpoints")

    def test_cannot_apply_unmarked_hyperedge(self):
        """Test P5 does not apply if R=0."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1, 0)
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)
        m4 = self.graph.add_node(0, 1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 0 # Not marked

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_partial_broken_edges(self):
        """Test P5 does not apply if only some edges are broken."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1, 0)
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Should not apply if a midpoint is missing")

    def test_cannot_apply_wrong_coordinates(self):
        """Test P5 does not apply if 'midpoint' nodes are geometrically incorrect."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1.5, 0) 
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)
        m4 = self.graph.add_node(0, 1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply, "Should not apply if midpoint is not geometrically accurate")

    def test_in_larger_graph(self):
        """Test P5 applies correctly when embedded in typical mesh structures (shared edges)."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1, 0)
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)
        m4 = self.graph.add_node(0, 1)

        q1 = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q1.R = 1
        
        n5 = self.graph.add_node(4, 0)
        n6 = self.graph.add_node(4, 2)
        
        m5 = self.graph.add_node(3, 0)
        m6 = self.graph.add_node(4, 1)
        m7 = self.graph.add_node(3, 2)
        
        q2 = self.graph.add_hyperedge([n2, n5, n6, n3], label="Q")
        
        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertEqual(matched['hyperedge'], q1)


    def test_apply_splits_quadrilateral(self):
        """Test applying P5 correctly splits the quadrilateral."""
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(2, 0)
        n3 = self.graph.add_node(2, 2)
        n4 = self.graph.add_node(0, 2)

        m1 = self.graph.add_node(1, 0)
        m2 = self.graph.add_node(2, 1)
        m3 = self.graph.add_node(1, 2)
        m4 = self.graph.add_node(0, 1)

        q = self.graph.add_hyperedge([n1, n2, n3, n4], label="Q")
        q.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.production.apply(self.graph, matched)

        final_hyperedges = [e for e in self.graph.edges if e.is_hyperedge()]
        
        self.assertNotIn(q, final_hyperedges) 
        
        new_qs = [e for e in final_hyperedges if e.label == "Q"]
        self.assertEqual(len(new_qs), 4)

        center_node = None
        for node in self.graph.nodes:
            if abs(node.x - 1.0) < 1e-6 and abs(node.y - 1.0) < 1e-6:
                center_node = node
                break
        
        self.assertIsNotNone(center_node, "Center node should be created at (1,1)")
        
        for nq in new_qs:
            self.assertIn(center_node, nq.nodes)
            self.assertEqual(nq.R, 0, "New hyperedges should have R=0")


if __name__ == '__main__':
    unittest.main()
