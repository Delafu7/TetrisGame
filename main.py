import pygame
from BaseGame import TetrisGame

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
    font = pygame.font.Font("PressStart2P.ttf", 24)
    logo_y = 50
    screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, logo_y))

    base_y = logo_y + logo.get_height() + 100

    while True:
        screen.blit(background, (0, 0))

        # Mostrar logo centrado
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50))

        # Mostrar modos
        for i, mode in enumerate(modes):
            color = (255, 255, 255) if i == selected else (160, 160, 160)
            text = font.render(mode, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, base_y +i * 60))
            screen.blit(text, text_rect)

        pygame.display.flip()

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


def pythonTetris():
    pygame.init()
    
    screen_width = 600
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")

    # Mostrar menú y obtener modo elegido
    selected_mode = show_start_menu(screen)

    game = TetrisGame(screen, mode=selected_mode)  # Asegúrate de que TetrisGame acepte el argumento `mode`

    # Música de fondo
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('Original_Tetris_theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error al cargar música: {e}")

    clock = pygame.time.Clock()
    running = True

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
                elif event.key == pygame.K_UP:
                    game.rotate()

        game.update()
        game.draw()
        pygame.display.flip()
        if game.game_over():
            print("Game Over")
            running = False
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    # Pantalla de inicio
    print("Bienvenido a Tetris!")
    print("Presiona cualquier tecla para comenzar...")
    # Ejecutar el juego de Tetris
    pythonTetris()
