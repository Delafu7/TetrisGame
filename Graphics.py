
import pygame
import math
import time


pygame.init()
# Pantalla 600x900
screen_width = 600
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
# Establecer título de la ventana
pygame.display.set_caption("Tetris")

class GraphicsParty:
    @staticmethod
    def get_player_name(name=""):
        """
        Funcionalidad: Muestra un input para que el jugador escriba su nombre.
        Parámetros
            - name: Nombre del jugador, por defecto es una cadena vacía.
        Retorna:
            - None
        """
        #Tipo y tamaño de letra
        font = pygame.font.Font("other/PressStart2P.ttf", 16)
        # Tamaño del rectángulo del input
        box_width = 500
        box_height = 120
        screen_rect = screen.get_rect() # tamaño de la pantalla
        #Definir el rectángulo del input centrado en la pantalla
        input_rect = pygame.Rect(
            screen_rect.centerx - box_width // 2,
            screen_rect.centery - box_height // 2,
            box_width,
            box_height
        )
        # Dibuja fondo del input
        #pygame.SRCALPHA permite transparencia
        s = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
        s.fill((30, 30, 30, 220))
        screen.blit(s, input_rect.topleft)

        # Renderizar textos
        prompt = font.render("Game Over! Escribe tu nombre:", True, (255, 0, 0))
        name_render = font.render(name, True, (255, 255, 255))

        # Centrarlos dentro del rectángulo
        prompt_rect = prompt.get_rect(center=(input_rect.centerx, input_rect.top + 30))
        name_rect = name_render.get_rect(center=(input_rect.centerx, input_rect.top + 80))

        screen.blit(prompt, prompt_rect)
        screen.blit(name_render, name_rect)

        #Actualizar la pantalla y limitar FPS
        updateDisplay()

    def put_music():

        """Funcionalidad: Carga y reproduce música de fondo.
        Parámetros:
            - None
        Retorna:
            - None
        """

        # Música de fondo
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('other/Original_Tetris_theme.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Reproduce en bucle
        except Exception as e:
            print(f"Error al cargar música: {e}")

    def get_animated_rainbow_colors(length, speed=2.0):
        """
        Funcionalidad: Genera una lista de colores animados en un espectro arcoíris.
        Parámetros:
            - length: Número de colores a generar.
            - speed: Velocidad de la animación, por defecto es 2.0.
        Retorna:
            - Una lista de tuplas RGB representando los colores animados.
        """
        t = time.time() * speed
        colors = []
        for i in range(length):
            r = int(127 * math.sin(t + i) + 128)
            g = int(127 * math.sin(t + i + 2) + 128)
            b = int(127 * math.sin(t + i + 4) + 128)
            colors.append((r, g, b))
        return colors
    
    def render_multicolor_text(text, font, colors):
        """
        Funcionalidad: Renderiza un texto con colores animados.
        Parámetros:
            - text: El texto a renderizar.
            - font: Fuente para renderizar el texto.
            - colors: Lista de colores para cada carácter del texto.
        Retorna:
            - Una lista de superficies de texto renderizadas con los colores especificados.
        """
        surfaces = []
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            surf = font.render(char, True, color)
            surfaces.append(surf)
        return surfaces
    

class TetrisGraphics:
    def __init__(self, rows=20, cols=10, cell_size=30):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.board_width = cols * cell_size
        self.board_height = rows * cell_size
        self.offset_x = 20
        self.offset_y = (screen_height - self.board_height) // 2
        

        # --PARTE DE LA IMAGEN--
        self.celebration_frames = [
            pygame.image.load(f"imagens/russianDancer/frame_{i}.gif").convert_alpha() for i in range(29)  # Cargar 29 frames de la animación
        ]
        self.celebration_index = 0
        self.show_celebration = False
        self.celebration_timer = 0
        self.celebration_lines = 0
        self.celebration_duration = 1000  # duración en milisegundos

        
    def draw_board(self):
        """Funcionalidad: Dibuja el tablero de Tetris con una cuadrícula.
        Parámetros
            - self: Instancia de la clase TetrisGraphics.
        Retorna:
            - None
        """
        screen.fill((20, 20, 40))  # Color de fondo general

        # Dibujar el área del tablero como un bloque negro
        pygame.draw.rect(
            screen,
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
                screen, (50, 50, 50),
                (self.offset_x + x * self.cell_size, self.offset_y),
                (self.offset_x + x * self.cell_size, self.offset_y + self.board_height)
            )

        for y in range(self.rows + 1):
            pygame.draw.line(
                screen, (50, 50, 50),
                (self.offset_x, self.offset_y + y * self.cell_size),
                (self.offset_x + self.board_width, self.offset_y + y * self.cell_size)
            )
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
    
    def draw_ghost_piece(self, ghost_piece):
        """
        Funcionalidad: Dibuja la pieza fantasma en el tablero.
        Parámetros:
            - ghost_piece: Instancia de la pieza fantasma.
        Retorna:
            - None  
        """
        ghost_shape = ghost_piece.get_current_shape()
        for i, row in enumerate(ghost_shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(ghost_piece.x + j, ghost_piece.y + i)
                    pygame.draw.rect(screen, ghost_piece.color, (x, y, self.cell_size, self.cell_size), 1)
    
    def draw_board_pieces(self, board):
        """
        Funcionalidad: Dibuja las piezas fijas en el tablero.
        Parámetros:     
            - board: Lista de listas que representa el estado del tablero.
        Retorna:
            - None
        """
        # Piezas fijas en el tablero
        for y in range(self.rows):
            for x in range(self.cols):
                color = board[y][x]
                if color != (0, 0, 0):
                    screen_x, screen_y = self.to_screen_coords(x, y)
                    pygame.draw.rect(screen, color, (screen_x, screen_y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (255, 255, 255), (screen_x, screen_y, self.cell_size, self.cell_size), 2)

    def draw_current_piece(self, piece):
        """
        Funcionalidad: Dibuja la pieza actual en el tablero.
        Parámetros:
            - piece: Instancia de la pieza actual.
        Retorna:
            - None
        """
        # Pieza actual
        shape = piece.get_current_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x, y = self.to_screen_coords(piece.x + j, piece.y + i)
                    pygame.draw.rect(screen, piece.color, (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 2)

    def moving_animation(self, del_lines=0):
        """
        Funcionalidad: Muestra una animación de celebración al completar una línea.
        Parámetros:
            - del_lines: Número de líneas eliminadas, por defecto es 0.
        Retorna:
            - None
        """
        
     # === CONFIGURACIÓN DE POSICIONES ===
     
        right_margin = 20
        top_start_y = 60  
        container_width = 150

        # === BLOQUE DE ANIMACIÓN ===
        animation_container_height = 120
        animation_x = screen_width - container_width - right_margin
        animation_y = top_start_y
        animation_rect = pygame.Rect(animation_x, animation_y, container_width, animation_container_height)

        # Fondo y borde del recuadro de animación
        pygame.draw.rect(screen, (240, 240, 240), animation_rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), animation_rect, 3, border_radius=12)

        # Imagen de celebración
        frame_size = 100
        frame_x = animation_x + (container_width - frame_size) // 2
        frame_y = animation_y + 10

        # Animación
        current_time = pygame.time.get_ticks()
        if del_lines > 0:
                self.show_celebration = True
                self.celebration_timer = pygame.time.get_ticks()
                self.celebration_index = 0
                self.celebration_lines = del_lines
        if self.show_celebration:
            frame_duration = 150
            total_frames = len(self.celebration_frames) * 2
            elapsed = current_time - self.celebration_timer
            current_frame = elapsed // frame_duration
            if current_frame >= total_frames:
                self.show_celebration = False
                self.celebration_index = 0
                self.celebration_lines = 0
            else:
                self.celebration_index = current_frame % len(self.celebration_frames)

        frame = self.celebration_frames[self.celebration_index]
        scaled_frame = pygame.transform.scale(frame, (frame_size, frame_size))
        screen.blit(scaled_frame, (frame_x, frame_y))
    
    def my_punctuation(self, score):
        """
        Funcionalidad: Muestra la puntuación del jugador en la pantalla.
        Parámetros:
            - score: Puntuación del jugador.
        Retorna:
            - None
        """
        # === BLOQUE DE PUNTUACIÓN ===
        font_score = pygame.font.Font("other/PressStart2P.ttf", 14)

        # Crear texto multicolor
        padded_score = str(score).rjust(6, " ")
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

        score_box_x = screen_width - score_box_width - 20
        score_box_y = 60 + 120 + 20  

        score_box = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
        pygame.draw.rect(screen, (255, 255, 255), score_box, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), score_box, 2, border_radius=6)

        # Dibujar el texto multicolor centrado
        start_x = score_box.centerx - (text_width // 2)
        y = score_box.centery - (text_height // 2)
        for surf in score_text_parts:
            screen.blit(surf, (start_x, y))
            start_x += surf.get_width()

    def truncate_text(self,text, font, max_width):
        """Recorta el texto si no cabe en max_width y añade '...'."""
        if font.size(text)[0] <= max_width:
            return text[:3]
        while font.size(text + "...")[0] > max_width and len(text) > 0:
            text = text[:-1]
        return text + "..." 

    def show_top5(self, top_scores):
        """
        Funcionalidad: Muestra las 5 mejores puntuaciones en la pantalla.
        Parámetros:
            - top_scores: Lista de tuplas con los nombres y puntuaciones.
        Retorna:
            - None
        """
        font_top = pygame.font.Font("other/PressStart2P.ttf", 12)
        line_height = 22
        padding = 15

        # Recuadro para el top 5
        top_box_width =230
        top_box_height = (len(top_scores) + 2) * line_height + padding * 2
        top_box_x = screen_width - top_box_width - 30
        top_box_y = screen_height - top_box_height - 100

        top_box_rect = pygame.Rect(top_box_x, top_box_y, top_box_width, top_box_height)
        pygame.draw.rect(screen, (245, 245, 245), top_box_rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), top_box_rect, 3, border_radius=12)

         # Dibujar título centrado
        title_string = "TOP 5"
        rainbow_colors_title = GraphicsParty.get_animated_rainbow_colors(len(title_string))
        title_surfs = GraphicsParty.render_multicolor_text(title_string, font_top, rainbow_colors_title)

        # Calcular ancho total del título
        title_width = sum(surf.get_width() for surf in title_surfs)
        tx = top_box_x + (top_box_width - title_width) // 2
        ty = top_box_y + padding
        for surf in title_surfs:
            screen.blit(surf, (tx, ty))
            tx += surf.get_width()

        # Dibujar las puntuaciones alineadas a la derecha
        for i, score in enumerate(top_scores):
            name = score.split(',')[0]
            points = score.split(',')[1]

            # 🔹 ancho máximo disponible para el nombre
            max_name_width = top_box_width - 80  
            name = self.truncate_text(name, font_top, max_name_width)

            score_str = f"{i + 1}.- {name}: {points}"
            colors_line = GraphicsParty.get_animated_rainbow_colors(len(score_str))
            parts = GraphicsParty.render_multicolor_text(score_str, font_top, colors_line)

            x = top_box_x + padding
            y = top_box_y + padding + (i + 2) * line_height
            for surf in parts:
                screen.blit(surf, (x, y))
                x += surf.get_width()

    def show_next_piece(self, next_pieces, shapes):
        """
        Funcionalidad: Muestra las próximas piezas en la pantalla.
        Parámetros:
            - next_pieces: Lista de las próximas piezas.
            - shapes: Lista de formas de las piezas.
        Retorna:
            - None
        """
                
        next_piece_box_width = 120
        next_piece_box_height = 100
        
        gap_between_boxes = 30
        block_size = 20

        font_next = pygame.font.Font("other/PressStart2P.ttf", 12)
        label_text ="SIGUIENTES:"
        
        total_height = 2 * next_piece_box_height + gap_between_boxes + 30  # altura total con etiqueta
        start_y = (screen_height - total_height) // 2
        start_x = screen_width - next_piece_box_width - 60  # margen derecho

        rainbow_colors_next = GraphicsParty.get_animated_rainbow_colors(len(label_text))
        label_surfs = GraphicsParty.render_multicolor_text(label_text, font_next, rainbow_colors_next)

        x = start_x
        y = start_y
        for surf in label_surfs:
            screen.blit(surf, (x, y))
            x += surf.get_width()


        # Dibujar los dos bloques de las próximas piezas
        for i in range(2):
            if i >= len(next_pieces):
                break

            piece = next_pieces[i]
            shape = shapes[i]

            box_x = start_x + 20
            box_y = start_y + 40 + i * (next_piece_box_height + gap_between_boxes)
            pygame.draw.rect(screen, (240, 240, 240), (box_x, box_y, next_piece_box_width, next_piece_box_height), border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, next_piece_box_width, next_piece_box_height), 2, border_radius=6)

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
                        pygame.draw.rect(screen, piece.color, (rect_x, rect_y, block_size, block_size))
                        pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, block_size, block_size), 2)

    def show_my_best_score(self, my_best_score):
        """
        Funcionalidad: Muestra la mejor puntuación del jugador en la pantalla.
        Parámetros:
            - my_best_score: La mejor puntuación del jugador.
        Retorna:
            - None
        """
        font_best = pygame.font.Font("other/PressStart2P.ttf", 10)
        best_score_text = f"YOUR BEST: {my_best_score}"
        rainbow_colors_best = GraphicsParty.get_animated_rainbow_colors(len(best_score_text))
        best_score_parts = GraphicsParty.render_multicolor_text(best_score_text, font_best, rainbow_colors_best)

        # Calcular tamaño total del texto
        text_width = sum(surf.get_width() for surf in best_score_parts)
        text_height = max(surf.get_height() for surf in best_score_parts)

        # Recuadro
        score_box_padding_x = 10
        score_box_padding_y = 8
        score_box_width = text_width + 2 * score_box_padding_x
        score_box_height = text_height + 2 * score_box_padding_y

        score_box_x = screen_width - score_box_width - 20
        score_box_y = 130 + 120 + 20  

        score_box = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
        pygame.draw.rect(screen, (255, 255, 255), score_box, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), score_box, 2, border_radius=6)

        # Dibujar el texto multicolor centrado
        start_x = score_box.centerx - (text_width // 2)
        y = score_box.centery - (text_height // 2)
        for surf in best_score_parts:
            screen.blit(surf, (start_x, y))
            start_x += surf.get_width()
class InicialMenu:
    def __init__(self):
        """
        InicialMenu: Clase que maneja el menú inicial del juego.
        Atributos:
            - background: Fondo del menú.
            - base_y: Posición base para dibujar los modos de juego.
            - font: Fuente personalizada para los textos del menú.
            - selected: Índice del modo de juego seleccionado.
            - logo: Logo del juego.
            - modes: Lista de modos de juego disponibles.
        """
        self.background = None
        self.base_y = 0
        self.font = None
        self.selected = 0
        self.logo = None
        self.modes = ["Modo Clásico", "Modo Rápido", "Modo con Obstáculos"]

    def start_menu_static(self):
        """
        Funcionalidad: Inicializa el menúl, todo aquello que sea estático dentro del menú.
        Parámetros:
            - None
        Retorna:
            - None
        """
        # Fondo
        background = pygame.image.load("imagens/tetris_background.jpg").convert()
        self.background = pygame.transform.scale(background, screen.get_size())
        
        # Logo
        logo = pygame.image.load("imagens/tetris_logo.png").convert_alpha()
        logo_width = 400
        logo_height = int(logo.get_height() * (logo_width / logo.get_width()))
        self.logo = pygame.transform.scale(logo, (logo_width, logo_height))


        # Fuente personalizada
        self.font = pygame.font.Font("other/PressStart2P.ttf", 24)
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50)) # Dibujar logo centrado

        #Base para posicionar el contenido debajo del logo
        self.base_y = 50 + self.logo.get_height() + 50

    def show_modes(self):
        """
        Funcionalidad: Muestra los modos de juego disponibles en el menú.
        Parámetros:
            - None
        Retorna:
            - None
        """
        # Dibujar fondo y logo
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, (screen.get_width() // 2 - self.logo.get_width() // 2, 50))

        # Mostrar modos con fondo enmarcado
        for i, mode in enumerate(self.modes):
            #Mostrar modos 
            color = (255, 255, 255) if i == self.selected else (160, 160, 160)
            text = self.font.render(mode, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, self.base_y + i * 80))

            # Añadir fondo tipo botón
            padding_x, padding_y = 20, 10
            bg_rect = pygame.Rect(
                text_rect.left - padding_x,
                text_rect.top - padding_y,
                text_rect.width + 2 * padding_x,
                text_rect.height + 2 * padding_y
            )

            # Cambiar color de fondo si es el seleccionado
            bg_color = (80, 80, 80) if i == self.selected else (30, 30, 30)
            pygame.draw.rect(screen, bg_color, bg_rect, border_radius=10)

            # Dibujar borde si es el seleccionado
            if i == self.selected:
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2, border_radius=10)

            screen.blit(text, text_rect)
    
    def show_myBestScore(self, my_best_score):
        """
        Funcionalidad: Muestra la mejor puntuación del jugador en el menú.
        Parámetros:
            - my_best_score: La mejor puntuación del jugador.
        Retorna:
            - None
        """
        # Caja que contiene la mejor puntuación
        box_width = 500
        box_height = 40
        score_box = pygame.Rect(
            (screen.get_width() - box_width) // 2,
            self.base_y + len(self.modes) * 70 + 10,
            box_width,
            box_height
        )
        score_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 220))  # negro con 70% opacidad
        screen.blit(score_surface, score_box.topleft)

        # Mostrar mi mejor puntuación
        font = pygame.font.Font("other/PressStart2P.ttf", 18)
        score_text = f"Mi mejor puntuación: {my_best_score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, self.base_y + len(self.modes) * 80 ))
        screen.blit(text_surface, text_rect)
        
        

    def show_scores(self,top_scores):
        """
        Funcionalidad: Muestra las puntuaciones más altas en el menú.
        Parámetros:
            - top_scores: Lista de tuplas con los nombres y puntuaciones.
        Retorna:
            - None
        """
         #--MOSTRAR PUNTUACIONES--
        score_font = pygame.font.Font("other/PressStart2P.ttf", 18)

        # Crea fondo para puntuaciones
        num_scores = len(top_scores)
        box_width = 500
        box_height = 60 + num_scores * 30 

        score_box = pygame.Rect(
            (screen.get_width() - box_width) // 2,
            self.base_y + len(self.modes) * 100 - 20,
            box_width,
            box_height
        )
        score_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 180))  # negro con 70% opacidad
        screen.blit(score_surface, score_box.topleft)

        #Dibujar titulo de las puntuaciones
        score_title = score_font.render("TOP PUNTUACIONES", True, (255, 255, 255))
        score_title_rect = score_title.get_rect(center=(screen.get_width() // 2, self.base_y + len(self.modes) * 100))
        screen.blit(score_title, score_title_rect)



        #Dibujar puntuaciones
        for i, (name, score) in enumerate(top_scores):
            score_text = f"{i+1}. {name}: {score}"
            score_render = score_font.render(score_text, True, (255, 255, 255))
            score_rect = score_render.get_rect(center=(screen.get_width() // 2, score_title_rect.bottom + 30 + i * 30))
            screen.blit(score_render, score_rect)
        
    
    def getModes(self):
        """
        Funcionalidad: Devuelve una lista que contiene los indices de los modos.
        Parámetros:
            - None
        Retorna:
            - None
        """
        return [i for i in range(0,len(self.modes))]

def updateDisplay():
    """Funcionalidad: Actualiza la pantalla del juego.
    Parámetros:
        - None
    Retorna:
        - None
    """
    pygame.display.flip()

def getScreen():
    """
    Funcionalidad: Devuelve la pantalla del juego.
    Parámetros:
        - None
    Retorna:
        - screen: Pantalla del juego.
    """
    # Crear pantalla
    return screen
