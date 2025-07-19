
class Piece:
    def __init__(self, type_, rotations, color):
        """
        Funcionalidad: Inicializa una pieza de Tetris.
        Parámetros:
            - type_: Tipo de pieza (por ejemplo, 'I', 'O', 'T', etc.).
            - rotations: Lista de rotaciones posibles de la pieza.
            - color: Color de la pieza.
            - x: Posición x inicial de la pieza en el tablero.
            - y: Posición y inicial de la pieza en el tablero.
            - rotation: Índice de la rotación actual de la pieza.
        Retorna:
            - None
        """
        self.type = type_
        self.rotations = rotations
        self.rotation = 0
        self.color = color
        self.x = 3
        self.y = -self.get_top_offset()

    def get_top_offset(self):
        """
        Funcionalidad: Obtiene el desplazamiento superior de la pieza.
        Parámetros:
            - None
        Retorna:
            - El índice de la fila superior de la forma actual de la pieza.
        """
        shape = self.get_current_shape()
        for i, row in enumerate(shape):
            if '0' in row:
                return i
        return 0
    
    def get_current_shape(self):
        """
        Funcionalidad: Obtiene la forma actual de la pieza según su rotación.
        Parámetros:
            - None
        Retorna:
            - La forma actual de la pieza.
        """
        return self.rotations[self.rotation % len(self.rotations)]
    
    def rotate(self):
        """        
        Funcionalidad: Rota la pieza a la siguiente rotación.
        Parámetros:
            - None
        Retorna:
            - None
        """
        
        self.rotation = (self.rotation + 1) % len(self.rotations)

    def copy(self):
        """
        Funcionalidad: Crea una copia de la pieza actual.
        Parámetros:
            - None
        Retorna:
            - Una nueva instancia de la pieza con las mismas propiedades.
        """
        new_piece = Piece(self.type, self.rotations, self.color)
        new_piece.rotation = self.rotation
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece
