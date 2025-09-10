from BlockConstructor import BlockConstructor
import pygame
import random
import os

SCORES_FILE = "scores.txt"
class TetrisGame:
    def __init__(self):
        """
            cell_size -> Es el tamaño que tendrá cada celda del tablero
            cols -> El número de columnas del tablero
            rows -> El número de filas del tablero
            board -> Variable que contiene el tablero en cada celda se define el color negro (0, 0, 0)
            down_key_held -> Parte de la funcionalidad de mantener presionada la tecla hacia abajo
            down_key_start_time -> Tiempo de inicio de la tecla hacia abajo
            down_key_last_scored -> Último tiempo en el que se sumó un punto
            down_score_interval -> En cada intervalo de 50 ms sumamos 1 punto
            fall_time-> Controla el tiempo de caida
            score-> Es la puntuación de la partida
            block_constructor -> Inicializa el constructor de bloques
            

        """

        # Variables del tablero
        self.cell_size = 30
        self.cols = 10
        self.rows = 20
        self.board = [[(0, 0, 0)] * self.cols for _ in range(self.rows)]  # tablero de 20x10
    

        #Variables relacionadas con  el presionado del teclado
        self.down_key_held = False
        self.down_key_start_time= 0
        self.down_key_last_scored = 0
        self.down_score_interval = 50

        # Variables de funcionalidad
        self.fall_time = 0
        self.score=0

        # Inicialización de piezas
        self.block_constructor = BlockConstructor()
        self.spawn_piece()

        
        
        
    
        
    def set_mode(self, mode):
        """
        Funcionalidad: Establece el modo de juego.
        Parámetros:
            - mode: Modo de juego (0, 1 o 2).
        Retorna:
            - None 
        """
        if mode == 1:
            self.fall_speed = 500
        elif mode == 2:
            self.fall_speed = 1000
            self.add_initial_obstacles()
        else:
            self.fall_speed = 1000 

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
            return self.move_down()
        return 0

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
        delLines = 0
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            delLines=self.move_down()
            self.fall_time = current_time
        return delLines
    
    
    
    
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
        """
        Funcionalidad: Copia la pieza actual y la lleva hasta la parte inferior del tablero.
        Hasta lo máximo que pueda descender esa pieza  en el tablero.
        Parámetros:
            - None
        Retorna:
            - None
        """
        
        ghost_piece = self.current_piece.copy()
        while self.valid_move(ghost_piece.get_current_shape(),ghost_piece.x, ghost_piece.y + 1):
            ghost_piece.y += 1
        return ghost_piece
        

        

    
            
    def valid_move(self,shape,x, y):
        """        
        Funcionalidad: Verifica si la pieza puede moverse a una nueva posición (x, y) en el tablero.
        Parametros:
            - x (int): Nueva coordenada x.
            - y (int): Nueva coordenada y.
        Retorna:
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
            - None
        """
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
        line_points = 0
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

            

            # Actualizar la pieza actual
            self.spawn_piece()

        return line_points
            
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
    def reset(self):
        """
        Funcionalidad: Reinicia el estado del juego.
        Parámetros:
            - None
        Retorna:
            - None
        """
        self.board = [[(0, 0, 0)] * self.cols for _ in range(self.rows)]
        self.score = 0

class ConnectorTXT:
    def __init__(self, scores_file="scores.txt", myScores_file="myBestScore.txt"):
        """
        Funcionalidad: Inicializa la clase ConnectorTXT.
        Parámetros:
            - None
        Retorna:
            - None
        """
        self.scores_file = scores_file
        self.myScores_file = myScores_file
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
        
    def save_score(self, name, score):
        """
        Funcionalidad: Guarda la puntuación del jugador en el archivo SCORES_FILE.
        Parámetros:
            - name: El nombre del jugador.
            - score: La puntuación del jugador.
        Retorna:
            - None
        """
        scores = []
        
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        n, s = parts
                        scores.append((n, int(s)))

        # Añadir la nueva puntuación
        scores.append((name, score))

        # Ordenar de mayor a menor
        scores.sort(key=lambda x: x[1], reverse=True)

        # Escribir al archivo
        with open(self.scores_file, "w") as f:
            for n, s in scores[:10]:
                f.write(f"{n},{s}\n")

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

    def get_my_best_score(self):
        """
        Funcionalidad: Obtiene la mejor puntuación del jugador desde el archivo SCORES_FILE.
        Parámetros:
            - None
        Retorna:
            - La mejor puntuación del jugador o 0 si no hay puntuaciones.
        """
        try:
            with open(self.myScores_file, "r") as f:
                score = f.read().strip()
                self.bestScore=int(score) if score else 0
                return self.bestScore
        except FileNotFoundError:
            return 0
        
    def save_my_best_score(self, score):
        """
        Funcionalidad: Guarda la mejor puntuación del jugador en el archivo MY_SCORES_FILE.
        Parámetros:
            - score: La puntuación a guardar.
        Retorna:
            - None
        """
        print(f"Guardando puntuación: {self.bestScore}")
        with open(self.myScores_file, "w") as f:
            if self.bestScore < score:
                print(f"Nueva mejor puntuación: {self.get_my_best_score()} < {score}")
                # Solo guardar si la nueva puntuación es mejor
                f.write(f"{score}")
            else:
                f.write(f"{self.bestScore}")
