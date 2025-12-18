import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from hypergraph.node import Node
from hypergraph.edge import Edge


class HyperGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, label="V"):
        node = Node(x, y, label)
        self.nodes.append(node)
        return node

    def add_edge(self, node_1, node_2, is_border=False, label="E"):
        edge = Edge([node_1, node_2], is_border, label)
        self.edges.append(edge)
        return edge

    def add_hyperedge(self, nodes, label="Q"):
        edge = Edge(nodes, label=label)
        self.edges.append(edge)
        return edge

    def get_edge_between(self, node_1, node_2):
        for edge in self.edges:
            if not edge.is_hyperedge() and \
               ((edge.nodes[0] == node_1 and edge.nodes[1] == node_2) or \
                (edge.nodes[0] == node_2 and edge.nodes[1] == node_1)):
                return edge
        return None

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def print(self):
        print("Nodes:")
        for node in self.nodes:
            print(f"  {node}")
        print("Edges:")
        for edge in self.edges:
            print(f"  {edge}")

    def visualize(self, filename=None):
        plt.figure(figsize=(10, 10))

        for edge in self.edges:
            if not edge.is_hyperedge():
                x_vals = [edge.nodes[0].x, edge.nodes[1].x]
                y_vals = [edge.nodes[0].y, edge.nodes[1].y]

                # Edge color: red for marked, black for rest
                if edge.R:
                    color = 'red'

                else:
                    color = 'black'

                plt.scatter(edge.x, edge.y, s=700, c='white', marker='s',
                            edgecolors='black', linewidths=1.5, zorder=14)

                label_text = f"{edge.label}\nR={edge.R}" if edge.R else edge.label
                plt.text(edge.x, edge.y, label_text, ha='center', va='center',
                         fontsize=12, fontweight='bold', zorder=15)

                # Edge is thicker if it's a border edge
                linewidth = 4 if edge.B else 2
                plt.plot(x_vals, y_vals, color=color, linewidth=linewidth, zorder=1)
            else:
                # Hyperedge color: bright red for marked (R=1), yellow for normal (R=0)
                hyperedge_color = 'red' if edge.R else 'yellow'

                plt.scatter(edge.x, edge.y, s=700, c=hyperedge_color, marker='s',
                            edgecolors='black', linewidths=2, zorder=14)

                # Add R value to label if marked
                label_text = f"{edge.label}\nR={edge.R}" if edge.R else edge.label
                plt.text(edge.x, edge.y, label_text, ha='center', va='center',
                         fontsize=12, fontweight='bold', zorder=15)

                # Connection lines to nodes
                connection_color = 'red' if edge.R else 'black'
                for node in edge.nodes:
                    plt.plot([edge.x, node.x], [edge.y, node.y],
                            color=connection_color, alpha=0.6,
                            linewidth=2, zorder=5)

        for node in self.nodes:
            color = 'lightblue'
            plt.scatter(node.x, node.y, s=600, c=color, edgecolors='black',
                        linewidths=2, zorder=9)
            plt.text(node.x, node.y, node.label, ha='center', va='center',
                     fontsize=10, fontweight='bold', zorder=10)

        plt.axis('equal')
        plt.grid(True, alpha=0.3)

        # Add legend
        legend_elements = [
            Patch(facecolor='black', edgecolor='black', label='Edge (R=0)'),
            Patch(facecolor='red', edgecolor='red', label='Edge (R=1)'),
            Patch(facecolor='lightblue', edgecolor='black', label='Node'),

        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

        plt.title('HyperGraph Visualization')

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')
        else:
            plt.show()

        plt.close()