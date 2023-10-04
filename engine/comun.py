import os
import sys
import numpy as np
from rich import print
from copy import deepcopy

from minmax import minmax
from alfabeta import alfabeta


main_board = [['-', 'X', '-'],
              ['-', '-', '-'],
              ['-', '-', '-']]

main_board = [['-' for _ in range(19)] for _ in range(19)]
main_board[0][0] = 'X'
X_positions = set()
X_positions.add((1,1))
O_positions = set()

# Se puede elegir el jugador con el modulo de una variable, si es par uno y si es impar el otro jugador
turn = 0
limit = 19
depth = 1

def update_board(board, action):
    
    if not (0 <= action[0] < limit and 0 <= action[1] < limit):
        board[action[0]][action[1]] = player(board)
    return board


def player(board):
    X = 0
    O = 0
    for row in board:
        for col in row:
            if col != '-':
                if col == 'X':
                    X+=1
                else:
                    O+=1
    if X <= O or X == 0:
        return 'X'
    else:
        return 'O'
    

def actions(board):
    '''
    Input -> board
    Return -> set de movimientos posibles {(i,j), (i,j), (i,j)}
    '''
    out_set = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == '-':
                out_set.add((i, j))
    return out_set


def result(board: list[list[str]], action: tuple):
    '''
    Input board and action (i, j)
    Return deep copy board
    '''
    if not (0 <= action[0] < limit and 0 <= action[1] < limit):
        raise Exception("Index out of bounds")
    copy_board = deepcopy(board)
    copy_board[action[0]][action[1]] = player(board)
    return copy_board


def winner(board):
    '''
    Input board
    Output 'X' or 'O'
    '''
    # for i in range(len(board)):
    #     if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not '-':
    #         return board[i][0]
        
    # for i in range(len(board)):
    #     if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not '-':
    #         return board[0][i]
        
    # if board[0][0] == board[1][1] == board[2][2] and board[1][1] is not '-':
    #     return board[1][1]
    
    # if board[0][2] == board[1][1] == board[2][0] and board[1][1] is not '-':
    #     return board[1][1]
     # Verificar victoria horizontal
    for row in board:
        if ''.join(row).count('X' * 6) > 0:
            return 'X'
        if ''.join(row).count('O' * 6) > 0:
            return 'O'

    # Verificar victoria vertical
    for col in range(len(board[0])):
        column = ''.join([row[col] for row in board])
        if column.count('X' * 6) > 0:
            return 'X'
        if column.count('O' * 6) > 0:
            return 'O'

    # Verificar victoria en diagonal (ascendente)
    for i in range(len(board) - 5):
        for j in range(len(board[0]) - 5):
            diagonal = ''.join([board[i + k][j + k] for k in range(6)])
            if diagonal.count('X' * 6) > 0:
                return 'X'
            if diagonal.count('O' * 6) > 0:
                return 'O'

    # Verificar victoria en diagonal (descendente)
    for i in range(len(board) - 5):
        for j in range(5, len(board[0])):
            diagonal = ''.join([board[i + k][j - k] for k in range(6)])
            if diagonal.count('X' * 6) > 0:
                return 'X'
            if diagonal.count('O' * 6) > 0:
                return 'O'

    return None

def terminal(board):
    return (winner(board) is not None or not any('-' in i for i in board))

def utility(board):
    '''
    Esta es la función heurística
    '''
    if terminal(board):
        if winner(board) == 'X':
            return 1
        if winner(board) == 'O':
            return -1
    return 0

def is_oponent_or_border(board, position: tuple):
    if player(board) == 'O':
        opponnent = 'X'
    else: 
        opponnent = 'O'

    try:
        if board[position[0]][position[1]] == opponnent:
            return True
    except IndexError:
        return True
    return False



def evaluate(board,threat_size,opponnent):
    for row in board:
        if ''.join(row).count(opponnent * threat_size) > 0:
            return True

    # Verificar victoria vertical
    for col in range(len(board[0])):
        column = ''.join([row[col] for row in board])
        if column.count(opponnent * threat_size) > 0:
            return True

    # Verificar victoria en diagonal (ascendente)
    for i in range(len(board) - 5):
        for j in range(len(board[0]) - 5):
            diagonal = ''.join([board[i + k][j + k] for k in range(threat_size)])
            if diagonal.count(opponnent * threat_size) > 0:
                return True

    # Verificar victoria en diagonal (descendente)
    for i in range(len(board) - 5):
        for j in range(5, len(board[0])):
            diagonal = ''.join([board[i + k][j - k] for k in range(threat_size)])
            if diagonal.count(opponnent * threat_size) > 0:
                return True

    return False

def threat_space_search(board,threat_sizeopponnent):
    threat_size = 4
    
    if evaluate(threat_size):
        return False 
    pass

def sliding_window():
    pass

def defensive_slide_window():
    pass

def hmove_evaluation(board, position: tuple):
    '''
    Input position -> Evalua con un número como de buena es esa posición del tablero
    Return el score
    '''
    epsilon = 2
    w = [5,4,3,2,1]
    e = 0
    e_dir = 1

    for dir in range(4):                    # Cuatro direcciones (0 = Horizontal, 1 = Diagonal Creciente, 2 = , 
        for l in range(2):                  # Dos lados, Ejemplo: (izquierdo, derecho) o (arriba, abajo)  
            for next_pos in range(5):       # Por cada punto del lado
                if l == 0:                  # a
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] + next_pos
                        if is_oponent_or_border(board, (i, j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]


                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] - next_pos
                        j = position[1] + next_pos
                        if is_oponent_or_border(board, (i, j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]

                        
                    elif dir == 2:          # Vertical
                        i = position[0] - next_pos
                        j = position[1]
                        if is_oponent_or_border(board, (i,j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]

                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] - next_pos
                        j = position[1] - next_pos
                        if is_oponent_or_border(board, (i,j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]
                    
                else:                       # b
                    
                    if dir == 0:            #  Horizontal
                        i = position[0]
                        j = position[1] - next_pos
                        if is_oponent_or_border(board, (i, j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]


                    elif dir == 1:          # Diagonal ascendente
                        i = position[0] + next_pos
                        j = position[1] - next_pos
                        if is_oponent_or_border(board, (i, j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]

                        
                    elif dir == 2:          # Vertical
                        i = position[0] + next_pos
                        j = position[1]
                        if is_oponent_or_border(board, (i,j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]

                        
                    elif dir == 3:          # Diagonal descendente
                        i = position[0] + next_pos
                        j = position[1] + next_pos
                        if is_oponent_or_border(board, (i,j)):
                            break
                        elif board[i][j] == '-':
                            e_dir *= epsilon
                        elif board[i][j] == player(board):
                            e_dir *= w[next_pos]
            e = e + e_dir
    return e

    

def best_move(board):
    val_max = float('-inf')
    best_action = None

    for action in actions(board):
        copy_board = deepcopy(board)
        copy_board[action[0]][action[1]] = player(board)
        val = minmax(copy_board, depth, maximazing=False)
        if val_max < val:
            val_max = val
            best_action = action

    return best_action

def print_mat(board):
     s = ' '
     for row in board:
        s = ' '
        for col in row:
            s += ' ' + col 
        print(s)
#################

def limpiar_terminal():
    if os.name == 'posix':
        # En sistemas tipo Unix (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':
        # En sistemas Windows
        os.system('cls')
    else:
        # Si el sistema no es compatible, simplemente imprime caracteres de nueva línea para "limpiar" la pantalla
        print('\n' * 100)

if __name__ == "__main__":
    print(main_board)

    while winner(main_board) == None:
        if player(main_board) == 'X':
            best = best_move(main_board)
            print("MINMAX NEW", best)
            main_board[best[0]][best[1]] = player(main_board)
        else:
            i = input('Mov: ').split(' ')
            if i[0] == 'e':
                exit(0)
            main_board = result(main_board, tuple([int(el) for el in i]))
        limpiar_terminal()
        print_mat(main_board)
    else:
        print("FINISH")