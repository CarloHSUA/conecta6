import math
import time
from copy import deepcopy
from rich import print
import random

# Constantes para representar los jugadores
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# Tamaño del tablero
ROWS = 19
COLUMNS = 19

# Ventana deslizante (sliding window) de amenazas
WINDOW_SIZE = 6
RANGE = 1

# PESOS
weights = []

all_positions = set()
last_postion = set() 

# Zobrist hashing
transposition_table = {}
hash_table = [[random.getrandbits(64) for _ in range(3)] for _ in range(ROWS * COLUMNS)]


# Función para crear un tablero con X en el centro
def create_board():
    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    # Coloca una X en el centro del tablero
    board[ROWS // 2][COLUMNS // 2] = PLAYER_X
    all_positions.add((ROWS // 2, COLUMNS // 2))
    return board

# Función para imprimir el tablero
def print_board(board):
    print("    0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18")
    for i, row in enumerate(board):
        if i <= 9:
            row_str = str(i) + " " + "  " + "  ".join(cell if cell != EMPTY else "-" for cell in row)
        else: 
            row_str = str(i) + "  " + "  ".join(cell if cell != EMPTY else "-" for cell in row)
        print(row_str)
    print()

def is_oponent_or_border(board, position: tuple, player):
    oponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    try:
        if board[position[0]][position[1]] == oponent or position[0] < 0 or position[1] < 0:
            return True
    except:
        return True
    return False

def actions(board, array_tuplas, rango, player):
    out_set = set()
    recorrido = rango * 2 + 1
    if(array_tuplas):
        for tupla in array_tuplas:
            i_inicial = tupla[0] - rango
            j_inicial = tupla[1] - rango
            
            for i in range(recorrido):
                for j in range(recorrido):
                    if(not is_oponent_or_border(board, (i + i_inicial, j + j_inicial), player) and board[i + i_inicial][j + j_inicial] != player):
                        out_set.add((i + i_inicial, j + j_inicial))
    return out_set

def result(board, action, player):
    if not (0 <= action[0] < ROWS and 0 <= action[1] < ROWS):
        raise Exception("Index out of bounds")
    copy_board = deepcopy(board)
    copy_board[action[0]][action[1]] = player
    return copy_board

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
def evaluate_advanced(board, position, player, all_actions, w_player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    
    player_score = 0
    opponent_score = 0
    a = 0
    val_tot = 0

    if has_won(board, player):
        return float('inf')
    elif has_won(board, opponent):
        return float('-inf')
    else:
        player_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player}# and (i,j) in all_actions}
        opponent_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == opponent}# and (i,j) in all_actions}
        # all_board = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player or val == opponent}
 
        for pos in player_positions:
            aux, amenazas, val = evaluate_star(board, pos, player, w_player)
            val_tot += val
            player_score += aux
            a += amenazas
        if a >= 19:
            print("AMENAZAS ", a, val_tot)
            print_board(board)
        player_score = player_score * (10**(12 * a))
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

def is_border(position: tuple):
    try:
        if not(0 <= position[0] < ROWS and 0 <= position[1] < COLUMNS):
            return True
    except:
        return True
    return False

def calcule_e_dir(board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces):
    if board[i][j] == '-':
        e_dir *= epsilon
        val -= 0.5
        my_places = True
    elif board[i][j] == player: # Turno de las X
        e_dir *=  w[next_pos-1]
        val = 0
        busy_places = True
    else:
        my_places = True
        if val > 0.:
            final_val += val

    if not busy_places:
        # Cuenta cuantos numeros hay de enemigos y espacios
        enemy_busy_places += 1
        if board[i][j] == '-':
            free_spaces += 1

    if not my_places:
        # Cuenta el numero de player que hay juntos. 
        my_busy_places += 1

    return e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces


def evaluate_star_v2(board, position, player):

    epsilon = 3 # Contante
    w = [1, 2, 3, 4, 5] # 2**10 == w_2**10
    w.reverse()
    propia = 1.1
    enem = 1
    vacio = 1

    busy_places = False 
    enemy_busy_places = 0

    my_places = False
    my_busy_places = 0
    e = 0
    e_dir = 1

    for dir in range(4):                    # Cuatro direcciones (0 = Horizontal, 1 = Diagonal Creciente,
        final_val = 0
        enemy_busy_places = 0
        my_busy_places = 0
        for l in range(2):                  # Dos lados, Ejemplo: (izquierdo, derecho) o (arriba, abajo)
            busy_places = False
            my_places = False
            val = 1  
            for next_pos in range(1,6):       # Por cada punto del lado
                if l == 0:                  # a
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] + next_pos

                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] - next_pos
                        j = position[1] + next_pos
                        
                    elif dir == 2:          # Vertical
                        i = position[0] - next_pos
                        j = position[1]
                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] - next_pos
                        j = position[1] - next_pos                   
                else:                       # b
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] - next_pos

                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] + next_pos
                        j = position[1] - next_pos

                    elif dir == 2:          # Vertical
                        i = position[0] + next_pos
                        j = position[1]
                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] + next_pos
                        j = position[1] + next_pos
                if is_border((i, j)):
                    break
                e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places = calcule_e_dir(board, i, j, epsilon, player, w, next_pos, propia, enem, vacio, e_dir, val, final_val, busy_places, enemy_busy_places, my_places, my_busy_places)
            e += e_dir

        if ((final_val >= 3) and enemy_busy_places >= 5):
            print(f"AAMENAZA A LA VISTA !!!!! ({position})")
        #  and total_busy_places >= 5
        e = e * 1000 if ((final_val >= 3) and enemy_busy_places >= 5) else e
        # if my_busy_places >= 4:
        #     print(f"INTENTO GANAR: {(position[0], position[1])} | SCORE: {e:.2f}")
        #     print_board(board)
        e = e * 15 if my_busy_places >= 4 else e
    # e = e if player == PLAYER_X else -e
    return e


def evaluate_star(board, position, player, w_player):
    # PESOS ----------------
    epsilon = w_player[0] # 3
    w = w_player[1:6] # [5, 4, 3, 2, 1]
    # w.reverse()
    final_val_weight = w_player[6] # 3
    enemy_busy_places_weight = w_player[7] # 5
    my_busy_places_weight = w_player[8] # 4
    e_opponent_weight = w_player[9] # 10**20
    e_win_weight = w_player[10] # 10**25
    val_weight = w_player[11] # 0.5
    # ----------------------

    amenaza = 0

    busy_places = False 
    enemy_busy_places = 0
    free_spaces = 0

    my_places = False
    my_busy_places = 0
    e = 0
    e_dir = 1

    for dir in range(4):                    # Cuatro direcciones (0 = Horizontal, 1 = Diagonal Creciente,
        final_val = 0
        enemy_busy_places = 0
        my_busy_places = 0
        free_spaces = 0
        for l in range(2):                  # Dos lados, Ejemplo: (izquierdo, derecho) o (arriba, abajo)
            busy_places = False
            my_places = False
            val = 1  
            for next_pos in range(1,6):       # Por cada punto del lado
                if l == 0:                  # a
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] + next_pos

                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] - next_pos
                        j = position[1] + next_pos
                        
                    elif dir == 2:          # Vertical
                        i = position[0] - next_pos
                        j = position[1]
                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] - next_pos
                        j = position[1] - next_pos                   
                else:                       # b
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] - next_pos

                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] + next_pos
                        j = position[1] - next_pos

                    elif dir == 2:          # Vertical
                        i = position[0] + next_pos
                        j = position[1]
                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] + next_pos
                        j = position[1] + next_pos
                if is_border((i, j)):
                    break
                e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces = calcule_e_dir(board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces)
            e += e_dir

        if final_val >= 3 and enemy_busy_places >= 5 and free_spaces > 0:
            amenaza += 1
        
        e = e * 1000 if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight) else e
        '''
        if my_busy_places >= 4:
            print(f"INTENTO GANAR: {(position[0], position[1])}")
            print_board(board)
        e = e * e_win_weight if my_busy_places >= my_busy_places_weight else e
        '''
    return e, amenaza, enemy_busy_places

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
                # Verifica patrones en filas hacia abajo
                if j + len(pattern) <= ROWS:
                    row = "".join(board[i][j:j + len(pattern)])
                    if pattern == row:
                        total_score += weight

                # Verifica patrones en filas hacia arriba
                if j - len(pattern) >= -1:
                    row = "".join(board[i][j:j - len(pattern):-1])
                    if pattern == row:
                        total_score += weight

                # Verifica patrones en columnas a la derecha
                if i + len(pattern) <= ROWS:
                    column = "".join(board[k][j] for k in range(i, i + len(pattern)))
                    if pattern == column:
                        total_score += weight

                # Verifica patrones en columnas a la izquierda
                if i - len(pattern) >= -1:
                    column = "".join(board[k][j] for k in range(i, i - len(pattern), -1))
                    if pattern == column:
                        total_score += weight

                # Verifica patrones en diagonal derecha hacia abajo izquierda
                if j + len(pattern) <= ROWS and i + len(pattern) <= ROWS:
                    diagonal = "".join(board[i + k][j + k] for k in range(len(pattern)))
                    if pattern == diagonal:
                        total_score += weight

                # Verifica patrones en diagonal izquierda hacia arriba derecha
                if j - len(pattern) >= -1 and i - len(pattern) >= -1:
                    diagonal = "".join(board[i - k][j - k] for k in range(len(pattern)))
                    if pattern == diagonal:
                        total_score += weight

                # Verifica patrones en diagonal izquierda superior a derecha abajo
                if j + len(pattern) <= ROWS and i - len(pattern) >= -1:
                    diagonal = "".join(board[i - k][j + k] for k in range(len(pattern)))
                    if pattern == diagonal:
                        total_score += weight

                # Verifica patrones en diagonal derecha abajo arriba izquierda
                if j - len(pattern) >= -1 and i + len(pattern) <= ROWS:
                    diagonal = "".join(board[i + k][j - k] for k in range(len(pattern)))
                    if pattern == diagonal:
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
def window_search(board, player, depth, alpha, beta, action, all_actions: set, w_player, count = 2, maximizing_player = True):
    if depth == 0 or has_won(board, PLAYER_X) or has_won(board, PLAYER_O):
        return evaluate_advanced(board, action, player, all_actions, w_player)
   
    valid_moves = actions(board, all_actions, RANGE, player)
    valid_moves_part_1, valid_moves_part_2 = tuples_divider(valid_moves)
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O

    if(len(valid_moves) == 0):
        return 0
    
    if maximizing_player:
        value = float('-inf')
        for move in valid_moves - valid_moves_part_1:
            valid_moves_2 = actions(result(board, move, player), all_actions.union({move}), RANGE, player)
            for move_2 in valid_moves_2 - valid_moves_part_2:
                new_actions = all_actions.union({move, move_2})
                
                value = max(value, window_search(result(result(board, move, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, w_player, count - 1, maximizing_player=False))
                new_actions = set()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
    else:
        value = float('inf')
        for move in valid_moves - valid_moves_part_1:
            valid_moves_2 = actions(result(board, move, player), all_actions.union({move}), RANGE, player)
            for move_2 in valid_moves_2 - valid_moves_part_2:
                new_actions = all_actions.union({move, move_2})
                value = min(value, window_search(result(result(board, move, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, w_player, count - 1, maximizing_player=True))
                new_actions = set()
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

def tuples_divider(conjunto_tuplas):
    # Calcular la mitad del conjunto
    mitad = len(conjunto_tuplas) // 2

    # Dividir el conjunto en dos partes
    parte_1 = set(list(conjunto_tuplas)[:mitad])
    parte_2 = conjunto_tuplas - parte_1
    return parte_1, parte_2

# Función para elegir el mejor movimiento con búsqueda de ventana
def choose_best_move(board, player, depth, count, w_player):
    best_move = (None, None)
    best_move_2 = (None, None)
    best_value = float('-inf')
    new_actions = set()

    # valid_moves = [(row, col) for row in range(ROWS) for col in range(COLUMNS) if is_valid_move(board, row, col)]
    # print(last_postion)
    valid_moves = actions(board, all_positions, RANGE, player)
    valid_moves_part_1, valid_moves_part_2 = tuples_divider(valid_moves)

    for move in valid_moves:# - valid_moves_part_1:
        # valid_moves_2 = actions(result(board, move, player), {move}, RANGE, player)
        valid_moves_2 = actions(result(board, move, player), all_positions.union({move}), RANGE, player)
        # new_actions = new_actions.union({move})
        for move_2 in valid_moves_2:# - valid_moves_part_2:
            
            new_actions = new_actions.union({move, move_2})
            value = window_search(result(result(board, move, player), move_2, player), player, depth - 1, float('-inf'), float('inf'), move_2, new_actions, w_player, count-1, maximizing_player=False)
            new_actions = set()
            if value > best_value:
                best_value = value
                best_move = move
                best_move_2 = move_2

    return best_move, best_move_2

# Función principal del juego
def play_connect6(w_player, w_opponent, autobot = True):
    best_player = None
    board = create_board()

    # board = [
    # ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', 'X', 'O', 'O', 'O', 'O', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', 'O', 'O', '-', '-', 'X', '-', 'X', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', 'X', 'O', 'O', 'O', 'X', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', 'O', 'X', 'X', 'X', 'O', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', 'X', 'O', 'X', 'X', 'X', 'X', 'O', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', 'X', 'X', 'O', 'X', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', 'O', 'X', '-', 'O', 'X', 'O', 'O', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', 'X', 'O', 'O', 'O', 'O', 'X', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', 'O', '-', 'O', 'O', 'X', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', 'X', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    # ]

    player = PLAYER_O  # El jugador (O) comienza los movimientos
    DEPTH = 1
    depth = DEPTH  # Profundidad máxima de búsqueda
    
    
    time_limit_per_move = float('inf')  # No hay límite de tiempo

    print("Bienvenido al juego de Conecta6!")

    while True:
        if not autobot:
            print(board)
            print_board(board)
        count = 1
        # for _ in range(2):  # Realiza dos movimientos en cada turno
        if player == PLAYER_O:
            if not autobot:
                last_postion.clear()
                for _ in range(2):
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
                        all_positions.add((row, col))
                        make_move(board, player, row, col)

                        last_postion.add((row, col))
                        break
            else:

                '''MAQUINA vs MAQUINA'''
                # row, col = choose_best_move(board, PLAYER_O, depth, count, w_player)
                # make_move(board, PLAYER_O, row, col)
                jugada1, jugada2 = choose_best_move(board, PLAYER_O, depth, count, w_player)
                all_positions.add((jugada1[0], jugada1[1]))
                all_positions.add((jugada2[0], jugada2[1]))
                make_move(board, PLAYER_O, jugada1[0], jugada1[1])
                make_move(board, PLAYER_O, jugada2[0], jugada2[1])
                
        else:
            jugada1, jugada2 =  choose_best_move(board, PLAYER_X, depth, count, w_opponent)
            if jugada1 == (None,None) and jugada2 == (None,None):
                print_board(board)
            else:
                count -= 1
                # depth -= 1
                all_positions.add((jugada1[0], jugada1[1]))
                all_positions.add((jugada2[0], jugada2[1]))
                # print('BEST MOVE', row, col)
                make_move(board, PLAYER_X, jugada1[0], jugada1[1])
                make_move(board, PLAYER_X, jugada2[0], jugada2[1])
                
                

        if has_won(board, player):
            print_board(board)
            print(f"¡El jugador {player} ha ganado!")
            best_player = player
            break
        if all(all(cell != EMPTY for cell in row) for row in board):
            print_board(board)
            print("¡Es un empate!")
            break

        player = PLAYER_X if player == PLAYER_O else PLAYER_O
    return best_player
if __name__ == "__main__":
    w = [
        3.1374458419275735,
        4.63272249656081,
        4.209165932010326,
        2.579898640103004,
        2.1884658375629815,
        0.9705097815393123,
        2.782633301831423,
        5.207137705286316,
        4.335041428787528,
        1e+20,
        1e+25,
        0.5
    ]

    w = [
        2.501007229057705,
        5.250728680254656,
        4.335441586615015,
        2.580488531839296,
        2.4510074261763246,
        1.3577760943926123,
        2.819126812634115,
        4.570608775518734,
        4.227608099209076,
        1e+20,
        1e+25,
        0.2740416905995666
    ]

    w = [3,                 # epsilon
     5, 4, 3, 2, 1,     # w
     3,                 # final_val_weight
     4,                 # enemy_busy_places_weight
     4,                 # my_busy_places_weight
     10**20,            # e_opponent_weight
     10**25,            # e_win_weight
     0.5                # val_weight
    ]

    play_connect6(w, w, autobot = False)
    # board = create_board()
    # print(reduce_board(board,19,19,13))
