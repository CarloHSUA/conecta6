BOARD = [
                ["-","-","-"] ,
                ["-","-","-"] ,
                ["-","-","-"]
            ]
rows = 3
columns = 3

def player(board):
    count_moves_X = 0
    count_moves_O = 0
    for i in range(rows):
        for j in range(columns):
            print(board[i][j])
            if board[i][j] == "X":
                count_moves_X+=1
            if board[i][j] == "O":
                count_moves_O+=1
                
    if count_moves_X <= count_moves_O:
        return "X"
    else:
        return "O"

def actions(board):
    '''
    Return all the possible actions in a given board in a set
    '''
    posible_moves = set()
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == "-":
                posible_moves.add((i,j))
                
    return posible_moves

def result(board, action):
    '''
    Receive a board and an action and return the resulting board
    '''
    # if action
    pass

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "-":
            return board[0][i]

    # Verificar diagonales
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
        return board[0][2]
    
    if all(cell != " " for row in board for cell in row):
        return None
    
    return None

def terminal():
    pass

def utility():
    pass


def alfa_beta_search(board):
    pass
    
    
def main():
    print(player(BOARD))
    
main()