import pygame
from BaseGame import TetrisGame
from Graphics import *
from Graphics import updateDisplay
from BaseGame import ConnectorTXT

SCORES_FILE = "scores.txt"
connectorTxt= ConnectorTXT(SCORES_FILE)
def get_player_name():
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

        # LLamada a la parte visual del juego
        GraphicsParty.get_player_name(name)
       
        clock.tick(30)
    
    return name




def show_start_menu():
    """
        Funcionalidad: Muestra el menú de inicio del juego.
        Parámetros:
            - screen: La pantalla donde se mostrará el menú.
        Retorna:
            - El modo seleccionado por el jugador.
    """
    #FPS
    clock = pygame.time.Clock()

    # Crear instancia de la clase InicialMenu
    menu = InicialMenu()
    menu.start_menu_static()
    while True:
        
        #--MOSTRAR MODOS DE JUEGO--#
        menu.show_modes()
        #--MOSTRAR PUNTUACIONES--
        top_scores = connectorTxt.get_sorted_scores()
        menu.show_scores(top_scores)
        #Actualizar pantalla

        updateDisplay()
        # Dibujar el menú de selección de modo
        # Gestion de eventos
        modes = menu.getModes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Salida
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Cambiar selección
                    menu.selected = (menu.selected - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    # Cambiar selección
                    menu.selected = (menu.selected + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    return modes[menu.selected]

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

    while True:
        selected_mode = show_start_menu()
        if selected_mode !=0 and selected_mode != 1 and selected_mode != 2:
            print("Modo no reconocido, saliendo del juego.")
            # Esto no debería ocurrir, pero por si acaso
            break
        # selectrd_mode = 0 -> Modo Clásico
        # selected_mode = 1 -> Modo Rápido
        # selected_mode = 2 -> Modo con Obstáculos
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

    # Poner música de fondo
    GraphicsParty.put_music()

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
        updateDisplay()

        # Comprobar si el juego ha terminado
        if game.game_over():
            pygame.mixer.music.stop()
            name = get_player_name()
            if len(name)>0:
                connectorTxt.save_score(name, game.score)
            running = False
        # Controlar FPS
        clock.tick(10)

if __name__ == "__main__":
    # Pantalla de inicio del juego
    party() 
