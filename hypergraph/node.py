class Node:
    def __init__(self, x, y, z=0, is_hanging=False, label="V"):
        self.x = x
        self.y = y
        self.z = z
        self.is_hanging = is_hanging
        self.label = label

    def __str__(self):
        return (
            f"Node({self.x}, {self.y}, {self.z}, hanging={self.is_hanging}, label={self.label})"
        )
