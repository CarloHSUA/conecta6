from defines import *
import time

# Point (x, y) if in the valid position of the board.
def isValidPos(x,y):
    return x>0 and x<Defines.GRID_NUM-1 and y>0 and y<Defines.GRID_NUM-1
    
def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][Defines.GRID_NUM - 1] = board[Defines.GRID_NUM - 1][i] = Defines.BORDER
    for i in range(1, Defines.GRID_NUM - 1):
        for j in range(1, Defines.GRID_NUM - 1):
            board[i][j] = Defines.NOSTONE
            
def make_move(board, move, color):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color

def unmake_move(board, move):
    board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE
    board[move.positions[1].x][move.positions[1].y] = Defines.NOSTONE

def is_win_by_premove(board, preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for direction in directions:
        for i in range(len(preMove.positions)):
            count = 0
            position = preMove.positions[i]
            n = x = position.x
            m = y = position.y
            movStone = board[n][m]
            
            if (movStone == Defines.BORDER or movStone == Defines.NOSTONE):
                return False
                
            while board[x][y] == movStone:
                count += 1
                x += direction[0]
                y += direction[1]

            x = n - direction[0]
            y = m - direction[1]

            while board[x][y] == movStone:
                count += 1
                x -= direction[0]
                y -= direction[1]

            if count >= 6:
                return True

    return False

def get_msg(max_len):
    buf = input().strip()
    return buf[:max_len]

def log_to_file(msg):
    g_log_file_name = Defines.LOG_FILE
    try:
        with open(g_log_file_name, "a") as file:
            tm = time.time()
            ptr = time.ctime(tm)
            ptr = ptr[:-1]
            file.write(f"[{ptr}] - {msg}\n")
        return 0
    except Exception as e:
        print(f"Error: Can't open log file - {g_log_file_name}")
        return -1

def move2msg(move):
    if move.positions[0].x == move.positions[1].x and move.positions[0].y == move.positions[1].y:
        msg = f"{chr(ord('S') - move.positions[0].x + 1)}{chr(move.positions[0].y + ord('A') - 1)}"
        return msg
    else:
        msg = f"{chr(move.positions[0].y + ord('A') - 1)}{chr(ord('S') - move.positions[0].x + 1)}" \
              f"{chr(move.positions[1].y + ord('A') - 1)}{chr(ord('S') - move.positions[1].x + 1)}"
        return msg

def msg2move(msg):
    move = StoneMove()
    if len(msg) == 2:
        move.positions[0].x = move.positions[1].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = move.positions[1].y = ord(msg[0]) - ord('A') + 1
        move.score = 0
        return move
    else:
        move.positions[0].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = ord(msg[0]) - ord('A') + 1
        move.positions[1].x = ord('S') - ord(msg[3]) + 1
        move.positions[1].y = ord(msg[2]) - ord('A') + 1
        move.score = 0
        return move

def print_board(board, preMove=None):
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{chr(ord('A') - 1 + i)}", end=" ")
        for j in range(1, Defines.GRID_NUM - 1):
            x = Defines.GRID_NUM - 1 - j
            y = i
            stone = board[x][y]
            if stone == Defines.NOSTONE:
                print(" -", end="")
            elif stone == Defines.BLACK:
                print(" O", end="")
            elif stone == Defines.WHITE:
                print(" *", end="")
        print(" ", end="")        
        print(f"{chr(ord('A') - 1 + i)}", end="\n")
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, Defines.GRID_NUM - 1)]))

def print_score(move_list, n):
    board = [[0] * Defines.GRID_NUM for _ in range(Defines.GRID_NUM)]
    for move in move_list:
        board[move.x][move.y] = move.score

    print("  " + "".join([f"{i:4}" for i in range(1, Defines.GRID_NUM - 1)]))
    for i in range(1, Defines.GRID_NUM - 1):
        print(f"{i:2}", end="")
        for j in range(1, Defines.GRID_NUM - 1):
            score = board[i][j]
            if score == 0:
                print("   -", end="")
            else:
                print(f"{score:4}", end="")
        print()
        
        

## OUR CODE STARTS HERE
def evaluate_advanced(board, position, player, w_player):
    opponent = Defines.BLACK if player == Defines.WHITE else Defines.WHITE
    player_score = 0
    opponent_score = 0
    if has_won(board, player):
        return float('inf')
    elif has_won(board, opponent):
        return float('-inf')
    else:
        player_score = evaluate_star(board, position, player, w_player)
    return player_score 

def evaluate_star(board, position, player, w_player):
    # PESOS ----------------
    epsilon = w_player[0] # 3
    w = w_player[1:6] # [5, 4, 3, 2, 1]
    final_val_weight = w_player[6] # 3
    enemy_busy_places_weight = w_player[7] # 5
    my_busy_places_weight = w_player[8] # 4
    e_opponent_weight = w_player[9] # 10**20
    e_win_weight = w_player[10] # 10**25
    val_weight = w_player[11] # 0.5
    # ----------------------

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
                if isValidPos(i, j):
                    break
                e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_places = calcule_e_dir(board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places)
            e += e_dir

        # if final_val >= 3:
            # print("final_val: ", final_val)
        #  and total_busy_places >= 5
        
        e = e * e_opponent_weight if ((final_val >= final_val_weight) and enemy_busy_places >= enemy_busy_places_weight) else e
        
        # if my_busy_places >= 5:
        #     print(f"INTENTO GANAR: {(position[0], position[1])}")
        #     print_board(board)
        e = e * e_win_weight if my_busy_places >= my_busy_places_weight else e
        
    # e = e if player == PLAYER_X else -e
    return e

def calcule_e_dir(board, i, j, epsilon, player, w, next_pos, e_dir, val, val_weight, final_val, busy_places, enemy_busy_places, my_places, my_busy_places):
    if board[i][j] == '-':
        e_dir *= epsilon
        val -= 0.5
        my_places = True
    elif board[i][j] == player:
        e_dir *=  w[next_pos-1]
        val = 0
        busy_places = True
    else:
        my_places = True
        if val > 0.:
            final_val += val

    if not busy_places:
        enemy_busy_places += 1

    if not my_places:
        my_busy_places += 1

    return e_dir, final_val, val, busy_places, enemy_busy_places, my_places, my_busy_place

def has_won(board, player):
    for row in range(Defines.GRID_NUM):
        for col in range(Defines.GRID_NUM):
            if board[row][col] == player:
                # Comprueba horizontal
                if col <= Defines.GRID_NUM - Defines.WINDOW_SIZE:
                    if all(board[row][col + i] == player for i in range(Defines.WINDOW_SIZE)):
                        return True
                # Comprueba vertical
                if row <= Defines.GRID_NUM - Defines.WINDOW_SIZE:
                    if all(board[row + i][col] == player for i in range(Defines.WINDOW_SIZE)):
                        return True
                # Comprueba diagonal de izquierda a derecha
                if col <= Defines.GRID_NUM - Defines.WINDOW_SIZE and row <= Defines.GRID_NUM - Defines.WINDOW_SIZE:
                    if all(board[row + i][col + i] == player for i in range(Defines.WINDOW_SIZE)):
                        return True
                # Comprueba diagonal de derecha a izquierda
                if col >= Defines.WINDOW_SIZE - 1 and row <= Defines.GRID_NUM - Defines.WINDOW_SIZE:
                    if all(board[row + i][col - i] == player for i in range(Defines.WINDOW_SIZE)):
                        return True
    return False

def get_opponent(player):
    if player == Defines.BLACK:
        return Defines.WHITE
    else:
        return Defines.BLACK
    
def actions(board, array_tuplas, player):
    out_set = set()
    recorrido = Defines.RANGE * 2 + 1
    if(array_tuplas):
        for tupla in array_tuplas:
            i_inicial = tupla[0] - Defines.RANGE
            j_inicial = tupla[1] - Defines.RANGE
            
            for i in range(recorrido):
                for j in range(recorrido):
                    if(not is_oponent_or_border(board, (i + i_inicial, j + j_inicial), player) and board[i + i_inicial][j + j_inicial] != player):
                        out_set.add((i + i_inicial, j + j_inicial))
    return out_set

def is_oponent_or_border(board, position: tuple, player):
    oponent = get_opponent(player)
    try:
        if board[position[0]][position[1]] == oponent or not isValidPos(position[0], position[1]):
            return True
    except:
        return True
    return False