class Piece:
    def __init__(self, type_, rotations, color):
        self.type = type_
        self.rotations = rotations
        self.rotation = 0
        self.color = color
        self.x = 4  # posición inicial en X (centro)
        self.y = 0  # posición inicial en Y (arriba)

    def get_current_shape(self):
        return self.rotations[self.rotation % len(self.rotations)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.rotations)