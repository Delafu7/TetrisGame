import pygame
from BaseGame import TetrisGame
from Graphics import *
from Graphics import updateDisplay
from Graphics import getScreen
from BaseGame import ConnectorTXT



###--VARIABLES GLOBALES--###
# Archivo de puntuaciones
SCORES_FILE = "scores.txt"
# Archivo de puntuaciones personales
MY_SCORES_FILE = "myBestScore.txt"
# Conexión a la base de datos de puntuaciones, en este caso un archivo de texto
connectorTxt= ConnectorTXT(SCORES_FILE, MY_SCORES_FILE)
# Crear la pantalla
screen = getScreen()
# Crear una instancia del juego Tetris
game = TetrisGame() 
# Crear una instancia de la clase TetrisGraphics que controla la parte visual del juego
graphics = TetrisGraphics(
            rows=game.rows,
            cols=game.cols,
            cell_size=game.cell_size
        )
def get_player_name():
    """
    Funcionalidad: Permite al jugador ingresar su nombre después de perder.
    Parámetros:
        - None
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
                sys.exit()
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
            - None
        Retorna:
            - None
    """
    #FPS
    clock = pygame.time.Clock()

    # Crear instancia de la clase InicialMenu
    menu = InicialMenu()
    menu.start_menu_static()
    myBestScore = connectorTxt.get_my_best_score()
    while True:
        
        #Mostrar el menú de inicio
        menu.show_modes()
        #Mostrar Puntuaciones
        top_scores = connectorTxt.get_sorted_scores()
        menu.show_scores(top_scores)
        #Actualizar pantalla
        menu.show_myBestScore(myBestScore)
        updateDisplay()
        # Dibujar el menú de selección de modo
        # Gestion de eventos
        modes = menu.getModes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Salida
                pygame.quit()
                sys.exit()
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
        Funcionalidad: Mueestra el menú de inicio y ejecuta el juego.
        Parámetros:
            - None
        Retorna:
            - None
    """
   

    while True:
        selected_mode = show_start_menu()
        if selected_mode !=0 and selected_mode != 1 and selected_mode != 2:
            print("Modo no reconocido, saliendo del juego.")
            # Esto no debería ocurrir, pero por si acaso
            break
        # selectrd_mode = 0 -> Modo Clásico
        # selected_mode = 1 -> Modo Rápido
        # selected_mode = 2 -> Modo con Obstáculos
        run_game(selected_mode)



def handle_down_key_hold():
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
            return game.handle_down_key_hold()
        else:
            game.down_key_held = False

        return 0
            
def run_game(mode=0):
    """
        Funcionalidad: Ejecuta el juego Tetris con el modo seleccionado.
        Parámetros:
            - screen: La pantalla donde se dibujará el juego.
            - mode: El modo de juego seleccionado (0, 1 o 2).
                    Por defecto es 0 (Modo Clásico).
        Retorna:
            - None
    """
    #Indicar el modo de juego  
    game.set_mode(mode)
   

    # Poner música de fondo
    GraphicsParty.put_music()

    # Control FPS
    clock = pygame.time.Clock()
    running = True
    rotation_allowed = True
    myBestScore = connectorTxt.get_my_best_score()

    # Permitir que la tecla de rotación se mantenga presionada
    # Esto permite que el jugador mantenga presionada la tecla de rotación para rotar la pieza continuamente
    # Esto es útil para evitar que el jugador tenga que presionar repetidamente la tecla de rotación
    # y hace que la jugabilidad sea más fluida.
    #200 ms de espera entre repeticiones, 100 ms de intervalo
    
    pygame.key.set_repeat(200, 100)
    while running:
        contDelRows = 0
        contDelRowsAux = 0
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
        contDelRows=game.update()
        contDelRowsAux=handle_down_key_hold()
        contDelRows += contDelRowsAux
        # Actualizar los visuales del juego
        ghost_piece=game.ghost_piece()
        aux_board = game.get_board_state()

        # Dibujar solo las partes del tablero
        graphics.draw_board()
        graphics.draw_ghost_piece(ghost_piece)
        graphics.draw_board_pieces(aux_board)
        graphics.draw_current_piece(game.current_piece)
        graphics.my_punctuation(game.score)
        graphics.show_my_best_score(myBestScore)
        graphics.moving_animation(contDelRows)
        
        # Bloque top 5 scores
        top_scores = connectorTxt.get_top_scores()
        graphics.show_top5(top_scores)

        # Bloque piezas siguientes
        shapes= [game.trim_shape(piece.get_current_shape()) for piece in game.next_pieces]
        graphics.show_next_piece(game.next_pieces, shapes)

        # Actualizar la pantalla
        updateDisplay()

        # Comprobar si el juego ha terminado
        if game.game_over():
            pygame.mixer.music.stop()
            name = get_player_name()
            if len(name)>0:
                connectorTxt.save_score(name, game.score)
            running = False
            connectorTxt.save_my_best_score(game.score)
            game.reset()
        # Controlar FPS
        clock.tick(10)

if __name__ == "__main__":
    # Pantalla de inicio del juego
    party() 
