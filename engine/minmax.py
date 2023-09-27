import numpy as np
from rich import print


board = [['-', 'X', '-'],
         ['-', 'O', '-'],
         ['-', 'X', '-']]

def player():
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
    
def actions():
    pass

def result():
    pass

def winner():
    pass

def terminal():
    pass

def utility():
    pass

def minmax():
    '''
    Input es el tablero del juego
    Devuelve la jugada optima por el jugador
    '''
    pass

if __name__ == "__main__":
    print(board)
    print(player())
