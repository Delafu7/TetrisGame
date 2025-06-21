from BlockConstructor import BlockConstructor
import pygame

class TetrisGame:
    def __init__(self, screen, mode=0):
        self.screen = screen
        self.board = [[(0, 0, 0)] * 10 for _ in range(20)]  # tablero de 20x10
        self.block_constructor = BlockConstructor()
        self.current_piece = None
        self.spawn_piece()
        self.down_key_held = False
        self.down_key_start_time = 0
        self.down_key_last_scored = 0
        self.down_score_interval = 50  # Cada 50 ms sumamos 1 punto
        self.fall_time = 0
        self.cell_size = 30
        self.cols = 10
        self.rows = 20
        self.score=0

        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size

        screen_width, screen_height = self.screen.get_size()
        self.offset_x = (screen_width - self.board_width) // 2
        self.offset_y = (screen_height - self.board_height) // 2
        if mode == 1:
            self.fall_speed = 500
        else:
            self.fall_speed = 1000
        if mode == 2:
            self.add_initial_obstacles()
    
    def handle_down_key_hold(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            now = pygame.time.get_ticks()
            if not self.down_key_held:
                self.down_key_held = True
                self.down_key_start_time = now
                self.down_key_last_scored = now
            else:
                # Agrega puntos por cada intervalo completado
                while now - self.down_key_last_scored >= self.down_score_interval:
                    self.score += 1
                    self.down_key_last_scored += self.down_score_interval

                # Hace que la pieza baje constantemente
                self.move_down()
        else:
            self.down_key_held = False

    def add_initial_obstacles(self):
        import random
        for _ in range(5):
            x = random.randint(0, 9)
            y = random.randint(15, 19)
            self.board[y][x] = (100, 100, 100)  # Color gris para los obstáculos
            
    def spawn_piece(self):
        self.current_piece = self.block_constructor.getRandomBlock()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            self.move_down()
            self.fall_time = current_time

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Dibujar la cuadrícula
        for x in range(self.cols + 1):
            pygame.draw.line(
                self.screen, (50, 50, 50),
                (self.offset_x + x * self.cell_size, self.offset_y),
                (self.offset_x + x * self.cell_size, self.offset_y + self.board_height)
            )

        for y in range(self.rows + 1):
            pygame.draw.line(
                self.screen, (50, 50, 50),
                (self.offset_x, self.offset_y + y * self.cell_size),
                (self.offset_x + self.board_width, self.offset_y + y * self.cell_size)
            )
        # Dibujar la posición fantasma
        ghost_piece = self.current_piece.copy()
        while self.valid_move(ghost_piece.get_current_shape(), ghost_piece.x, ghost_piece.y + 1):
            ghost_piece.y += 1


        ghost_shape = ghost_piece.get_current_shape()
        for i, row in enumerate(ghost_shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(ghost_piece.x + j, ghost_piece.y + i)
                    pygame.draw.rect(self.screen, ghost_piece.color, (x, y, self.cell_size, self.cell_size), 1)
        # Dibujar el tablero (piezas ya fijas)
        for y in range(20): 
            for x in range(10):
                color = self.board[y][x]
                if color != (0, 0, 0):
                    screen_x, screen_y = self.to_screen_coords(x, y)
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.screen, (255, 255, 255), (screen_x, screen_y, self.cell_size, self.cell_size), 2)

        # Dibujar la pieza actual
        shape = self.current_piece.get_current_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(self.current_piece.x + j, self.current_piece.y + i)
                    pygame.draw.rect(self.screen, self.current_piece.color, (x, y, 30, 30))
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 30, 30), 2)
        font = pygame.font.Font("other/PressStart2P.ttf", 20)
        score_text = font.render(f"PUNTOS: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.offset_x, self.offset_y - 40))
    def to_screen_coords(self, x, y):
        return self.offset_x + x * self.cell_size, self.offset_y + y * self.cell_size
    
            
        
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
        return len(rows_to_delete)
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
            line_points=self.deleteColumns()
            if line_points == 1:
                self.score += 40
            elif line_points == 2:
                self.score += 100
            elif line_points == 3:
                self.score += 300
            elif line_points == 4:
                self.score += 1200
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

