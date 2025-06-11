import copy

class Piece:
    def __init__(self, type_, rotations, color):
        self.type = type_
        self.rotations = rotations
        self.rotation = 0
        self.color = color
        self.x = 4
        self.y = 0

    def get_current_shape(self):
        return self.rotations[self.rotation % len(self.rotations)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.rotations)

    def copy(self):
        new_piece = Piece(self.type, self.rotations, self.color)
        new_piece.rotation = self.rotation
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece
