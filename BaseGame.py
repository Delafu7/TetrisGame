from BlockConstructor import BlockConstructor
import pygame
import random
from Graphics import *
from Graphics import GraphicsParty
import os

SCORES_FILE = "scores.txt"
class TetrisGame:
    def __init__(self, screen, mode=0):
        self.cell_size = 30
        self.cols = 10
        self.rows = 20
        self.board = [[(0, 0, 0)] * self.cols for _ in range(self.rows)]  # tablero de 20x10
        self.block_constructor = BlockConstructor()
        self.down_key_held = False # Parte de la funcionalidad de mantener presionada la tecla hacia abajo
        self.down_key_start_time = 0 #Tiempo de inicio de la tecla hacia abajo
        self.down_key_last_scored = 0 #Último tiempo en el que se sumó un punto
        self.down_score_interval = 50  # Cada 50 ms sumamos 1 punto
        self.fall_time = 0
        self.score=0
        
        self.spawn_piece()

        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size

        self.screen_width, self.screen_height = self.screen.get_size()
        self.offset_x = (self.screen_width - self.board_width) // 2  - 100
        self.offset_y =(self.screen_height - self.board_height) // 2
        
        
    
        if mode == 1:
            self.fall_speed = 500
        else:
            self.fall_speed = 1000
        if mode == 2:
            self.add_initial_obstacles()
        
        self.graphics = TetrisGraphics(
            rows=self.rows,
            cols=self.cols,
            cell_size=self.cell_size
        )
        
    def handle_down_key_hold(self):
        """
        Funcionalidad: Maneja la lógica de mantener presionada la tecla hacia abajo.
        Permite que la pieza baje constantemente mientras la tecla está presionada,
        y otorga puntos por cada intervalo de tiempo transcurrido.
        Parámetros:
            - None
        Retorna:
            - None
        """
        # Verifica si la tecla hacia abajo está presionada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            # Si la tecla está presionada, actualiza el tiempo
            now = pygame.time.get_ticks()
            if not self.down_key_held:
                # Si la tecla no estaba presionada, inicia el conteo
                # y marca el tiempo de inicio y el último tiempo puntuado
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
        """
        Funcionalidad: Agrega obstáculos iniciales al tablero en el modo con obstáculos.
        Parámetros:
            - None
        Retorna:
            - None
        """
        for _ in range(5):
            x = random.randint(0, 9)
            y = random.randint(15, 19)
            self.board[y][x] = (100, 100, 100)  # Color gris para los obstáculos
            

    def spawn_piece(self):
        """        
        Funcionalidad: Genera una nueva pieza y la coloca en la parte superior del tablero.
        Parámetros:
            - None
        Retorna:
            - None
        """
        # Inicializar la cola si no existe
        if not hasattr(self, 'next_pieces') or self.next_pieces is None:
            self.next_pieces = [self.block_constructor.getRandomBlock() for _ in range(2)]

        # Tomar la siguiente pieza como la actual
        self.current_piece = self.next_pieces.pop(0)
       # Calcular el desplazamiento dinámico según las filas vacías arriba
        self.next_pieces.append(self.block_constructor.getRandomBlock())

    def update(self):
        """
        Funcionalidad: Actualiza el estado del juego, maneja eventos y dibuja el tablero.
        Parámetros:
            - None
        Retorna:
            - None
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            self.move_down()
            self.fall_time = current_time
    
    
    
    
    def trim_shape(self, shape):
        """ 
        Funcionalidad: Recorta el shape de la pieza para eliminar filas y columnas vacías.
        Parámetros:
            - shape: Lista de listas que representa el shape de la pieza.
        Retorna:
            - Una lista de listas recortada que representa el shape sin filas y columnas vacías.
        """
        # Elimina filas vacías
        trimmed_rows = [row for row in shape if any(cell == '0' for cell in row)]
        
        # Elimina columnas vacías
        if not trimmed_rows:
            return trimmed_rows
        
        # Transponer para analizar columnas como filas
        transposed = list(zip(*trimmed_rows))
        trimmed_columns = [col for col in transposed if any(cell == '0' for cell in col)]
        
        # Volver a transponer para obtener el shape recortado
        trimmed = list(zip(*trimmed_columns))
        
        return [list(row) for row in trimmed]

    def get_board_state(self):
        """
        Funcionalidad: Obtiene el estado actual del tablero.
        Parámetros:
            - None
        Retorna:
            - Una lista de listas que representa el estado actual del tablero.
        """
        return [row[:] for row in self.board]
    
    def ghost_piece(self):
        # Posición fantasma
        ghost_piece = self.current_piece.copy()
        while self.valid_move(ghost_piece.get_current_shape(),ghost_piece.x, ghost_piece.y + 1):
            ghost_piece.y += 1
        return ghost_piece
        

        
    def draw(self):

        ghost_piece=self.ghost_piece()
        aux_board = self.get_board_state()

        # Dibujar solo las partes del tablero
        self.graphics.draw_board()
        self.graphics.draw_ghost_piece(ghost_piece)
        self.graphics.draw_board_pieces(aux_board)
        self.graphics.draw_current_piece(self.current_piece)
        
    
       

        # === BLOQUE DE PUNTUACIÓN ===
        font_score = pygame.font.Font("other/PressStart2P.ttf", 14)

        # Crear texto multicolor
        padded_score = str(self.score).rjust(6, " ")
        score_string = f"PUNTOS: {padded_score}"
        rainbow_colors_score = GraphicsParty.get_animated_rainbow_colors(len(score_string))
        score_text_parts = GraphicsParty.render_multicolor_text(score_string, font_score, rainbow_colors_score)

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
        rainbow_colors_title = GraphicsParty.get_animated_rainbow_colors(len(title_string))
        title_surfs = GraphicsParty.render_multicolor_text(title_string, font_top, rainbow_colors_title)
        tx = top_box_x + padding
        ty = top_box_y + padding
        for surf in title_surfs:
            self.screen.blit(surf, (tx, ty))
            tx += surf.get_width()

       # Dibujar las puntuaciones (solo una vez)
        for i, score in enumerate(top_scores):
            score_str = f"{i + 1}.- {score.split(',')[0]}: {score.split(',')[1]}"
            colors_line = GraphicsParty.get_animated_rainbow_colors(len(score_str))
            parts = GraphicsParty.render_multicolor_text(score_str, font_top, colors_line)
            x = top_box_x + padding
            y = top_box_y + padding + (i + 1) * line_height
            for surf in parts:
                self.screen.blit(surf, (x, y))
                x += surf.get_width()

        # === BLOQUE SIGUIENTES PIEZAS (CENTRO DERECHA) ===
        next_piece_box_width = 120
        next_piece_box_height = 100
        box_padding = 8
        gap_between_boxes = 30
        block_size = 20

        font_next = pygame.font.Font("other/PressStart2P.ttf", 12)
        label_text ="SIGUIENTES:"
        
        total_height = 2 * next_piece_box_height + gap_between_boxes + 30  # altura total con etiqueta
        start_y = (self.screen_height - total_height) // 2
        start_x = self.screen_width - next_piece_box_width - 60  # margen derecho

        rainbow_colors_next = GraphicsParty.get_animated_rainbow_colors(len(label_text))
        label_surfs = GraphicsParty.render_multicolor_text(label_text, font_next, rainbow_colors_next)

        x = start_x
        y = start_y
        for surf in label_surfs:
            self.screen.blit(surf, (x, y))
            x += surf.get_width()


        # Dibujar los dos bloques de las próximas piezas
        for i in range(2):
            if i >= len(self.next_pieces):
                break

            piece = self.next_pieces[i]
            raw_shape = piece.get_current_shape()
            shape = self.trim_shape(raw_shape)

            box_x = start_x + 20
            box_y = start_y + 40 + i * (next_piece_box_height + gap_between_boxes)
            pygame.draw.rect(self.screen, (240, 240, 240), (box_x, box_y, next_piece_box_width, next_piece_box_height), border_radius=6)
            pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, next_piece_box_width, next_piece_box_height), 2, border_radius=6)

            # Centrar la pieza dentro del recuadro
            shape_width = len(shape[0]) * block_size
            shape_height = len(shape) * block_size
            offset_x = box_x + (next_piece_box_width - shape_width) // 2
            offset_y = box_y + (next_piece_box_height - shape_height) // 2

            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell == '0':
                        rect_x = offset_x + col_idx * block_size
                        rect_y = offset_y + row_idx * block_size
                        pygame.draw.rect(self.screen, piece.color, (rect_x, rect_y, block_size, block_size))
                        pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, block_size, block_size), 2)

    def to_screen_coords(self, x, y):
        """
        Funcionalidad: Convierte las coordenadas del tablero a coordenadas de pantalla.
        Parámetros:
            - x: Coordenada x en el tablero.
            - y: Coordenada y en el tablero.
        Retorna:
            - Una tupla (screen_x, screen_y) con las coordenadas en la pantalla.
        """
        return self.offset_x + x * self.cell_size, self.offset_y + y * self.cell_size
    
            
    def valid_move(self,shape,x, y):
        """        Verifica si la pieza puede moverse a una nueva posición (x, y) en el tablero.
        Args:
            x (int): Nueva coordenada x.
            y (int): Nueva coordenada y.
        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x] != (0, 0, 0):
                        return False
        return True


    def move_left(self):
        """
        Funcionalidad: Mueve la pieza actual hacia la izquierda si es un movimiento válido.
        Parámetros:
            - None 
        Retorna:
            - None"""
        if self.valid_move(self.current_piece.get_current_shape(),self.current_piece.x - 1, self.current_piece.y):
            self.current_piece.x -= 1

    def move_right(self):
        """
        Funcionalidad: Mueve la pieza actual hacia la derecha si es un movimiento válido.
        Parámetros:
            - None
        Retorna:
            - None
        """
        if self.valid_move( self.current_piece.get_current_shape(),self.current_piece.x + 1, self.current_piece.y):
            self.current_piece.x += 1


    def deleteColumns(self):
        """ 
        Funcionalidad: Elimina las filas completas del tablero y devuelve la cantidad de filas eliminadas.
        Parámetros:
            - None
        Retorna:
            - int: Número de filas eliminadas.
        """
        rows_to_delete = []
        for y in range(self.rows):
            if all(self.board[y][x] != (0, 0, 0) for x in range(self.cols)):
                rows_to_delete.append(y)
        for y in rows_to_delete:
            del self.board[y]
            self.board.insert(0, [(0, 0, 0)] * self.cols)  # Añadir una fila vacía al inicio del tablero
        return len(rows_to_delete)
    

    def move_down(self):
        """Funcionalidad: Mueve la pieza actual hacia abajo.
        Si la pieza no puede moverse hacia abajo, la guarda en el tablero y genera una nueva pieza.
        Parámetros:
            - None
        Retorna:
            - None
        """
        if self.valid_move(self.current_piece.get_current_shape(),self.current_piece.x,self.current_piece.y + 1):
            self.current_piece.y += 1
        else:
            # Guardar pieza en el tablero
            for i, row in enumerate(self.current_piece.get_current_shape()):
                for j, cell in enumerate(row):
                    if cell == '0':
                        # Calcular las coordenadas en el tablero
                        x = self.current_piece.x + j
                        y = self.current_piece.y + i
                        # Asegurarse de que las coordenadas estén dentro del tablero
                        if 0 <= x < self.cols and 0 <= y < self.rows:
                            self.board[y][x] = self.current_piece.color

            # Eliminar filas completas y actualizar la puntuación
            line_points = self.deleteColumns()

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

            # Actualizar la pieza actual
            self.spawn_piece()
            
    def rotate(self):
        """
        Funcionalidad: Rota la pieza actual en sentido horario.
        Parámetros:
            - None
        Retorna:
            - None
        """
        # Intentar rotar, y solo hacerlo si es una posición válida
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece.get_current_shape(),self.current_piece.x, self.current_piece.y):
            # Si no es válida, deshacer la rotación
            self.current_piece.rotate()
            self.current_piece.rotate()
            self.current_piece.rotate()
       
    def game_over(self):
        """
        Funcionalidad: Comprueba si el juego ha terminado.
        Parámetros:
            - None
        Retorna:
            - bool: True si el juego ha terminado, False en caso contrario.
        """
        return any(self.board[1][x] != (0, 0, 0) for x in range(10))


class ConnectorTXT:
    def __init__(self, scores_file="scores.txt"):
        """
        Funcionalidad: Inicializa la clase ConnectorTXT.
        Parámetros:
            - None
        Retorna:
            - None
        """
        self.scores_file = scores_file
    def load_scores(self):
        """ 
            Funcionalidad: Carga las puntuaciones desde el archivo SCORES_FILE.
            Parámetros:

            Retorna:
                - Si el archivo de SCORES_FILE, Una lista de listas con el formato [["Jugador", "1200"], ...]
                - Si el archivo no existe, retorna una lista vacía.
        """
        if not os.path.exists(self.scores_file):
            # El archivo no existe, retornar una lista vacía
            return []
        with open(self.scores_file, "r") as f:
            lines = f.readlines()
            return [line.strip().split(",") for line in lines] 
        
    def save_score(self,name, score):
        """
            Funcionalidad: Guarda la puntuación del jugador en el archivo SCORES_FILE.
            Parámetros:
                - name: El nombre del jugador.
                - score: La puntuación del jugador.
            Retorna:
                - None
        """
        with open(self.scores_file, "a") as f:
            # Si no existe el archivo, se crea automáticamente
            #TODO Comprobar que no se repita el nombre
            f.write(f"{name},{score}\n")

    def get_sorted_scores(self):
        """
            Funcionalidad: Obtiene las puntuaciones ordenadas desde el archivo SCORES_FILE.
            Parámetros:
                - None
            Retorna:
                - Una lista de las puntuaciones 5 puntuaciones más altas ordenadas de mayor a menor.
        """
        scores = self.load_scores()
        return sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]  # top 5

    def get_top_scores(self, count=5):
        """
        Funcionalidad: Obtiene las puntuaciones más altas desde un archivo.
        Parámetros:
            - filename: Nombre del archivo donde se guardan las puntuaciones.
            - count: Número de puntuaciones a retornar.
        Retorna:
            - Una lista de las puntuaciones más altas, cada una en formato "Jugador,Puntuación".
        """ 
        try:
            with open(self.scores_file, "r") as f:
                scores = [line.strip() for line in f.readlines()]
            return sorted(scores, key=lambda x: int(x.split(",")[1]), reverse=True)[:count]
        except FileNotFoundError:
            return []
