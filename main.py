import pygame
import os
from BaseGame import TetrisGame

SCORES_FILE = "scores.txt"

def get_player_name(screen, font):
    """
    Funcionalidad: Permite al jugador ingresar su nombre después de perder.
    Parámetros:
        - screen: La pantalla donde se mostrará el input.
        - font: Fuente para renderizar el texto.
    Retorna:
        - name: El nombre ingresado por el jugador.
    """

    name = ""
    clock = pygame.time.Clock() # Control de FPS
    input_active = True

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
    

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Si el usuario cierra la ventana, salir del juego
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Si el usuario presiona Enter, finalizar el input
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    # Elimina el último carácter del nombre
                    name = name[:-1]
                else:
                    # Agrega el carácter ingresado al nombre
                    # Verifica que el nombre no exceda los 10 caracteres y que sea imprimible
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode

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
        pygame.display.flip()
        clock.tick(30)
    
    return name


def load_scores():
    """ 
        Funcionalidad: Carga las puntuaciones desde el archivo SCORES_FILE.
        Parámetros:

        Retorna:
            - Si el archivo de SCORES_FILE, Una lista de listas con el formato [["Jugador", "1200"], ...]
            - Si el archivo no existe, retorna una lista vacía.
    """
    if not os.path.exists(SCORES_FILE):
        # El archivo no existe, retornar una lista vacía
        return []
    with open(SCORES_FILE, "r") as f:
        lines = f.readlines()
        return [line.strip().split(",") for line in lines] 
    
def save_score(name, score):
    """
        Funcionalidad: Guarda la puntuación del jugador en el archivo SCORES_FILE.
        Parámetros:
            - name: El nombre del jugador.
            - score: La puntuación del jugador.
        Retorna:
            - None
    """
    with open(SCORES_FILE, "a") as f:
        # Si no existe el archivo, se crea automáticamente
        #TODO Comprobar que no se repita el nombre
        f.write(f"{name},{score}\n")

def get_sorted_scores():
    """
        Funcionalidad: Obtiene las puntuaciones ordenadas desde el archivo SCORES_FILE.
        Parámetros:
            - None
        Retorna:
            - Una lista de las puntuaciones 5 puntuaciones más altas ordenadas de mayor a menor.
    """
    scores = load_scores()
    return sorted(scores, key=lambda x: int(x[1]), reverse=True)[:5]  # top 5

def show_start_menu(screen):
    """
        Funcionalidad: Muestra el menú de inicio del juego.
        Parámetros:
            - screen: La pantalla donde se mostrará el menú.
        Retorna:
            - El modo seleccionado por el jugador.
    """
    #FPS
    clock = pygame.time.Clock()

    selected = 0

    # Modos de juego
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
    screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50)) # Dibujar logo centrado

    #Base para posicionar el contenido debajo del logo
    base_y = logo.get_height() + 150

    while True:
        # Dibujar fondo y logo
        screen.blit(background, (0, 0))
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50))

        # Mostrar modos con fondo enmarcado
        for i, mode in enumerate(modes):
            #Mostrar modos 
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

            # Cambiar color de fondo si es el seleccionado
            bg_color = (80, 80, 80) if i == selected else (30, 30, 30)
            pygame.draw.rect(screen, bg_color, bg_rect, border_radius=10)

            # Dibujar borde si es el seleccionado
            if i == selected:
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2, border_radius=10)

            screen.blit(text, text_rect)

        #--MOSTRAR PUNTUACIONES--
        top_scores = get_sorted_scores()
        score_font = pygame.font.Font("other/PressStart2P.ttf", 18)

        # Crea fondo para puntuaciones
        num_scores = len(top_scores)
        box_width = 500
        box_height = 60 + num_scores * 30 

        score_box = pygame.Rect(
            (screen.get_width() - box_width) // 2,
            base_y + len(modes) * 100 - 20,
            box_width,
            box_height
        )
        score_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 180))  # negro con 70% opacidad
        screen.blit(score_surface, score_box.topleft)

        #Dibujar titulo de las puntuaciones
        score_title = score_font.render("TOP PUNTUACIONES", True, (255, 215, 0))
        score_title_rect = score_title.get_rect(center=(screen.get_width() // 2, base_y + len(modes) * 100))
        screen.blit(score_title, score_title_rect)

        #Dibujar puntuaciones
        for i, (name, score) in enumerate(top_scores):
            score_text = f"{i+1}. {name}: {score}"
            score_render = score_font.render(score_text, True, (255, 255, 255))
            score_rect = score_render.get_rect(center=(screen.get_width() // 2, score_title_rect.bottom + 10 + i * 30))
            screen.blit(score_render, score_rect)

        #Actualizar pantalla
        pygame.display.flip()

        # Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Salida
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Cambiar selección
                    selected = (selected - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    # Cambiar selección
                    selected = (selected + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    return modes[selected]

        clock.tick(30)


def party():
    """    
        Funcionalidad: Inicializa Pygame, muestra el menú de inicio y ejecuta el juego.
        Parámetros:

        Retorna:
            - None
    """
    # Inicializar Pygame
    pygame.init()

    # Pantalla 600x900
    screen_width = 600
    screen_height = 900
    # Crear pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Establecer título de la ventana
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
            # Esto no debería ocurrir, pero por si acaso
            break
        run_game(screen, selected_mode)


def run_game(screen,mode=0):
    """
        Funcionalidad: Ejecuta el juego Tetris con el modo seleccionado.
        Parámetros:
            - screen: La pantalla donde se dibujará el juego.
            - mode: El modo de juego seleccionado (0, 1 o 2).
                    Por defecto es 0 (Modo Clásico).
        Retorna:
            - None
    """
    # Mostrar menú y obtener modo elegido
    game = TetrisGame(screen, mode=mode)  

    # Música de fondo
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('other/Original_Tetris_theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Reproduce en bucle
    except Exception as e:
        print(f"Error al cargar música: {e}")

    # Control FPS
    clock = pygame.time.Clock()
    running = True
    rotation_allowed = True

    # Permitir que la tecla de rotación se mantenga presionada
    # Esto permite que el jugador mantenga presionada la tecla de rotación para rotar la pieza continuamente
    # Esto es útil para evitar que el jugador tenga que presionar repetidamente la tecla de rotación
    # y hace que la jugabilidad sea más fluida.
    #200 ms de espera entre repeticiones, 100 ms de intervalo
    pygame.key.set_repeat(200, 100)
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si el usuario cierra la ventana, salir del juego
                running = False
                pygame.mixer.music.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Mover pieza a la izquierda
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    # Mover pieza a la derecha
                    game.move_right()
                elif event.key == pygame.K_UP and rotation_allowed:
                    # Rotar pieza
                    game.rotate()
                    rotation_allowed = False  # bloquea rotaciones adicionales
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rotation_allowed = True  # permite rotar de nuevo
                
        # Manejar teclas de movimiento hacia abajo
        game.update()
        game.handle_down_key_hold()

        # Actualizar los visuales del juego
        game.draw()

        # Actualizar la pantalla
        pygame.display.flip()

        # Comprobar si el juego ha terminado
        if game.game_over():
            font = pygame.font.Font("other/PressStart2P.ttf", 16)
            name = get_player_name(screen, font)
            print("Game Over")
            if len(name)>0:
                save_score(name, game.score)
            running = False
            pygame.mixer.music.stop()
        # Controlar FPS
        clock.tick(10)

if __name__ == "__main__":
    # Pantalla de inicio del juego
    party() 
