import os
import sys
import numpy as np
from rich import print
from copy import deepcopy


main_board = [['X', '-', '-'],
              ['-', '-', '-'],
              ['-', '-', '-']]

X_positions = set()
X_positions.add((1,1))
O_positions = set()

# Se puede elegir el jugador con el modulo de una variable, si es par uno y si es impar el otro jugador
turn = 0
limit = 3

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
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not '-':
            return board[i][0]
        
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not '-':
            return board[0][i]
        
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] is not '-':
        return board[1][1]
    
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] is not '-':
        return board[1][1]
    
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


def minmax(board, maximazing = True):
    '''
    Input es el tablero del juego
    Devuelve la jugada optima por el jugador
    '''
    if terminal(board):
        return utility(board)
    if maximazing:
        v = float('-inf')
        for action in actions(board):
            v = max(v, minmax(result(board, action), False))
        return v
    else:
        v = float('inf')
        for action in actions(board):
            v = min(v, minmax(result(board, action), True))
        return v


#################

def minimax2(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == 'X':
        return __max_value(board)[1]
    if player(board) == 'O':
        return __min_value(board)[1]
    raise NotImplementedError

def __max_value(board):
    if terminal(board):
        return (utility(board), None)
    v = float('-inf')
    best_action: dict = {}
    for action in actions(board):
        v = max(v, __min_value(result(board, action))[0])
        best_action[action] = v
        # print("ACTION:", action, v)


    return (v, max(best_action.items(), key=lambda x: x[1])[0])

def __min_value(board):
    if terminal(board):
        return (utility(board), None)
    v = float('inf')
    best_action: dict = {}

    for action in actions(board):
        v = min(v, __max_value(result(board, action))[0])
        best_action[action] = v
        #print("ACTION:", action, v)

    return (v, min(best_action.items(), key=lambda x: x[1])[0])

#################

def mejor_movimiento(board, jugador):

    mejor_valor = float('-inf')
    mejor_mov = None
    s = ' '
    for fila in range(3):
        s = ' '
        for columna in range(3):
            if board[fila][columna] == '-':
                board[fila][columna] = jugador
                valor = minmax(board)
                s = s + str(valor) + ' ' 
                board[fila][columna] = '-'  # Deshacer el movimiento

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_mov = (fila, columna)
            else: 
                s = s + '-' + ' '
        # print(s)

    return mejor_mov

def print_mat(board):
     s = ' '
     for row in board:
        s = ' '
        for col in row:
            s += col 
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

# Llamar a la función para limpiar la terminal
limpiar_terminal()

if __name__ == "__main__":
    print(main_board)

    while winner(main_board) == None:
        if player(main_board) == 'X':
            # Revisar el funcionamiento del nuevo minmax y la siguiente function
            t = mejor_movimiento(main_board, player(main_board))
            best = minimax2(main_board)
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
    
    
