import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from loops.initial_graph import create_initial_graph
from productions import P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12
import math

output_dir = "./loops/outputs"
os.makedirs(output_dir, exist_ok=True)

ITERATION = 0
TARGET_NODE = None  # Will be set to target refinement node

g = create_initial_graph()

print("Generating starting graph...")
g.visualize(os.path.join(output_dir, "starting-graph.png"))


def find_node_by_position(x, y, tolerance=0.1):
    """Find node at specific position with tolerance.
    
    Args:
        x, y: Coordinates to search for
        tolerance: Maximum distance from target coordinates
        
    Returns:
        Node at that position or None
    """
    for node in g.nodes:
        dist = math.sqrt((node.x - x)**2 + (node.y - y)**2)
        if dist <= tolerance:
            return node
    return None

def distance(node1, node2):
    """Calculate Euclidean distance between two nodes."""
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)


def get_closest_hyperedge_index(production, target_node):
    """Find index of hyperedge closest to target node that can be processed by production.
    
    Args:
        production: Production instance
        target_node: Node to find closest hyperedge to
        
    Returns:
        int: Index of closest hyperedge, or 0 if none found
    """
    if target_node is None:
        return 0
    
    candidates = []
    for edge in g.edges:
        if edge.is_hyperedge():
            try:
                can_apply, _ = production.can_apply(g, hyperedge=edge)
                if can_apply:
                    # Calculate distance from target to hyperedge center
                    dist = distance(target_node, edge)
                    candidates.append((edge, dist))
            except TypeError:
                # Production doesn't support hyperedge parameter
                return 0
    
    if not candidates:
        return 0
    
    # Sort by distance
    candidates.sort(key=lambda x: x[1])
    
    # Find index of closest hyperedge in the original edge list
    closest_edge = candidates[0][0]
    
    # Count which index this is among applicable hyperedges
    index = 0
    for edge in g.edges:
        if edge.is_hyperedge():
            try:
                can_apply, _ = production.can_apply(g, hyperedge=edge)
                if can_apply:
                    if edge == closest_edge:
                        return index
                    index += 1
            except TypeError:
                return 0
    
    return 0


def apply_n_draw(production, index=None):
    """Apply production once and save visualization.
    
    Args:
        production: Production instance
        index: Index of element to apply to. If None, uses closest to TARGET_NODE
    """
    global ITERATION
    
    # Auto-select index based on target node if not specified
    if index is None and TARGET_NODE is not None:
        index = get_closest_hyperedge_index(production, TARGET_NODE)
        print(f"  Auto-selected index {index} (closest to target node)")
    elif index is None:
        index = 0
    
    hyperedge = None
    
    # Find specific hyperedge by index
    candidates = []
    for edge in g.edges:
        if edge.is_hyperedge():
            # Try to check if this production would accept this edge
            try:
                can_apply, _ = production.can_apply(g, hyperedge=edge)
                if can_apply:
                    candidates.append(edge)
            except TypeError:
                # Production doesn't support hyperedge parameter
                # Just apply it normally without filtering
                break
    
    # Select by index if we have candidates
    if candidates and 0 <= index < len(candidates):
        hyperedge = candidates[index]
    
    # Apply production
    try:
        can_apply, matched = production.can_apply(g, hyperedge=hyperedge)
    except TypeError:
        # Production doesn't support hyperedge parameter
        can_apply, matched = production.can_apply(g)
    
    if can_apply:
        print(f"[{ITERATION}] Applying {production.name}...")
        production.apply(g, matched)
        g.visualize(os.path.join(output_dir, f"{ITERATION:02d}-{production.name}.png"))
        ITERATION += 1
        return True
    else:
        print(f"[{ITERATION}] Cannot apply {production.name}")
        return False

def apply_while(productions):
    """Apply productions repeatedly until none can be applied."""
    global ITERATION
    
    all_failed = True
    
    while True:
        for prod in productions:
            while True:
                can_apply, matched = prod.can_apply(g)
                if can_apply:
                    all_failed = False
                    print(f"[{ITERATION}] Applying {prod.name}...")
                    prod.apply(g, matched)
                    g.visualize(os.path.join(output_dir, f"{ITERATION:02d}-{prod.name}.png"))
                    ITERATION += 1
                else:
                    break
        
        if all_failed:
            break
        all_failed = True

# ============ Production Pipeline ============

TARGET_NODE = find_node_by_position(7.5, -6.5)  # Bottom-right corner node
if TARGET_NODE:
    print(f"\nTarget node set to: ({TARGET_NODE.x:.2f}, {TARGET_NODE.y:.2f})\n")
else:
    print("\nWarning: Target node not found, using default indexing\n")


prods_chain = [P10(), P4(), P3(), P11(), P1(), P4(), P2(), P3(), P5()]

apply_n_draw(P9())
apply_n_draw(P0())
apply_while(prods_chain)
apply_n_draw(P0())
apply_n_draw(P0())
apply_while(prods_chain)

print(f"\nGenerated {ITERATION} iterations in {output_dir}")
print("Done!")
