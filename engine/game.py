import math
import time
from copy import deepcopy
from rich import print
import random
import matplotlib.pyplot as plt


class Game():
    def __init__(self, depth, weights, size = (19, 19), time_limit = 10, have_border = False, border = None, empty = "-", player = "X", opponent = "O") -> None:
        # Constantes para representar los jugadores
        self.empty = empty
        self.player = player
        self.opponent = opponent
        self.border = border
        self.have_border = have_border

        self.board = [[]]
        self.DEPTH = depth

        # Tamaño del tablero
        self.ROWS = size[0]
        self.COLUMNS = size[1]
        # Ventana deslizante (sliding window) de amenazas
        self.WINDOW_SIZE = 6
        self.RANGE = 1
        self.best_n_moves = 20
        # PESOS
        self.weights = weights
        self.all_positions = set()
        self.last_postion = set()
        

        # TIMER
        self.TIME_LIMIT = time_limit

        # GRAFICAS
        self.rounds = []
        self.time_per_round = []
        self.count_nodes = 0
        self.nodes_evaluated = []

        self.hash_table = [[random.getrandbits(64) for _ in range(4)] for _ in range(size[0] * size[1])]
        self.transposition_table = {}

    def set_board(self, board):
        self.board = board
    
    def set_depth(self, new_depth):
        self.DEPTH = new_depth

    def set_player_and_opponent(self, new_player, new_opponent):
        self.player = new_player
        self.opponent = new_opponent

    def set_weights(self, new_weights):
        self.weights = new_weights

    # Función para crear un tablero con X en el centro
    def create_board(self):
        board = [[self.empty for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        if self.have_border:
            # Establecer el borde superior e inferior
            for col in range(self.COLUMNS):
                board[0][col] = self.border
                board[self.ROWS - 1][col] = self.border
            
            # Establecer el borde izquierdo y derecho (excluyendo las esquinas que ya se han establecido)
            for row in range(1, self.ROWS - 1):
                board[row][0] = self.border
                board[row][self.COLUMNS - 1] = self.border

        # # Coloca una X en el centro del tablero
        # board[self.ROWS // 2][self.COLUMNS // 2] = self.player
        # self.all_positions.add((self.ROWS // 2, self.COLUMNS // 2))
        return board

    # Función para imprimir el tablero
    def print_board(self, board):
        print("    0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18")
        for i, row in enumerate(board):
            if i <= 9:
                row_str = str(i) + " " + "  " + "  ".join(str(cell) if str(cell) != str(self.empty) else str(self.empty) for cell in row)
            else: 
                row_str = str(i) + "  " + "  ".join(str(cell) if str(cell) != str(self.empty) else str(self.empty) for cell in row)
            print(row_str)
        print()

    def is_oponent_or_border(self, board, position: tuple, player):
        oponent = self.player if player == self.opponent else self.opponent
        try:
            if self.have_border:
                if board[position[0]][position[1]] == oponent or position[0] <= 0 or position[1] <= 0:
                    return True
            else:
                if board[position[0]][position[1]] == oponent or position[0] < 0 or position[1] < 0:
                    return True
        except:
            return True
        return False

    def actions(self, board, array_tuplas, rango, player):
        out_set = set()
        recorrido = rango * 2 + 1
        if(array_tuplas):
            for tupla in array_tuplas:
                i_inicial = tupla[0] - rango
                j_inicial = tupla[1] - rango
                
                for i in range(recorrido):
                    for j in range(recorrido):
                        if(not self.is_oponent_or_border(board, (i + i_inicial, j + j_inicial), player) and board[i + i_inicial][j + j_inicial] != player):
                            out_set.add((i + i_inicial, j + j_inicial))
        return out_set

    def result(self, board, action, player):
        if not (0 <= action[0] < self.ROWS and 0 <= action[1] < self.ROWS):
            raise Exception("Index out of bounds")
        copy_board = deepcopy(board)
        copy_board[action[0]][action[1]] = player
        return copy_board

    # Función para realizar un movimiento en el tablero
    def make_move(self, board, player, row, column):
        board[row][column] = player

    # Función para verificar si un movimiento es válido
    def is_valid_move(self,board, row, column):
        return board[row][column] == self.empty

    # Función para verificar si un jugador ha ganado
    def has_won(self,board, player):
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                if board[row][col] == player:
                    # Comprueba horizontal
                    if col <= self.COLUMNS - self.WINDOW_SIZE:
                        if all(board[row][col + i] == player for i in range(self.WINDOW_SIZE)):
                            return True
                    # Comprueba vertical
                    if row <= self.ROWS - self.WINDOW_SIZE:
                        if all(board[row + i][col] == player for i in range(self.WINDOW_SIZE)):
                            return True
                    # Comprueba diagonal de izquierda a derecha
                    if col <= self.COLUMNS - self.WINDOW_SIZE and row <= self.ROWS - self.WINDOW_SIZE:
                        if all(board[row + i][col + i] == player for i in range(self.WINDOW_SIZE)):
                            return True
                    # Comprueba diagonal de derecha a izquierda
                    if col >= self.WINDOW_SIZE - 1 and row <= self.ROWS - self.WINDOW_SIZE:
                        if all(board[row + i][col - i] == player for i in range(self.WINDOW_SIZE)):
                            return True
        return False

    def evaluate_positions(self, board, player):
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
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                if board[row][col] == player:
                    player_total_score += position_values[row][col]

        return player_total_score

    def evaluate_patterns(self, board, player):
        if player == 'X':
            player_patterns = {
                "XXXXXX": 500,
                "XXXX": 100,
                "XXX": 50,
                "XX": 20,
                "X": 10,
                "OOOOOO": -500,
                "OOOO": -100,
                "OOO": -50,
                "OO": -20,
                "O": -10
            }
        else:
            player_patterns = {
                "XXXXXX": -500,
                "XXXX": -100,
                "XXX": -50,
                "XX": -20,
                "X": -10,
                "OOOOOO": 500,
                "OOOO": 100,
                "OOO": 50,
                "OO": 20,
                "O": 10
            }

        total_score = 0

        for i in range(self.ROWS):
            for j in range(self.ROWS):
                for pattern, weight in player_patterns.items():
                    # Verifica patrones en filas hacia abajo
                    if j + len(pattern) <= self.ROWS:
                        row = "".join(board[i][j:j + len(pattern)])
                        if pattern == row:
                            total_score += weight

                    # Verifica patrones en filas hacia arriba
                    if j - len(pattern) >= -1:
                        row = "".join(board[i][j:j - len(pattern):-1])
                        if pattern == row:
                            total_score += weight

                    # Verifica patrones en columnas a la derecha
                    if i + len(pattern) <= self.ROWS:
                        column = "".join(board[k][j] for k in range(i, i + len(pattern)))
                        if pattern == column:
                            total_score += weight

                    # Verifica patrones en columnas a la izquierda
                    if i - len(pattern) >= -1:
                        column = "".join(board[k][j] for k in range(i, i - len(pattern), -1))
                        if pattern == column:
                            total_score += weight

                    # Verifica patrones en diagonal derecha hacia abajo izquierda
                    if j + len(pattern) <= self.ROWS and i + len(pattern) <= self.ROWS:
                        diagonal = "".join(board[i + k][j + k] for k in range(len(pattern)))
                        if pattern == diagonal:
                            total_score += weight

                    # Verifica patrones en diagonal izquierda hacia arriba derecha
                    if j - len(pattern) >= -1 and i - len(pattern) >= -1:
                        diagonal = "".join(board[i - k][j - k] for k in range(len(pattern)))
                        if pattern == diagonal:
                            total_score += weight

                    # Verifica patrones en diagonal izquierda superior a derecha abajo
                    if j + len(pattern) <= self.ROWS and i - len(pattern) >= -1:
                        diagonal = "".join(board[i - k][j + k] for k in range(len(pattern)))
                        if pattern == diagonal:
                            total_score += weight

                    # Verifica patrones en diagonal derecha abajo arriba izquierda
                    if j - len(pattern) >= -1 and i + len(pattern) <= self.ROWS:
                        diagonal = "".join(board[i + k][j - k] for k in range(len(pattern)))
                        if pattern == diagonal:
                            total_score += weight

        return total_score
    
    # Función de heurística avanzada
    def evaluate_advanced(self, board, player):
        # opponent = self.player if player == self.opponent else self.opponent
        self.count_nodes += 1
        player_score = 0
        a = 0

        if self.has_won(board, self.player):
            return float('inf')
        elif self.has_won(board, self.opponent):
            return float('-inf')
        else:
            player_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player}
    
            for pos in player_positions:
                aux, amenazas = self.evaluate_star(board, pos, player)
                player_score += aux
                a += amenazas
           
            player_score = player_score * (10**(2 * a))
            player_score = player_score / 1000   
            if player != self.player:
                print("CABEZON")       
        return player_score if player == self.player else - player_score

    def evaluate_advanced_with_patterns(self, board, player):
        opponent = self.player if player == self.opponent else self.opponent
        self.count_nodes += 1
        player_score = 0
        opponent_score = 0
        a = 0

        if self.has_won(board, self.player):
            return float('inf')
        elif self.has_won(board, self.opponent):
            return float('-inf')
        else:
            player_score += self.evaluate_positions(board, player)
            # opponent_score += evaluate_positions(board, opponent)
            player_score += self.evaluate_patterns(board, player)
            opponent_score += self.evaluate_patterns(board, opponent)

        return player_score - opponent_score #if player == self.player else - player_score

    def is_border(self, position: tuple):
        try:
            if self.have_border:
                if not(0 < position[0] < self.ROWS - 1 and 0 < position[1] < self.COLUMNS - 1):
                    return True
            else:
                if not(0 <= position[0] < self.ROWS and 0 <= position[1] < self.COLUMNS):
                    return True
        except:
            return True
        return False

    def calcule_e_dir(self, board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces, enemy):
        if board[i][j] == self.empty:
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
            if board[i][j] == self.empty:
                free_spaces += 1
            else: 
                enemy += 1

        if not my_places:
            # Cuenta el numero de player que hay juntos. 
            my_busy_places += 1

        return e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces, enemy


    def evaluate_star(self, board, position, player):
        # PESOS ----------------
        w_player = self.weights
        # epsilon = w_player[0] # 3
        epsilon = w_player[2]
        w = w_player[0:5] # [5, 4, 3, 2, 1]
        # w.reverse()
        final_val_weight = w_player[5] # 3
        enemy_busy_places_weight = w_player[6] # 5
        val_weight = w_player[7] # 0.5
        # my_busy_places_weight = w_player[8] # 4
        # e_opponent_weight = w_player[9] # 10**20
        # e_win_weight = w_player[10] # 10**25
        # ----------------------

        amenaza = 0
        enemy = 0

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
            for l in range(2):                  # Dos lados, Ejemplo: (izquierdo, derecho) o (arriba, abajo)
                busy_places = False
                my_places = False
                val = 1  
                enemy = 0
                free_spaces = 0
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
                    if self.is_border((i, j)):
                        break
                    e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces, enemy = self.calcule_e_dir(board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places, free_spaces, enemy)
                
                if enemy == 4 and free_spaces == 0:
                    # Hay 4 enemigos juntos y dos huecos vacios
                    amenaza += 1
                if enemy == 5 and free_spaces == 0:
                    # Hay 4 enemigos juntos y dos huecos vacios
                    amenaza += 2
                # if enemy == 5 and free_spaces == 0:
                #     # Hay 4 enemigos juntos y dos huecos vacios
                #     e = e ** 4

                e += e_dir 

            if final_val >= final_val_weight and enemy_busy_places >= enemy_busy_places_weight: # and free_spaces > 0:
                amenaza += 1
                # print(enemy)
            
            # e = e * 1000 if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight) else e
            # e = e * final_val if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight + 1) else e
            # TODO: Revisar esta función
            e = e * final_val if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight + 1) else e
            '''
            if my_busy_places >= 4:
                print(f"INTENTO GANAR: {(position[0], position[1])}")
                print_board(board)
            e = e * e_win_weight if my_busy_places >= my_busy_places_weight else e
            '''
        return e, amenaza

    # Función para evaluar las amenazas utilizando sliding window
    def evaluate_sliding_window(self, board, player):
        player_score = 0
        self.WINDOW_SIZE = 4  # Tamaño de la ventana

        for row in range(self.ROWS):
            for col in range(self.COLUMNS - self.WINDOW_SIZE + 1):
                window = [board[row][col + i] for i in range(self.WINDOW_SIZE)]
                if window.count(player) == self.WINDOW_SIZE - 1 and window.count(self.empty) == 1:
                    player_score += 1

        for col in range(self.COLUMNS):
            for row in range(self.ROWS - self.WINDOW_SIZE + 1):
                window = [board[row + i][col] for i in range(self.WINDOW_SIZE)]
                if window.count(player) == self.WINDOW_SIZE - 1 and window.count(self.empty) == 1:
                    player_score += 1

        return player_score

    # Función para evaluar la defensa utilizando defensive sliding window
    def evaluate_defensive_sliding_window(self, board, player):
        opponent = self.player if player == self.opponent else self.player
        opponent_score = 0
        self.WINDOW_SIZE = 4  # Tamaño de la ventana

        for row in range(self.ROWS):
            for col in range(self.COLUMNS - self.WINDOW_SIZE + 1):
                window = [board[row][col + i] for i in range(self.WINDOW_SIZE)]
                if window.count(opponent) == self.WINDOW_SIZE - 1 and window.count(self.empty) == 1:
                    opponent_score += 1

        for col in range(self.COLUMNS):
            for row in range(self.ROWS - self.WINDOW_SIZE + 1):
                window = [board[row + i][col] for i in range(self.WINDOW_SIZE)]
                if window.count(opponent) == self.WINDOW_SIZE - 1 and window.count(self.empty) == 1:
                    opponent_score += 1

        return opponent_score

    # Función para generar el hash Zobrist del tablero
    def zobrist_hash(self, board):
        hash_val = 0
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if board[i][j] == 'X':
                    hash_val ^= self.hash_table[i * self.ROWS + j][0]
                elif board[i][j] == 'O':
                    hash_val ^= self.hash_table[i * self.ROWS + j][1]
                elif board[i][j] == '$':
                    hash_val ^= self.hash_table[i * self.ROWS + j][2]
                else:
                    hash_val ^= self.hash_table[i * self.ROWS + j][3]
        return hash_val
    
    def get_order_moves(self, board, all_actions, player, opponent, num_ordered_moves = None):
        valid_moves = self.actions(board, all_actions, self.RANGE, player)
        moves_with_score = {}
        #Bucle en movimientos para guardar en un set en tuplas de 4
        for move in valid_moves:
            valid_moves_2 = self.actions(self.result(board, move, player), all_actions.union({move}), self.RANGE, player)
            for move_2 in valid_moves_2:
                score = 0
                # # TODO: Hay que revisar si a este board se le han aplicado los anteriores movimientos
                # # score = self.evaluate_advanced(board, self.player)
                # board_hash_2 = self.zobrist_hash(self.result(self.result(board, move, opponent), move_2, opponent))
                # if board_hash_2 in self.transposition_table:
                #     score = self.transposition_table[board_hash_2]
                #     # print("Tabla HASH")
                # else:
                score = self.evaluate_advanced(self.result(self.result(board, move, player), move_2, player), self.player)
                # self.transposition_table[board_hash_2] = score
                    # print("NO - Tabla HASH")

                moves_with_score[score] = (move[0], move[1], move_2[0], move_2[1])

        # Obtenemos lista de tuplas de mejor a peor
        '''
        ordered_moves = dict(sorted(moves_with_score.items(), key=lambda x: x[0], reverse=True))
        ordered_moves = [values for _, values in moves_with_score.items()]
        '''
        ordered_moves = [moves_with_score[score] for score in sorted(moves_with_score, reverse=True)]
        # ordered_moves = ordered_moves[:1]
        if num_ordered_moves == None:
            return ordered_moves[:]
        else:
            return ordered_moves[:num_ordered_moves]


    # Función para realizar la búsqueda en ventanas
    def window_search(self, board, player, depth, alpha, beta, action, all_actions, predicted_actions, maximizing_player = True):

        # board_hash = self.zobrist_hash(board)
        if depth == 0 or self.has_won(board, self.player) or self.has_won(board, self.opponent):
            # if board_hash in self.transposition_table:
            #     return self.transposition_table[board_hash]
            value = self.evaluate_advanced(board, self.player)
            # self.transposition_table[board_hash] = value
            return value
    
        valid_moves = self.actions(board, all_actions, self.RANGE, player)
        opponent = self.player if player == self.opponent else self.opponent
        # valid_moves_part_1, valid_moves_part_2 = self.tuples_divider(valid_moves)

        if(len(valid_moves) == 0):
            return 0
        
        # ordered_moves = self.get_order_moves(board, all_actions, player, opponent, 10)
        ordered_moves = self.get_order_moves(board, predicted_actions, player, opponent, self.best_n_moves)

        if maximizing_player:
            value = float('-inf')
            for move in ordered_moves:
                move_1 = (move[0],move[1])
                move_2 = (move[2],move[3])
                new_actions = all_actions.union({move_1, move_2})
                # new_predicted_actions = predicted_actions.union({move_1, move_2})
                new_predicted_actions = {move_1, move_2}
                value = max(value, self.window_search(self.result(self.result(board, move_1, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, new_predicted_actions, maximizing_player=False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    print('PODO', depth)
                    break
            return value
        else:
            value = float('inf')
            for move in ordered_moves:
                move_1 = (move[0],move[1])
                move_2 = (move[2],move[3])
                new_actions = all_actions.union({move_1, move_2})
                # new_predicted_actions = predicted_actions.union({move_1, move_2})
                new_predicted_actions = predicted_actions
                value = min(value, self.window_search(self.result(self.result(board, move_1, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, new_predicted_actions, maximizing_player=True))
                beta = min(beta, value)
                if alpha >= beta:
                    print('PODO', depth)
                    break
            return value          
        '''
        if maximizing_player:
            value = float('-inf')
            for move in valid_moves:# - valid_moves_part_1:
                valid_moves_2 = self.actions(self.result(board, move, player), all_actions.union({move}), self.RANGE, player)
                for move_2 in valid_moves_2:#  - valid_moves_part_2:
                    new_actions = all_actions.union({move, move_2})
                    
                    value = max(value, self.window_search(self.result(self.result(board, move, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, w_player, maximizing_player=False))
                    new_actions = set()
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value
        else:
            value = float('inf')
            for move in valid_moves - valid_moves_part_1:
                valid_moves_2 = self.actions(self.result(board, move, player), all_actions.union({move}), self.RANGE, player)
                for move_2 in valid_moves_2 - valid_moves_part_2:
                    new_actions = all_actions.union({move, move_2})
                    value = min(value, self.window_search(self.result(self.result(board, move, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, w_player, maximizing_player=True))
                    new_actions = set()
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value
        '''   

    def tuples_divider(self, conjunto_tuplas):
        # Calcular la mitad del conjunto
        mitad = len(conjunto_tuplas) // 2

        # Dividir el conjunto en dos partes
        parte_1 = set(list(conjunto_tuplas)[:mitad])
        parte_2 = conjunto_tuplas - parte_1
        return parte_1, parte_2

    # Función para elegir el mejor movimiento con búsqueda de ventana
    def choose_best_move(self, board, player, depth):
        best_move = (None, None)
        best_move_2 = (None, None)
        best_value = float('-inf')
        new_actions = set()

        if len(self.all_positions) > 0:
            all_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val != self.border and val != self.empty}
        else:
            all_positions = self.all_positions

        valid_moves = self.actions(board, all_positions, self.RANGE, player)
        # valid_moves_part_1, valid_moves_part_2 = self.tuples_divider(valid_moves)

        for move in valid_moves:# - valid_moves_part_1:
            valid_moves_2 = self.actions(self.result(board, move, player), all_positions.union({move}), self.RANGE, player)
            for move_2 in valid_moves_2:# - valid_moves_part_2:
                
                new_actions = new_actions.union({move, move_2})
                value = self.window_search(self.result(self.result(board, move, player), move_2, player), player, depth - 1, float('-inf'), float('inf'), move_2, new_actions, maximizing_player=False)
                new_actions = set()
                
                if value > best_value:
                    best_value = value
                    best_move = move
                    best_move_2 = move_2

        return best_move, best_move_2


    # Función para elegir el mejor movimiento con búsqueda de ventana
    def choose_best_move_2(self, board, player, depth):
        
        time_in_round = time.time()

        if board[self.ROWS // 2][self.COLUMNS // 2] == self.empty:
            board[self.ROWS // 2][self.COLUMNS // 2] = player
            self.all_positions.add((self.ROWS // 2, self.COLUMNS // 2))
            return (self.ROWS // 2, self.COLUMNS // 2), None

        best_move = (None, None)
        best_move_2 = (None, None)
        best_value = float('-inf')
        value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        predicted_actions = set()

        all_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val != self.border and val != self.empty}
        # if len(self.all_positions) > 0:
        # else:
        #     all_positions = self.all_positions

        opponent = self.player if player == self.opponent else self.opponent
        ordered_moves = self.get_order_moves(board, all_positions, player, opponent, self.best_n_moves)

        start_time = time.time()

        print('PLAYER', player, 'Oponent', opponent, ordered_moves[:10])
        for move in ordered_moves:
            move_1 = (move[0],move[1])
            move_2 = (move[2],move[3])
            
            new_actions = all_positions.union({move_1, move_2})
            predicted_actions = {move_1, move_2}
            # value = self.window_search(self.result(self.result(board, move_1, player), move_2, player), player, depth - 1, alfa, beta, move_2, new_actions, w_player, maximizing_player=False)
            value = max(value, self.window_search(self.result(self.result(board, move_1, player), move_2, player), player, depth - 1, alpha, beta, move_2, new_actions, predicted_actions, maximizing_player=False))
            alpha = max(alpha, value)
            # print("VALUE", value)


            if value > best_value:
                best_value = value
                best_move = move_1
                best_move_2 = move_2

            if time.time() - start_time > self.TIME_LIMIT:
                self.time_per_round.append(time.time() - time_in_round)
                print("Tiempo agotado", self.TIME_LIMIT)
                return best_move, best_move_2
            
            if alpha >= beta:
                print("PODO", depth)
                break

            
        self.time_per_round.append(time.time() - time_in_round)

        print(best_move, best_move_2)
        return best_move, best_move_2

    def show_plot_rounds(self, x, y):
        # Crear el gráfico
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='blue')

        # Etiquetas y título
        plt.xlabel('Rondas de la Partida')
        plt.ylabel('Tiempo de Ejecución por Ronda (segundos)')
        plt.title('Tiempo de Ejecución por Ronda en una Partida')

        # Mostrar la gráfica
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def show_plot_nodes(self, x, y):
        # Crear el gráfico
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='blue')

        # Etiquetas y título
        plt.xlabel('Rondas de la Partida')
        plt.ylabel('Nodos evaluados por Ronda')
        plt.title('Nodos evaluados por Ronda en una Partida')

        # Mostrar la gráfica
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Función principal del juego
    def play_connect6(self, w_player, w_opponent, autobot = True, verbose = False):
        best_player = None
        board = self.create_board()
        round = 0

        initial_player = self.opponent  # El jugador (X) comienza los movimientos
        self.set_player_and_opponent(new_player = self.opponent,
                                     new_opponent = self.player)
        self.set_weights(new_weights=w_opponent)
        print(self.player, self.weights)
        
        print("Bienvenido al juego de Conecta6!")

        while True:
            if verbose:
                print(board)
                self.print_board(board)
            # for _ in range(2):  # Realiza dos movimientos en cada turno
            if initial_player == self.opponent:
                if not autobot:
                    self.last_postion.clear()

                    for _ in range(2):
                        while True:
                            try:
                                row = int(input("Ingresa la fila: "))
                                col = int(input("Ingresa la columna: "))
                            except ValueError:
                                print("Entrada no válida. Ingresa números enteros.")
                                continue
                            if not self.is_valid_move(board, row, col):
                                print("Movimiento no válido. La casilla ya está ocupada.")
                                continue
                            self.all_positions.add((row, col))
                            self.make_move(board, self.opponent, row, col)

                            self.last_postion.add((row, col))
                            break
                    self.set_player_and_opponent(new_player = self.opponent,
                                                 new_opponent = self.player)
                else:

                    '''MAQUINA vs MAQUINA'''
                    # row, col = choose_best_move(board, self.opponent, depth)
                    # make_move(board, self.opponent, row, col)
                    self.set_player_and_opponent(new_player = self.opponent,
                                                 new_opponent = self.player)
                    self.set_weights(new_weights=w_opponent)
                    jugada1, jugada2 = self.choose_best_move_2(board, self.player, self.DEPTH)
                    self.all_positions.add((jugada1[0], jugada1[1]))
                    self.make_move(board, self.player, jugada1[0], jugada1[1])
                    if jugada2 != None:
                        self.all_positions.add((jugada2[0], jugada2[1]))
                        self.make_move(board, self.player, jugada2[0], jugada2[1])
            else:
                self.set_player_and_opponent(new_player = self.opponent,
                                             new_opponent = self.player)
                self.set_weights(new_weights=w_player)
                jugada1, jugada2 =  self.choose_best_move_2(board, self.player, self.DEPTH)
                if jugada1 == (None,None) and jugada2 == (None,None):
                    pass
                    #self.print_board(board)
                else:
                    self.all_positions.add((jugada1[0], jugada1[1]))
                    self.make_move(board, self.player, jugada1[0], jugada1[1])
                    if jugada2 != None:
                        self.all_positions.add((jugada2[0], jugada2[1]))
                        self.make_move(board, self.player, jugada2[0], jugada2[1])
        

            if self.has_won(board, self.player):
                if verbose:
                    self.print_board(board)
                    print(f"¡El jugador {self.player} ha ganado!")
                    print(f"Mejor peso: {self.weights}")
                best_player = self.player
                break
            if all(all(cell != self.empty for cell in row) for row in board):
                if verbose:
                    self.print_board(board)
                    print("¡Es un empate!")
                break

            round += 1
            self.rounds.append(round) 
            self.nodes_evaluated.append(self.count_nodes)
            # self.rounds = self.rounds if len(self.rounds) == len(self.time_per_round) else self.rounds[:len(self.rounds) // 2]
            self.count_nodes = 0

            # player = self.player if player == self.opponent else self.opponent
        print(self.rounds, self.time_per_round, self.nodes_evaluated)
        self.show_plot_rounds(self.rounds, self.time_per_round)
        self.show_plot_nodes(self.rounds, self.nodes_evaluated)

        return best_player

if __name__ == "__main__":
    w = [
        5, 4, 3, 2, 1,     # w
        3,                 # final_val_weight
        5,                 # enemy_busy_places_weight
        0.5,               # val_weight
        20                 # N_best_moves_weight
    ]

    # w = [
    #     4.618268110967487,
    #     4.171445178044721,
    #     3.4406837522999445,
    #     1.6148067426093888,
    #     1.4499124860640344,
    #     2.9643650627564053,
    #     7,
    #     0.11567832043012127,
    #     18
    # ]

    w_opponent = [
        4.967394294832711,
        4.047565463606995,
        3.254086133285639,
        2.211861046951265,
        0.6930561813454589,
        2.976518041034753,
        5,
        0.6900514807500613,
        24]

    # w = [
    #     5.440125720349658,
    #     3.801169896265987,
    #     3.466591753465339,
    #     1.8002378612193457,
    #     0.6196233398563769,
    #     2.782827933885025,
    #     3.8241072409163737,
    #     0.7335043259196556
    # ]

    g = Game(depth = 3,
             weights = w,
             size = (21,21),
             time_limit = 15,
             have_border=True,
             border = '$',
             empty = '-',
             player = 'X',
             opponent = 'O')

    g.play_connect6(w_player = w,
                    w_opponent = w_opponent,
                    autobot = False,
                    verbose = True)
    
    # board = create_board()
    # print(reduce_board(board,19,19,13))
