import unittest
import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from hypergraph.hypergraph import HyperGraph
from productions.p10.p10 import P10


class TestP10(unittest.TestCase):

    def setUp(self):
        self.graph = HyperGraph()
        self.production = P10()

    def _create_hexagon(self, r_value=1, label="S"):
        nodes = []
        for i in range(6):
            angle = 2.0 * math.pi * i / 6.0
            x = math.cos(angle)
            y = math.sin(angle)
            nodes.append(self.graph.add_node(x, y))

        edges = []
        for i in range(6):
            n1 = nodes[i]
            n2 = nodes[(i + 1) % 6]
            e = self.graph.add_edge(n1, n2, is_border=True)
            edges.append(e)

        hyperedge = self.graph.add_hyperedge(nodes, label=label)
        hyperedge.R = r_value
        return nodes, edges, hyperedge

    def test_can_apply_correct_hexagon(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertTrue(can_apply)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["hyperedge"], hyperedge)
        self.assertEqual(len(matched["nodes"]), 6)
        self.assertEqual(len(matched["edges"]), 6)

    def test_cannot_apply_not_marked_hexagon(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=0, label="S")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_wrong_label(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="Q")

        can_apply, matched = self.production.can_apply(self.graph)

        self.assertFalse(can_apply)
        self.assertIsNone(matched)

    def test_cannot_apply_too_few_nodes(self):
        nodes = [self.graph.add_node(i, i) for i in range(4)]
        for i in range(4):
            self.graph.add_edge(nodes[i], nodes[(i + 1) % 4])
        hyperedge = self.graph.add_hyperedge(nodes, label="S")
        hyperedge.R = 1

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)

    def test_cannot_apply_missing_edge(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")
        self.graph.remove_edge(edges[-1])  # remove one edge

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertFalse(can_apply)

    def test_cannot_apply_edges_already_marked(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")
        # Pre-mark all edges
        for e in edges:
            e.R = 1

        # Even though hyperedge R=1 and structure correct, we can still apply (idempotent)
        # But let's test that it still finds it (some implementations block re-application)
        # Here we allow re-application (as in original), so it should still be applicable
        can_apply, _ = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

    def test_apply_marks_all_edges(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")

        for e in edges:
            self.assertFalse(e.R)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)

        result = self.production.apply(self.graph, matched)

        for e in edges:
            self.assertTrue(e.R)

        self.assertEqual(len(result["marked_edges"]), 6)

    def test_apply_is_idempotent(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")
        self.production.apply(self.graph, self.production.can_apply(self.graph)[1])

        # Apply again
        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.production.apply(self.graph, matched)

        for e in edges:
            self.assertTrue(e.R)  # Still True, no error

    def test_apply_preserves_graph_structure(self):
        nodes, edges, hyperedge = self._create_hexagon(r_value=1, label="S")

        extra_node = self.graph.add_node(10, 10)
        extra_edge = self.graph.add_edge(nodes[0], extra_node)

        initial_nodes = len(self.graph.nodes)
        initial_edges = len(self.graph.edges)

        self.production.apply(self.graph, self.production.can_apply(self.graph)[1])

        self.assertEqual(len(self.graph.nodes), initial_nodes)
        self.assertEqual(len(self.graph.edges), initial_edges)
        self.assertIn(extra_node, self.graph.nodes)
        self.assertIn(extra_edge, self.graph.edges)

    def test_in_larger_graph(self):
        # Main hexagon to refine
        nodes1, edges1, h1 = self._create_hexagon(r_value=1, label="S")

        # Another hexagon not marked
        nodes2, _, h2 = self._create_hexagon(r_value=0, label="S")
        for n in nodes2:
            n.x += 3  # shift to avoid overlap
            n.y += 3

        # Extra unrelated stuff
        a = self.graph.add_node(5, 5)
        b = self.graph.add_node(6, 6)
        self.graph.add_edge(a, b)

        can_apply, matched = self.production.can_apply(self.graph)
        self.assertTrue(can_apply)
        self.assertEqual(matched["hyperedge"], h1)  # should find the marked one


if __name__ == "__main__":
    unittest.main(verbosity=2)
