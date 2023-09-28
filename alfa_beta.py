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
    
    # if count_moves_X == 0:
    #     return "X"
    if count_moves_X <= count_moves_O:
        return "X"
    else:
        return "O"

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


def alfa_beta_search(board):
    pass
    
    
def main():
    print(player(BOARD))
    
main()