import matplotlib.pyplot as plt
from node import Node
from edge import Edge


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
                color = 'red' if edge.is_border else 'black'
                plt.plot(x_vals, y_vals, color=color, linewidth=2, zorder=1)
            else:
                plt.scatter(edge.x, edge.y, s=700, c='yellow', marker='s', 
                            edgecolors='black', linewidths=2, zorder=14)
                plt.text(edge.x, edge.y, edge.label, ha='center', va='center', 
                         fontsize=12, fontweight='bold', zorder=15)
                for node in edge.nodes:
                    plt.plot([edge.x, node.x], [edge.y, node.y], color='black', 
                             alpha=0.5, zorder=5)

        for node in self.nodes:
            color = 'orange' if node.is_hanging else 'lightblue'
            plt.scatter(node.x, node.y, s=600, c=color, edgecolors='black', 
                        linewidths=2, zorder=9)
            plt.text(node.x, node.y, node.label, ha='center', va='center', 
                     fontsize=10, fontweight='bold', zorder=10)
        
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        plt.title('HyperGraph Visualization')
        
        if filename:
            plt.savefig(filename)
        else:
            plt.show()
        
        plt.close()
