from BlockConstructor import BlockConstructor
import pygame

class TetrisGame:
    def __init__(self, screen):
        self.screen = screen
        self.board = [[(0, 0, 0)] * 10 for _ in range(20)]  # tablero de 20x10
        self.block_constructor = BlockConstructor()
        self.current_piece = None
        self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 1000

    def spawn_piece(self):
        self.current_piece = self.block_constructor.getRandomBlock()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            self.move_down()
            self.fall_time = current_time

    def draw(self):
        self.screen.fill((0, 0, 0))

        for x in range(11):  # 10 columnas + 1 línea extra al final
            pygame.draw.line(self.screen, (50, 50, 50), (x * 30, 0), (x * 30, 20 * 30))
        for y in range(21):  # 20 filas + 1 línea extra al final
            pygame.draw.line(self.screen, (50, 50, 50), (0, y * 30), (10 * 30, y * 30))
        # Dibujar el tablero (piezas ya fijas)
        for y in range(20):
            for x in range(10):
                color = self.board[y][x]
                if color != (0, 0, 0):
                    pygame.draw.rect(self.screen, color, (x * 30, y * 30, 30, 30))
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * 30, y * 30, 30, 30), 2)

        # Dibujar la pieza actual
        shape = self.current_piece.get_current_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = (self.current_piece.x + j) * 30
                    y = (self.current_piece.y + i) * 30
                    pygame.draw.rect(self.screen, self.current_piece.color, (x, y, 30, 30))
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 30, 30), 2)
        
    def valid_move(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x] != (0, 0, 0):
                        return False
        return True

    def move_left(self):
        shape = self.current_piece.get_current_shape()
        if self.valid_move(shape, self.current_piece.x - 1, self.current_piece.y):
            self.current_piece.x -= 1

    def move_right(self):
        shape = self.current_piece.get_current_shape()
        if self.valid_move(shape, self.current_piece.x + 1, self.current_piece.y):
            self.current_piece.x += 1

    def deleteColumns(self):
        rows_to_delete = []
        for y in range(20):
            if all(self.board[y][x] != (0, 0, 0) for x in range(10)):
                rows_to_delete.append(y)
        for y in rows_to_delete:
            del self.board[y]
            self.board.insert(0, [(0, 0, 0)] * 10)
    def move_down(self):
        shape = self.current_piece.get_current_shape()
        if self.valid_move(shape, self.current_piece.x, self.current_piece.y + 1):
            self.current_piece.y += 1
        else:
            # Guardar pieza en el tablero
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == '0':
                        x = self.current_piece.x + j
                        y = self.current_piece.y + i
                        if 0 <= x < 10 and 0 <= y < 20:
                            self.board[y][x] = self.current_piece.color
            self.deleteColumns()
            self.spawn_piece()

    def rotate(self):

        #TODO rotate is not working properly
        # Intentar rotar, y solo hacerlo si es una posición válida
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece.get_current_shape(), self.current_piece.x, self.current_piece.y):
            # Si no es válida, deshacer la rotación
            self.current_piece.rotate()
            self.current_piece.rotate()
            self.current_piece.rotate()
    def game_over(self):
        return any(self.board[1][x] != (0, 0, 0) for x in range(10))

