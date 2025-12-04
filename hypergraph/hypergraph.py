import matplotlib.pyplot as plt
from hypergraph.node import Node
from hypergraph.edge import Edge


class HyperGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, is_hanging=False, label="V"):
        node = Node(x, y, is_hanging, label)
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

                # Edge color: red for boundary, green for marked (R=1), black for normal
                if edge.is_border:
                    color = 'red'
                elif edge.R == 1:
                    color = 'green'
                else:
                    color = 'black'

                linewidth = 3 if edge.R == 1 else 2
                plt.plot(x_vals, y_vals, color=color, linewidth=linewidth, zorder=1)
            else:
                # Hyperedge color: bright red for marked (R=1), yellow for normal (R=0)
                hyperedge_color = '#FF3333' if edge.R == 1 else 'yellow'
                edge_color = 'red' if edge.R == 1 else 'black'
                linewidth = 3 if edge.R == 1 else 2

                plt.scatter(edge.x, edge.y, s=700, c=hyperedge_color, marker='s',
                            edgecolors=edge_color, linewidths=linewidth, zorder=14)

                # Add R value to label if marked
                label_text = f"{edge.label}\nR={edge.R}" if edge.R == 1 else edge.label
                plt.text(edge.x, edge.y, label_text, ha='center', va='center',
                         fontsize=12, fontweight='bold', zorder=15)

                # Connection lines to nodes
                connection_color = 'red' if edge.R == 1 else 'black'
                connection_alpha = 0.7 if edge.R == 1 else 0.5
                for node in edge.nodes:
                    plt.plot([edge.x, node.x], [edge.y, node.y],
                            color=connection_color, alpha=connection_alpha,
                            linewidth=linewidth-1, zorder=5)

        for node in self.nodes:
            color = 'orange' if node.is_hanging else 'lightblue'
            plt.scatter(node.x, node.y, s=600, c=color, edgecolors='black',
                        linewidths=2, zorder=9)
            plt.text(node.x, node.y, node.label, ha='center', va='center',
                     fontsize=10, fontweight='bold', zorder=10)

        plt.axis('equal')
        plt.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='yellow', edgecolor='black', label='Hyperedge (R=0)'),
            Patch(facecolor='#FF3333', edgecolor='red', label='Hyperedge (R=1) - Marked'),
            Patch(facecolor='lightblue', edgecolor='black', label='Node'),
            Patch(facecolor='orange', edgecolor='black', label='Hanging Node'),
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

        plt.title('HyperGraph Visualization')

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')
        else:
            plt.show()

        plt.close()
