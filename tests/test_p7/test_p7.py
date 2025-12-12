import unittest
import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from hypergraph.hypergraph import HyperGraph
from productions import P7


class TestP7(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P7()

    def _create_pentagon(self, r_value=1, label="P"):
        nodes = []
        for i in range(5):
            angle = 2.0 * math.pi * i / 5.0
            x = math.cos(angle)
            y = math.sin(angle)
            nodes.append(self.graph.add_node(x, y))

        edges = []
        for i in range(5):
            n1 = nodes[i]
            n2 = nodes[(i + 1) % 5]
            e = self.graph.add_edge(n1, n2, is_border=True)
            edges.append(e)

        p = self.graph.add_hyperedge(nodes, label=label)
        p.R = r_value
        return nodes, edges, p

    def test_can_apply_correct_pentagon(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["hyperedge"], p)
        self.assertEqual(len(matched["nodes"]), 5)
        self.assertEqual(len(matched["edges"]), 5)

    def test_cannot_apply_missing_node(self):
        n1 = self.graph.add_node(0, 0)
        n2 = self.graph.add_node(1, 0)
        n3 = self.graph.add_node(1, 1)
        n4 = self.graph.add_node(0, 1)

        self.graph.add_edge(n1, n2, is_border=True)
        self.graph.add_edge(n2, n3, is_border=True)
        self.graph.add_edge(n3, n4, is_border=True)
        self.graph.add_edge(n4, n1, is_border=True)

        p = self.graph.add_hyperedge([n1, n2, n3, n4], label="P")
        p.R = 1

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_missing_edge(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")
        self.graph.remove_edge(edges[-1])  
        edges.pop()  

        p = self.graph.add_hyperedge(nodes, label="P")
        p.R = 1

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_wrong_label(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_not_marked_pentagon(self):
        nodes, edges, p = self._create_pentagon(r_value=0, label="P")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_apply_marks_all_edges(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")

        for e in edges:
            self.assertEqual(e.R, 0)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        for e in edges:
            self.assertEqual(e.R, 1)

        self.assertEqual(len(result["marked_edges"]), 5)

    def test_apply_preserves_graph_structure(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")

        extra_node = self.graph.add_node(2, 2)
        extra_edge = self.graph.add_edge(nodes[0], extra_node, is_border=False)

        initial_node_count = len(self.graph.nodes)
        initial_edge_count = len(self.graph.edges)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        self.production.apply(self.graph, matched)

        self.assertEqual(len(self.graph.nodes), initial_node_count)
        self.assertEqual(len(self.graph.edges), initial_edge_count)
        self.assertIn(extra_node, self.graph.nodes)
        self.assertIn(extra_edge, self.graph.edges)

    def test_visualization_before_after(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")

        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)

        before_path = os.path.join(output_dir, "test_p7_before.png")
        self.graph.visualize(before_path)
        self.assertTrue(os.path.exists(before_path))

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        after_path = os.path.join(output_dir, "test_p7_after.png")
        self.graph.visualize(after_path)
        self.assertTrue(os.path.exists(after_path))

    def test_in_larger_graph(self):
        nodes, edges, p = self._create_pentagon(r_value=1, label="P")

        n_extra1 = self.graph.add_node(3, 0)
        n_extra2 = self.graph.add_node(3, 1)
        self.graph.add_edge(n_extra1, n_extra2, is_border=True)
        self.graph.add_hyperedge([n_extra1, n_extra2, nodes[0], nodes[1], nodes[2]], label="P")

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)


if __name__ == "__main__":
    unittest.main(verbosity=2)
