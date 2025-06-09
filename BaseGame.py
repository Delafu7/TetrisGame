from BlockConstructor import BlockConstructor
import pygame

class TetrisGame:
    def __init__(self, screen):

        self.screen = screen
        self.board = [[(0, 0, 0)] * 10 for _ in range(20)]  # tablero de colores
        self.block_constructor = BlockConstructor()
        self.current_piece = None
        self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 1000
    def spawn_piece(self):
        # Logic to spawn a new Tetris piece

        self.current_piece = self.block_constructor.getRandomBlock()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            self.move_down()
            self.fall_time = current_time

    def draw(self):
        # Draw the current state of the game, such as the board and the current piece
        self.screen.fill((0, 0, 0))
        shape = self.current_piece.get_current_shape()

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = (self.current_piece.x + j) * 30
                    y = (self.current_piece.y + i) * 30
                    pygame.draw.rect(self.screen, self.current_piece.color, (x, y, 30, 30))
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 30, 30), 2) 
    def move_left(self):
        # Move the current piece left if possible
        if self.current_piece.x > 0:
            self.current_piece.x -= 1
        
    def move_right(self):
        # Move the current piece right if possible
        if self.current_piece.x  < 12:
            self.current_piece.x += 1
        
    def move_down(self): 
        # Move the current piece down if possible
        shape = self.current_piece.get_current_shape()
        if self.current_piece.y + len(shape) < 20:
            self.current_piece.y += 1
        else:
            # Here you would typically check for collisions and finalize the piece's position
            self.spawn_piece()

    def rotate(self):
        # Rotate the current piece if possible
        self.current_piece.rotate()
       