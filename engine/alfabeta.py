import os
import sys
import numpy as np
from rich import print
from copy import deepcopy


main_board = [['-', 'X', '-'],
              ['-', '-', '-'],
              ['-', '-', '-']]

main_board = [['-' for _ in range(8)] for _ in range(8)]
main_board[0][0] = 'X'
X_positions = set()
X_positions.add((1,1))
O_positions = set()

# Se puede elegir el jugador con el modulo de una variable, si es par uno y si es impar el otro jugador
turn = 0
limit = 8
depth = 2

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
        board[action[0]][action[1]] = player(board)
        raise Exception("Index out of bounds")
    copy_board = deepcopy(board)
    copy_board[action[0]][action[1]] = player(board)
    return copy_board


def winner(board):
    '''
    Input board
    Output 'X' or 'O'
    '''
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
    return (winner(board) is not None or all(all(cell != '-' for cell in row) for row in board))

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
    
def max_value(board, alpha, beta, depth):
    if terminal(board) or depth == 0:
        return utility(board)
    v = -float("inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta, depth-1))
        # alpha = max(alpha, v)
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v

def min_value(board, alpha, beta, depth):
    if terminal(board) or depth == 0:
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta, depth-1))
        if v <= alpha:   
            return v
        beta = min(beta, v)
    return v
    
def alfabeta(board, depth):
    if terminal(board):
        return None

    current_player = player(board)
    
    if current_player == "X":
        alpha = -float("inf")
        beta = float("inf")
        best_value = -float("inf")
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta, depth)
            if value > best_value:
                best_value = value
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float("inf")
        alpha = -float("inf")
        beta = float("inf")
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta, depth)
            if value < best_value:
                best_value = value
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def best_move(board):
    val_max = float('-inf')
    best_action = None

    for action in actions(board):
        copy_board = deepcopy(board)
        copy_board[action[0]][action[1]] = player(board)
        val = alfabeta(copy_board, depth)
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
            # best = alfabeta(main_board,depth)
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