import pygame
from BaseGame import TetrisGame

def pythonTetris():
    pygame.init()
    
    screen_width = 600
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")

    game = TetrisGame(screen)

    # Música de fondo
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('Original_Tetris_theme.mp3')
        pygame.mixer.music.set_volume(0)  #Volume between 0.0 and 1.0
        pygame.mixer.music.play(-1)  # -1 para loop infinito
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

        clock.tick(10)  # Controla FPS, aquí 10 cuadros por segundo

    pygame.quit()

if __name__ == "__main__":
    pythonTetris()
