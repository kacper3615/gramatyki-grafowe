class Node:
    def __init__(self, x, y, is_hanging=False, label="V"):
        self.x = x
        self.y = y
        self.is_hanging = is_hanging
        self.label = label

    def __str__(self):
        return (
            f"Node({self.x}, {self.y}, hanging={self.is_hanging}, label={self.label})"
        )
