import math
import time
from copy import deepcopy
from rich import print
import random

class Game():
    def __init__(self, depth, weights, size = (19, 19), have_border = False, border = None, empty = "-", player_black = "X", player_white = "O") -> None:
        # Constantes para representar los jugadores
        self.empty = empty
        self.player_black = player_black
        self.player_white = player_white
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
        # PESOS
        self.weights = weights
        self.all_positions = set()
        self.last_postion = set() 

        self.hash_table = [[random.getrandbits(64) for _ in range(4)] for _ in range(size[0] * size[1])]
        self.transposition_table = {}

    def set_board(self, board):
        self.board = board

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

        # Coloca una X en el centro del tablero
        board[self.ROWS // 2][self.COLUMNS // 2] = self.player_black
        self.all_positions.add((self.ROWS // 2, self.COLUMNS // 2))
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
        oponent = self.player_black if player == self.player_white else self.player_white
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

    # Función de heurística avanzada
    def evaluate_advanced(self, board, player, w_player):
        opponent = self.player_black if player == self.player_white else self.player_white
        
        player_score = 0
        opponent_score = 0
        a = 0

        if self.has_won(board, self.player_black):
            return float('inf')
        elif self.has_won(board, self.player_white):
            return float('-inf')
        else:
            player_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player}# and (i,j) in all_actions}
            opponent_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == opponent}# and (i,j) in all_actions}
            # all_board = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player or val == opponent}
    
            for pos in player_positions:
                aux, amenazas = self.evaluate_star(board, pos, player, w_player)
                player_score += aux
                a += amenazas
           
            player_score = player_score * (10**(2 * a)) # 12
            player_score = player_score / 1000          # 10 ** 17
        return player_score if player == self.player_black else - player_score # - opponent_score


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


    def evaluate_star(self, board, position, player, w_player):
        # PESOS ----------------
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

            if final_val >= 3 and enemy_busy_places >= 5: # and free_spaces > 0:
                amenaza += 1
                # print(enemy)
            
            # e = e * 1000 if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight) else e
            # e = e * final_val if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight + 1) else e
            # TODO: Revisar esta función
            e = e * final_val if ((final_val >= final_val_weight) and enemy_busy_places >= 5 + 1) else e
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
        opponent = self.player_black if player == self.player_white else self.player_black
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
                # # score = self.evaluate_advanced(board, self.player_black, w_player)
                # board_hash_2 = self.zobrist_hash(self.result(self.result(board, move, opponent), move_2, opponent))
                # if board_hash_2 in self.transposition_table:
                #     score = self.transposition_table[board_hash_2]
                #     # print("Tabla HASH")
                # else:
                score = self.evaluate_advanced(self.result(self.result(board, move, player), move_2, player), player, self.weights)
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
    def window_search(self, board, player, depth, alpha, beta, action, all_actions, predicted_actions, w_player, maximizing_player = True):

        # board_hash = self.zobrist_hash(board)
        if depth == 0 or self.has_won(board, self.player_black) or self.has_won(board, self.player_white):
            # if board_hash in self.transposition_table:
            #     return self.transposition_table[board_hash]
            value = self.evaluate_advanced(board, player, w_player)
            # self.transposition_table[board_hash] = value
            return value
    
        valid_moves = self.actions(board, all_actions, self.RANGE, player)
        opponent = self.player_black if player == self.player_white else self.player_white
        # valid_moves_part_1, valid_moves_part_2 = self.tuples_divider(valid_moves)

        if(len(valid_moves) == 0):
            return 0
        
        # ordered_moves = self.get_order_moves(board, all_actions, player, opponent, 10)
        ordered_moves = self.get_order_moves(board, predicted_actions, player, opponent, 20)

        if maximizing_player:
            value = float('-inf')
            for move in ordered_moves:
                move_1 = (move[0],move[1])
                move_2 = (move[2],move[3])
                new_actions = all_actions.union({move_1, move_2})
                # new_predicted_actions = predicted_actions.union({move_1, move_2})
                new_predicted_actions = {move_1, move_2}
                value = max(value, self.window_search(self.result(self.result(board, move_1, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, new_predicted_actions, w_player, maximizing_player=False))
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
                value = min(value, self.window_search(self.result(self.result(board, move_1, opponent), move_2, opponent), opponent, depth - 1, alpha, beta, move_2, new_actions, new_predicted_actions, w_player, maximizing_player=True))
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
    def choose_best_move(self, board, player, depth, w_player):
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
                value = self.window_search(self.result(self.result(board, move, player), move_2, player), player, depth - 1, float('-inf'), float('inf'), move_2, new_actions, w_player, maximizing_player=False)
                new_actions = set()
                
                if value > best_value:
                    best_value = value
                    best_move = move
                    best_move_2 = move_2

        return best_move, best_move_2


    # Función para elegir el mejor movimiento con búsqueda de ventana
    def choose_best_move_2(self, board, player, depth, w_player):
        best_move = (None, None)
        best_move_2 = (None, None)
        best_value = float('-inf')
        value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        predicted_actions = set()

        if len(self.all_positions) > 0:
            all_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val != self.border and val != self.empty}
        else:
            all_positions = self.all_positions

        opponent = self.player_black if player == self.player_white else self.player_white
        ordered_moves = self.get_order_moves(board, all_positions, player, opponent, 20)

        print('PLAYER', player, 'Oponent', opponent, ordered_moves[:10])
        for move in ordered_moves:
            move_1 = (move[0],move[1])
            move_2 = (move[2],move[3])
            
            new_actions = all_positions.union({move_1, move_2})
            predicted_actions = {move_1, move_2}
            # value = self.window_search(self.result(self.result(board, move_1, player), move_2, player), player, depth - 1, alfa, beta, move_2, new_actions, w_player, maximizing_player=False)
            value = max(value, self.window_search(self.result(self.result(board, move_1, player), move_2, player), player, depth - 1, alpha, beta, move_2, new_actions, predicted_actions, w_player, maximizing_player=False))
            alpha = max(alpha, value)
            # print("VALUE", value)

            if value > best_value:
                best_value = value
                best_move = move_1
                best_move_2 = move_2

            if alpha >= beta:
                print("PODO", depth)
                break

            

        print(best_move, best_move_2)
        return best_move, best_move_2

    # Función principal del juego
    def play_connect6(self, w_player, w_opponent, autobot = True):
        best_player = None
        board = self.create_board()

        player = self.player_white  # El jugador (O) comienza los movimientos
        
        time_limit_per_move = float('inf')  # No hay límite de tiempo

        print("Bienvenido al juego de Conecta6!")

        while True:
            if not autobot:
                print(board)
                self.print_board(board)
            # for _ in range(2):  # Realiza dos movimientos en cada turno
            if player == self.player_white:
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
                            self.make_move(board, player, row, col)

                            self.last_postion.add((row, col))
                            break
                else:

                    '''MAQUINA vs MAQUINA'''
                    # row, col = choose_best_move(board, self.player_white, depth, w_player)
                    # make_move(board, self.player_white, row, col)
                    jugada1, jugada2 = self.choose_best_move_2(board, self.player_white, self.DEPTH, w_player)
                    self.all_positions.add((jugada1[0], jugada1[1]))
                    self.all_positions.add((jugada2[0], jugada2[1]))
                    self.make_move(board, self.player_white, jugada1[0], jugada1[1])
                    self.make_move(board, self.player_white, jugada2[0], jugada2[1])
                    
            else:
                jugada1, jugada2 =  self.choose_best_move_2(board, self.player_black, self.DEPTH, w_opponent)
                if jugada1 == (None,None) and jugada2 == (None,None):
                    pass
                    #self.print_board(board)
                else:
                    self.all_positions.add((jugada1[0], jugada1[1]))
                    self.all_positions.add((jugada2[0], jugada2[1]))
                    # print('BEST MOVE', row, col)
                    self.make_move(board, self.player_black, jugada1[0], jugada1[1])
                    self.make_move(board, self.player_black, jugada2[0], jugada2[1])
                    
                    

            if self.has_won(board, player):
                if not autobot:
                    self.print_board(board)
                    print(f"¡El jugador {player} ha ganado!")
                best_player = player
                break
            if all(all(cell != self.empty for cell in row) for row in board):
                if not autobot:
                    self.print_board(board)
                    print("¡Es un empate!")
                break

            player = self.player_black if player == self.player_white else self.player_white
        return best_player

if __name__ == "__main__":
    w = [
        # 3,                 # epsilon
        5, 4, 3, 2, 1,     # w
        3,                 # final_val_weight
        4,                 # enemy_busy_places_weight
        0.5,               # val_weight
                           # NO SE USAN ---------------
        # 4,                 # my_busy_places_weight
        # 10**20,            # e_opponent_weight
        # 10**25,            # e_win_weight
    ]

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
             have_border=True,
             border = '$',
             empty = '-',
             player_black = 'X',
             player_white = 'O')

    g.play_connect6(w, w, autobot = False)
    # board = create_board()
    # print(reduce_board(board,19,19,13))
