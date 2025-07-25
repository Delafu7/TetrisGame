import random
from Piece import Piece

#Define la formas de las piezas y sus rotaciones
TETROMINOS = {
    "S": [
        ['.....',
         '.....',
         '..00.',
         '.00..',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '...0.',
         '.....'],
        ['.....',
         '.....',
         '..00.',
         '.00..',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '...0.',
         '.....'],
    ],"S_REV": [
    ['.....',
     '.....',
     '.00..',
     '..00.',
     '.....'],
    ['.....',
     '..0..',
     '.00..',
     '.0...',
     '.....'],
    ['.....',
     '.....',
     '.00..',
     '..00.',
     '.....'],
    ['.....',
     '..0..',
     '.00..',
     '.0...',
     '.....'],
],
    "Z": [
        ['.....',
         '.....',
         '.00..',
         '..00.',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '.0...',
         '.....'],
        ['.....',
         '.....',
         '.00..',
         '..00.',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '.0...',
         '.....'],
    ],
    "I": [
        ['..0..',
         '..0..',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '0000.',
         '.....',
         '.....',
         '.....'],
        ['..0..',
         '..0..',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '0000.',
         '.....',
         '.....',
         '.....'],
    ],
    "O": [  # O no rota (todas las rotaciones son iguales)
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....'],
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....'],
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....'],
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....'],
    ],
    "J": [
        ['.....',
         '.0...',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..00.',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '...0.',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '.00..',
         '.....'],
    ],
    "L": [
        ['.....',
         '...0.',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '..00.',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '.0...',
         '.....'],
        ['.....',
         '.00..',
         '..0..',
         '..0..',
         '.....'],
    ],
    "T": [
        ['.....',
         '..0..',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '..0..',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '..0..',
         '.....'],
    ],
}

class BlockConstructor:
    def __init__(self):
        """
        tetrominos: contiene la forma de las piezas y sus rotaciones.
        """
        self.tetrominos = TETROMINOS

    def getRandomBlock(self):
        """
            Funcionalidad: Genera un bloque aleatorio con un color aleatorio.
            Parámetros:
                - None
            Retorna:
                - Piece
        """
        block_type = random.choice(list(self.tetrominos.keys()))
        rotations = self.tetrominos[block_type]
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        return Piece(block_type, rotations, color)
