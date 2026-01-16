class Node:
    def __init__(self, x, y, z=0, label="V"):
        self.x = x
        self.y = y
        self.z = z
        self.label = label

    def __str__(self):
        return (
            f"Node({self.x}, {self.y}, {self.z}, label={self.label})"
        )
