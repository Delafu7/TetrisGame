from BlockConstructor import BlockConstructor
import pygame
import math
import time

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

        self.screen_width, self.screen_height = self.screen.get_size()
        self.offset_x = (self.screen_width - self.board_width) // 2  - 100
        self.offset_y = (self.screen_height - self.board_height) // 2
        
        self.celebration_frames = [
            pygame.image.load(f"imagens/russianDancer/frame_{i}.gif").convert_alpha() for i in range(29)  # Cargar 29 frames de la animación
        ]
        self.celebration_index = 0
        self.show_celebration = False
        self.celebration_timer = 0
        self.celebration_duration = 1000  # duración en milisegundos
    
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
    
    def get_animated_rainbow_colors(self, length, speed=2.0):
        t = time.time() * speed
        colors = []
        for i in range(length):
            r = int(127 * math.sin(t + i) + 128)
            g = int(127 * math.sin(t + i + 2) + 128)
            b = int(127 * math.sin(t + i + 4) + 128)
            colors.append((r, g, b))
        return colors
    def render_multicolor_text(self, text, font, colors):
        surfaces = []
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            surf = font.render(char, True, color)
            surfaces.append(surf)
        return surfaces
    def draw(self):
        self.screen.fill((20, 20, 40))  # Color de fondo general

        # Dibujar el área del tablero como un bloque negro
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),  # tablero negro
            (
                self.offset_x,
                self.offset_y,
                self.board_width,
                self.board_height
            )
        )


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

        # Posición fantasma
        ghost_piece = self.current_piece.copy()
        while self.valid_move(ghost_piece.get_current_shape(), ghost_piece.x, ghost_piece.y + 1):
            ghost_piece.y += 1

        ghost_shape = ghost_piece.get_current_shape()
        for i, row in enumerate(ghost_shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(ghost_piece.x + j, ghost_piece.y + i)
                    pygame.draw.rect(self.screen, ghost_piece.color, (x, y, self.cell_size, self.cell_size), 1)

        # Piezas fijas en el tablero
        for y in range(20):
            for x in range(10):
                color = self.board[y][x]
                if color != (0, 0, 0):
                    screen_x, screen_y = self.to_screen_coords(x, y)
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.screen, (255, 255, 255), (screen_x, screen_y, self.cell_size, self.cell_size), 2)

        # Pieza actual
        shape = self.current_piece.get_current_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(self.current_piece.x + j, self.current_piece.y + i)
                    pygame.draw.rect(self.screen, self.current_piece.color, (x, y, 30, 30))
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 30, 30), 2)

        
       
        current_time = pygame.time.get_ticks()
        if self.show_celebration:
            frame_duration = 150
            total_frames = len(self.celebration_frames) * 2
            elapsed = current_time - self.celebration_timer
            current_frame = elapsed // frame_duration
            if current_frame >= total_frames:
                self.show_celebration = False
                self.celebration_index = 0
            else:
                self.celebration_index = current_frame % len(self.celebration_frames)

        frame = self.celebration_frames[self.celebration_index]
        # Tamaño del recuadro contenedor (más alto para incluir imagen + puntuación)
        # === CONFIGURACIÓN DE POSICIONES ===
        right_margin = 20
        top_start_y = 60  # Más arriba
        container_width = 150

        # === BLOQUE DE ANIMACIÓN ===
        animation_container_height = 120
        animation_x = self.screen_width - container_width - right_margin
        animation_y = top_start_y
        animation_rect = pygame.Rect(animation_x, animation_y, container_width, animation_container_height)

        # Fondo y borde del recuadro de animación
        pygame.draw.rect(self.screen, (240, 240, 240), animation_rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), animation_rect, 3, border_radius=12)

        # Imagen de celebración
        frame_size = 100
        frame_x = animation_x + (container_width - frame_size) // 2
        frame_y = animation_y + 10

        # Animación
        current_time = pygame.time.get_ticks()
        if self.show_celebration:
            frame_duration = 150
            total_frames = len(self.celebration_frames) * 2
            elapsed = current_time - self.celebration_timer
            current_frame = elapsed // frame_duration
            if current_frame >= total_frames:
                self.show_celebration = False
                self.celebration_index = 0
            else:
                self.celebration_index = current_frame % len(self.celebration_frames)

        frame = self.celebration_frames[self.celebration_index]
        scaled_frame = pygame.transform.scale(frame, (frame_size, frame_size))
        self.screen.blit(scaled_frame, (frame_x, frame_y))

        # === BLOQUE DE PUNTUACIÓN ===
        font_score = pygame.font.Font("other/PressStart2P.ttf", 14)
        rainbow_colors = self.get_animated_rainbow_colors(20)

        # Crear texto multicolor
        padded_score = str(self.score).rjust(6, " ")
        score_string = f"PUNTOS: {padded_score}"
        rainbow_colors_score = self.get_animated_rainbow_colors(len(score_string))
        score_text_parts = self.render_multicolor_text(score_string, font_score, rainbow_colors_score)

        # Calcular tamaño total del texto
        text_width = sum(surf.get_width() for surf in score_text_parts)
        text_height = max(surf.get_height() for surf in score_text_parts)

        # Recuadro
        score_box_padding_x = 10
        score_box_padding_y = 8
        score_box_width = text_width + 2 * score_box_padding_x
        score_box_height = text_height + 2 * score_box_padding_y

        score_box_x = self.screen_width - score_box_width - 20
        score_box_y = animation_y + animation_container_height + 20  # Más arriba, pero con margen

        score_box = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
        pygame.draw.rect(self.screen, (255, 255, 255), score_box, border_radius=6)
        pygame.draw.rect(self.screen, (0, 0, 0), score_box, 2, border_radius=6)

        # Dibujar el texto multicolor centrado
        start_x = score_box.centerx - (text_width // 2)
        y = score_box.centery - (text_height // 2)
        for surf in score_text_parts:
            self.screen.blit(surf, (start_x, y))
            start_x += surf.get_width()

        # === BLOQUE TOP 5 ===
        top_scores = get_top_scores()
        font_top = pygame.font.Font("other/PressStart2P.ttf", 12)
        line_height = 20
        padding = 10

        # Recuadro para el top 5
        top_box_width = 180
        top_box_height = (len(top_scores) + 1) * line_height + padding * 2
        top_box_x = self.screen_width - top_box_width - 20
        top_box_y = self.screen_height - top_box_height - 20

        top_box_rect = pygame.Rect(top_box_x, top_box_y, top_box_width, top_box_height)
        pygame.draw.rect(self.screen, (245, 245, 245), top_box_rect, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), top_box_rect, 2, border_radius=10)

        # Dibujar título
        title_string = "TOP 5"
        rainbow_colors_title = self.get_animated_rainbow_colors(len(title_string))
        title_surfs = self.render_multicolor_text(title_string, font_top, rainbow_colors_title)
        tx = top_box_x + padding
        ty = top_box_y + padding
        for surf in title_surfs:
            self.screen.blit(surf, (tx, ty))
            tx += surf.get_width()

       # Dibujar las puntuaciones (solo una vez)
        for i, score in enumerate(top_scores):
            score_str = f"{i + 1}.- {score.split(',')[0]}: {score.split(',')[1]}"
            colors_line = self.get_animated_rainbow_colors(len(score_str))
            parts = self.render_multicolor_text(score_str, font_top, colors_line)
            x = top_box_x + padding
            y = top_box_y + padding + (i + 1) * line_height
            for surf in parts:
                self.screen.blit(surf, (x, y))
                x += surf.get_width()

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

            # Activar animación si se borró alguna línea
            if line_points > 0:
                self.show_celebration = True
                self.celebration_timer = pygame.time.get_ticks()
                self.celebration_index = 0
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

def get_top_scores(filename="scores.txt", count=5):
        SCORES_FILE = "scores.txt"
        try:
            with open(filename, "r") as f:
                scores = [line.strip() for line in f.readlines()]
            return sorted(scores, key=lambda x: int(x.split(",")[1]), reverse=True)[:count]
        except FileNotFoundError:
            return []