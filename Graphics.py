
import pygame

# Pantalla 600x900
screen_width = 600
screen_height = 900
# Crear pantalla
screen = pygame.display.set_mode((screen_width, screen_height))

class GraphicsParty:
    @staticmethod
    def get_player_name(font, name=""):
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

class InicialMenu:
    def __init__(self):
        self.background = None
        self.base_y = 0
        self.font = None
        self.selected = 0
        self.logo = None
        self.modes = ["Modo Clásico", "Modo Rápido", "Modo con Obstáculos"]

    def start_menu_static(self):
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

    def show_scores(self,top_scores):
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
        score_title = score_font.render("TOP PUNTUACIONES", True, (255, 215, 0))
        score_title_rect = score_title.get_rect(center=(screen.get_width() // 2, self.base_y + len(self.modes) * 100))
        screen.blit(score_title, score_title_rect)

        #Dibujar puntuaciones
        for i, (name, score) in enumerate(top_scores):
            score_text = f"{i+1}. {name}: {score}"
            score_render = score_font.render(score_text, True, (255, 255, 255))
            score_rect = score_render.get_rect(center=(screen.get_width() // 2, score_title_rect.bottom + 10 + i * 30))
            screen.blit(score_render, score_rect)
    
    def getModes(self):
        return [i for i in range(0,len(self.modes))]

def updateDisplay():
    pygame.display.flip()