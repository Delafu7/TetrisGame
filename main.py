import pygame
import os
from BaseGame import TetrisGame

SCORES_FILE = "scores.txt"

def get_player_name(screen, font):
    name = ""
    clock = pygame.time.Clock()
    input_active = True

    # Tamaño del rectángulo del input
    box_width = 500
    box_height = 120

    # Centrar el rectángulo en la pantalla
    screen_rect = screen.get_rect()
    input_rect = pygame.Rect(
        screen_rect.centerx - box_width // 2,
        screen_rect.centery - box_height // 2,
        box_width,
        box_height
    )
    bg_color = (30, 30, 30, 220)  # fondo con alpha para transparencia

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(name) > 0:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode

        # Dibuja fondo del input
        s = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
        s.fill(bg_color)
        screen.blit(s, input_rect.topleft)

        # Renderizar textos
        prompt = font.render("Game Over! Escribe tu nombre:", True, (255, 0, 0))
        name_render = font.render(name, True, (255, 255, 255))

        # Centrarlos dentro del rectángulo
        prompt_rect = prompt.get_rect(center=(input_rect.centerx, input_rect.top + 30))
        name_rect = name_render.get_rect(center=(input_rect.centerx, input_rect.top + 80))

        screen.blit(prompt, prompt_rect)
        screen.blit(name_render, name_rect)

        pygame.display.flip()
        clock.tick(30)

    return name


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        lines = f.readlines()
        return [line.strip().split(",") for line in lines]  # [["Jugador", "1200"], ...]

def save_score(name, score):
    with open(SCORES_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def get_sorted_scores():
    scores = load_scores()
    return sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]  # top 5

def show_start_menu(screen):
    clock = pygame.time.Clock()
    selected = 0
    modes = ["Modo Clásico", "Modo Rápido", "Modo con Obstáculos"]

    # Fondo
    background = pygame.image.load("imagens/tetris_background.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())
    

    # Logo
    logo = pygame.image.load("imagens/tetris_logo.png").convert_alpha()
    logo_width = 400
    logo_height = int(logo.get_height() * (logo_width / logo.get_width()))
    logo = pygame.transform.scale(logo, (logo_width, logo_height))

    # Fuente personalizada
    font = pygame.font.Font("other/PressStart2P.ttf", 24)
    logo_y = 50
    screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, logo_y))

    base_y = logo_y + logo.get_height() + 100

    while True:
        screen.blit(background, (0, 0))

        # Mostrar logo centrado
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50))

        # Mostrar modos con fondo enmarcado
        for i, mode in enumerate(modes):
            color = (255, 255, 255) if i == selected else (160, 160, 160)
            text = font.render(mode, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, base_y + i * 80))

            # Añadir fondo tipo botón
            padding_x, padding_y = 20, 10
            bg_rect = pygame.Rect(
                text_rect.left - padding_x,
                text_rect.top - padding_y,
                text_rect.width + 2 * padding_x,
                text_rect.height + 2 * padding_y
            )

            bg_color = (80, 80, 80) if i == selected else (30, 30, 30)
            pygame.draw.rect(screen, bg_color, bg_rect, border_radius=10)

            if i == selected:
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2, border_radius=10)

            screen.blit(text, text_rect)

        # Mostrar puntuaciones (¡mueve esto antes del flip!)
        top_scores = get_sorted_scores()
        score_font = pygame.font.Font("other/PressStart2P.ttf", 18)
        # Crea fondo para puntuaciones
        num_scores = len(top_scores)
        padding = 20
        box_width = 500
        box_height = 60 + num_scores * 30  # 1 línea para el título + N puntuaciones

        score_box = pygame.Rect(
            (screen.get_width() - box_width) // 2,
            base_y + len(modes) * 100 - 20,
            box_width,
            box_height
        )

        # Fondo con transparencia
        score_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 180))  # negro con 70% opacidad
        screen.blit(score_surface, score_box.topleft)
        score_title = score_font.render("TOP PUNTUACIONES", True, (255, 215, 0))
        score_title_rect = score_title.get_rect(center=(screen.get_width() // 2, base_y + len(modes) * 100))
        screen.blit(score_title, score_title_rect)

        for i, (name, score) in enumerate(top_scores):
            score_text = f"{i+1}. {name}: {score}"
            score_render = score_font.render(score_text, True, (255, 255, 255))
            score_rect = score_render.get_rect(center=(screen.get_width() // 2, score_title_rect.bottom + 10 + i * 30))
            screen.blit(score_render, score_rect)

        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    return modes[selected]

        clock.tick(30)


def party():
    pygame.init()
    screen_width = 600
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")
    while True:
        selected_mode = show_start_menu(screen)
        if selected_mode == "Modo Clásico":
            selected_mode = 0
        elif selected_mode == "Modo Rápido":
            selected_mode = 1
        elif selected_mode == "Modo con Obstáculos":
            selected_mode = 2
        else:
            print("Modo no reconocido, saliendo del juego.")
            break
        run_game(screen, selected_mode)


def run_game(screen,mode=0):    
    # Mostrar menú y obtener modo elegido
    
    game = TetrisGame(screen, mode=mode)  # Asegúrate de que TetrisGame acepte el argumento `mode`

    # Música de fondo
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('other/Original_Tetris_theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error al cargar música: {e}")

    clock = pygame.time.Clock()
    running = True
    rotation_allowed = True  # Variable para controlar las rotaciones
    pygame.key.set_repeat(200, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                elif event.key == pygame.K_UP and rotation_allowed:
                    game.rotate()
                    rotation_allowed = False  # bloquea rotaciones adicionales
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rotation_allowed = True  # permite rotar de nuevo
                

        game.update()
        game.draw()

        pygame.display.flip()
        if game.game_over():
            font = pygame.font.Font("other/PressStart2P.ttf", 16)
            name = get_player_name(screen, font)
            print("Game Over")
            save_score(name, game.score)
            running = False
        clock.tick(10)

    


if __name__ == "__main__":
    # Pantalla de inicio
    party() 
