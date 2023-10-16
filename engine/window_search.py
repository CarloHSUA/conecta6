import math
import time

# Constantes para representar los jugadores
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# Tamaño del tablero
ROWS = 19
COLUMNS = 19

# Ventana deslizante (sliding window) de amenazas
WINDOW_SIZE = 6

# Función para crear un tablero con X en el centro
def create_board():
    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    # Coloca una X en el centro del tablero
    board[ROWS // 2][COLUMNS // 2] = PLAYER_X
    return board

# Función para imprimir el tablero
def print_board(board):
    for row in board:
        row_str = " ".join(cell if cell != EMPTY else "-" for cell in row)
        print(row_str)
    print()

# Función para realizar un movimiento en el tablero
def make_move(board, player, row, column):
    board[row][column] = player

# Función para verificar si un movimiento es válido
def is_valid_move(board, row, column):
    return board[row][column] == EMPTY

# Función para verificar si un jugador ha ganado
def has_won(board, player):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                # Comprueba horizontal
                if col <= COLUMNS - WINDOW_SIZE:
                    if all(board[row][col + i] == player for i in range(WINDOW_SIZE)):
                        return True
                # Comprueba vertical
                if row <= ROWS - WINDOW_SIZE:
                    if all(board[row + i][col] == player for i in range(WINDOW_SIZE)):
                        return True
                # Comprueba diagonal de izquierda a derecha
                if col <= COLUMNS - WINDOW_SIZE and row <= ROWS - WINDOW_SIZE:
                    if all(board[row + i][col + i] == player for i in range(WINDOW_SIZE)):
                        return True
                # Comprueba diagonal de derecha a izquierda
                if col >= WINDOW_SIZE - 1 and row <= ROWS - WINDOW_SIZE:
                    if all(board[row + i][col - i] == player for i in range(WINDOW_SIZE)):
                        return True
    return False

# Función de heurística avanzada
def evaluate_advanced(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O

    player_score = 0
    opponent_score = 0

    # Implementa sliding window y defensive sliding window aquí
    # player_score += evaluate_sliding_window(board, player)
    # opponent_score += evaluate_defensive_sliding_window(board, player)
    
    # print("Player score: ", player_score)
    # print("Opponent score: ", opponent_score)
    # Implementa la búsqueda de patrones
    player_score += evaluate_patterns(board, player)
    # Implementa la puntuación de posiciones
    player_score += evaluate_positions(board, player) # -396
    opponent_score += evaluate_positions(board, opponent) 
    
    # Implementa threat space search aquí
    player_score += evaluate_threat_space(board, player)

    # Evalúa la presencia de amenazas que podrían convertirse en victorias en el próximo turno
    threats = threat_space_search(board, player)
    for threat in threats:
        row, col = threat
        if is_valid_move(board, row, col):
            board[row][col] = player
            if has_won(board, player):
                player_score += 100  # Valor alto para una amenaza que podría llevar a la victoria
            board[row][col] = EMPTY

    # Evalúa la presencia de amenazas del oponente
    opponent_threats = threat_space_search(board, opponent)
    for threat in opponent_threats:
        row, col = threat
        if is_valid_move(board, row, col):
            board[row][col] = opponent
            if has_won(board, opponent):
                opponent_score += 100  # Valor alto para una amenaza del oponente
            board[row][col] = EMPTY

    return player_score - opponent_score

def evaluate_positions(board,player):
    position_values = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    player_total_score = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                player_total_score += position_values[row][col]

    return player_total_score

def evaluate_patterns(board,player):
    if player == PLAYER_X:
        player_patterns = {
            "XXXXXX": 500,
            "-XXXX-": 100,
            "-XXX-": 50,
            "-XX-": 20,
            "-X-": 10,
            "OOOOOO": -500,
            "-OOOO-": -100,
            "-OOO-": -50,
            "-OO-": -20,
            "-O-": -10
        }
    else:
        player_patterns = {
            "XXXXXX": -500,
            "-XXXX-": -100,
            "-XXX-": -50,
            "-XX-": -20,
            "-X-": -10,
            "OOOOOO": 500,
            "-OOOO-": 100,
            "-OOO-": 50,
            "-OO-": 20,
            "-O-": 10
        }

    total_score = 0

    for i in range(ROWS):
        for j in range(ROWS):
            for pattern, weight in player_patterns.items():
                if j + len(pattern) <= ROWS:
                    row = "".join(board[i][j:j + len(pattern)])
                    if pattern == row:
                        total_score += weight

                if i + len(pattern) <= ROWS:
                    column = "".join(board[k][j] for k in range(i, i + len(pattern)))
                    if pattern == column:
                        total_score += weight

                if j + len(pattern) <= ROWS and i + len(pattern) <= ROWS:
                    diagonal1 = "".join(board[i + k][j + k] for k in range(len(pattern)))
                    if pattern == diagonal1:
                        total_score += weight

                if j - len(pattern) >= -1 and i + len(pattern) <= ROWS:
                    diagonal2 = "".join(board[i + k][j - k] for k in range(len(pattern)))
                    if pattern == diagonal2:
                        total_score += weight

    return total_score


# Función para evaluar las amenazas utilizando sliding window
def evaluate_sliding_window(board, player):
    player_score = 0
    window_size = 4  # Tamaño de la ventana

    for row in range(ROWS):
        for col in range(COLUMNS - window_size + 1):
            window = [board[row][col + i] for i in range(window_size)]
            if window.count(player) == window_size - 1 and window.count(EMPTY) == 1:
                player_score += 1

    for col in range(COLUMNS):
        for row in range(ROWS - window_size + 1):
            window = [board[row + i][col] for i in range(window_size)]
            if window.count(player) == window_size - 1 and window.count(EMPTY) == 1:
                player_score += 1

    return player_score

# Función para evaluar la defensa utilizando defensive sliding window
def evaluate_defensive_sliding_window(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_X
    opponent_score = 0
    window_size = 4  # Tamaño de la ventana

    for row in range(ROWS):
        for col in range(COLUMNS - window_size + 1):
            window = [board[row][col + i] for i in range(window_size)]
            if window.count(opponent) == window_size - 1 and window.count(EMPTY) == 1:
                opponent_score += 1

    for col in range(COLUMNS):
        for row in range(ROWS - window_size + 1):
            window = [board[row + i][col] for i in range(window_size)]
            if window.count(opponent) == window_size - 1 and window.count(EMPTY) == 1:
                opponent_score += 1

    return opponent_score

# Función para buscar amenazas en el tablero
def threat_space_search(board, player):
    threats = []

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                # Verificar amenazas horizontales
                if col <= COLUMNS - 4:
                    if board[row][col + 1:col + 4] == [player, player, player]:
                        if col + 4 < COLUMNS and board[row][col + 4] == EMPTY:
                            threats.append((row, col + 4))
                        if col - 1 >= 0 and board[row][col - 1] == EMPTY:
                            threats.append((row, col - 1))
                # Verificar amenazas verticales
                if row <= ROWS - 4:
                    if [board[row + i][col] for i in range(1, 4)] == [player, player, player]:
                        if row + 4 < ROWS and board[row + 4][col] == EMPTY:
                            threats.append((row + 4, col))
                        if row - 1 >= 0 and board[row - 1][col] == EMPTY:
                            threats.append((row - 1, col))
                # Verificar amenazas diagonales (izquierda a derecha)
                if col <= COLUMNS - 4 and row <= ROWS - 4:
                    if [board[row + i][col + i] for i in range(1, 4)] == [player, player, player]:
                        if row + 4 < ROWS and col + 4 < COLUMNS and board[row + 4][col + 4] == EMPTY:
                            threats.append((row + 4, col + 4))
                        if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == EMPTY:
                            threats.append((row - 1, col - 1))
                # Verificar amenazas diagonales (derecha a izquierda)
                if col >= 3 and row <= ROWS - 4:
                    if [board[row + i][col - i] for i in range(1, 4)] == [player, player, player]:
                        if row + 4 < ROWS and col - 4 >= 0 and board[row + 4][col - 4] == EMPTY:
                            threats.append((row + 4, col - 4))
                        if row - 1 >= 0 and col + 1 < COLUMNS and board[row - 1][col + 1] == EMPTY:
                            threats.append((row - 1, col + 1))

    return threats

# Función para evaluar el threat space
def evaluate_threat_space(board, player):
    threats = threat_space_search(board, player)

    return len(threats)  # Puedes ajustar la puntuación según la cantidad de amenazas

# Función para realizar la búsqueda en ventanas
def window_search(board, player, depth, alpha, beta, maximizing_player):
    if depth == 0 or has_won(board, PLAYER_X) or has_won(board, PLAYER_O):
        return evaluate_advanced(board, player)

    # Sustituir por la función de actions de comun.py
    valid_moves = [(row, col) for row in range(ROWS) for col in range(COLUMNS) if is_valid_move(board, row, col)]
    

    if maximizing_player:
        value = -math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = player
            value = max(value, window_search(board, PLAYER_X if player == PLAYER_O else PLAYER_X, depth - 1, alpha, beta, False))
            board[row][col] = EMPTY
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in valid_moves:
            row, col = move
            board[row][col] = player
            value = min(value, window_search(board, PLAYER_X if player == PLAYER_O else PLAYER_X, depth - 1, alpha, beta, True))
            board[row][col] = EMPTY
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

# Reducción del tablero original
def reduce_board(board, row, col, reduced_size, player, last_position:tuple):
    min_row = max(0, row - reduced_size // 2)
    max_row = min(len(board), row + reduced_size // 2 + 1)
    min_col = max(0, col - reduced_size // 2)
    max_col = min(len(board[0]), col + reduced_size // 2 + 1)

    reduced_board = [[board[r][c] for c in range(min_col, max_col)] for r in range(min_row, max_row)]

    return reduced_board, (row - min_row, col - min_col)

# Función para elegir el mejor movimiento con búsqueda de ventana
def choose_best_move(board, player, depth):
    best_move = None
    best_value = -math.inf
    # print(threat_space_search(board, "X"))
        
    valid_moves = [(row, col) for row in range(ROWS) for col in range(COLUMNS) if is_valid_move(board, row, col)]

    for move in valid_moves:
        row, col = move
        board[row][col] = player

        # Implementa la búsqueda en ventanas
        # if player == PLAYER_X:
        value = window_search(board, PLAYER_X if player == PLAYER_O else PLAYER_X, depth - 1, -math.inf, math.inf, False)
        # else:
            # value = window_search(board, PLAYER_O if player == PLAYER_X else PLAYER_O, depth - 1, -math.inf, math.inf, True)
       

        board[row][col] = EMPTY

        if value > best_value:
            best_value = value
            best_move = (row, col)
    
    return best_move

# Función principal del juego
def play_connect6():
    board = create_board()
    player = PLAYER_O  # El jugador (O) comienza los movimientos
    depth = 1  # Profundidad máxima de búsqueda
    time_limit_per_move = float('inf')  # No hay límite de tiempo

    print("Bienvenido al juego de Conecta6!")

    while True:
        print_board(board)

        for _ in range(2):  # Realiza dos movimientos en cada turno
            if player == PLAYER_O:
                while True:
                    try:
                        row = int(input("Ingresa la fila: "))
                        col = int(input("Ingresa la columna: "))
                    except ValueError:
                        print("Entrada no válida. Ingresa números enteros.")
                        continue
                    if not is_valid_move(board, row, col):
                        print("Movimiento no válido. La casilla ya está ocupada.")
                        continue
                    make_move(board, player, row, col)
                    break
                # row, col = choose_best_move(board, PLAYER_O, depth)
                # make_move(board, PLAYER_O, row, col)
            else:
                row, col = choose_best_move(board, PLAYER_X, depth)
                make_move(board, PLAYER_X, row, col)

        if has_won(board, player):
            print_board(board)
            print(f"¡El jugador {player} ha ganado!")
            break
        if all(all(cell != EMPTY for cell in row) for row in board):
            print_board(board)
            print("¡Es un empate!")
            break

        player = PLAYER_X if player == PLAYER_O else PLAYER_O

if __name__ == "__main__":
    play_connect6()
    # board = create_board()
    # print(reduce_board(board,19,19,13))
