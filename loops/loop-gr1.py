import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from loops.initial_graph import create_initial_graph
from productions import P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12

output_dir = "./loops/outputs"
os.makedirs(output_dir, exist_ok=True)

ITERATION = 0

g = create_initial_graph()

print("Generating starting graph...")
g.visualize(os.path.join(output_dir, "starting-graph.png"))


def apply_n_draw(production, index=0):
    """Apply production once and save visualization.
    
    Args:
        production: Production instance
        index: Index of element to apply to (0=first, 1=second, etc.)
    """
    global ITERATION
    
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

def mark_element_for_refinement(label="Q", index=0):
    """Mark a hyperedge for refinement (set R=1)."""
    global ITERATION
    
    count = 0
    for edge in g.edges:
        if edge.is_hyperedge() and edge.label == label:
            if count == index:
                edge.R = 1
                print(f"[{ITERATION}] Marked {label} hyperedge {index} for refinement (R=1)")
                g.visualize(os.path.join(output_dir, f"{ITERATION:02d}-mark-R1.png"))
                ITERATION += 1
                return True
            count += 1
    
    print(f"Could not find {label} hyperedge at index {index}")
    return False

# ============ Production Pipeline ============

apply_n_draw(P9(), index=1)
apply_n_draw(P0(), index=2)
apply_while([P10(), P4(), P3(), P11(), P1(), P4(), P2(), P3(), P5()])
apply_n_draw(P0(), index=6)

print(f"\nGenerated {ITERATION} iterations in {output_dir}")
print("Done!")
