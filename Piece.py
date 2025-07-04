import copy

class Piece:
    def __init__(self, type_, rotations, color):
        self.type = type_
        self.rotations = rotations
        self.rotation = 0
        self.color = color
        self.x = 3
        shape = self.get_current_shape()
        offset = self.count_empty_top_rows(shape)
        self.y = -self.get_top_offset()

    def get_top_offset(self):
        shape = self.get_current_shape()
        for i, row in enumerate(shape):
            if '0' in row:
                return i
        return 0
    
    def count_empty_top_rows(self, shape):
        count = 0
        for row in shape:
            if all(c != '0' for c in row):
                count += 1
            else:
                break  # se detiene en la primera fila con un bloque real
        return count
    
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
