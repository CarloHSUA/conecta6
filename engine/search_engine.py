from tools import *
from defines import Defines
from game import Game

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

    # self, depth, alpha, beta, ourColor, bestMove, preMove
    def alfa_beta(self, game:Game, board, player, depth):
        
        score = 0
        positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val != Defines.BORDER and val != Defines.NOSTONE}
        if len(positions) == 0:
            best_move = StoneMove()
            best_move.positions[0].x = jugada1[0]
            best_move.positions[0].y = jugada1[1]
            return score, best_move

        depth = 1
        print(board, player, depth, 1, game.weights)

        jugada1, jugada2 =  game.choose_best_move(board, player, depth, 1, game.weights)

        print(jugada1, jugada2)

        if jugada1 == (None,None) and jugada2 == (None,None):
            print_board(board)
        else:

            best_move = StoneMove()
            best_move.positions[0].x = jugada1[0]
            best_move.positions[0].y = jugada1[1]
            best_move.positions[1].x = jugada2[0]
            best_move.positions[1].y = jugada2[1]

        
        return score, best_move

    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
        
        opponent = get_opponent(self.m_chess_type)
        if depth == 0 or has_won(self.m_board, self.m_chess_type) or has_won(self.m_board, opponent):
            return evaluate_advanced(self.m_board, action, player, self.all_positions, w_player)
        
        valid_moves = actions(self.m_board, {action}, player)
        if ourColor == self.m_chess_type:
            value = float('-inf')
            for move in valid_moves:
                new_actions = all_actions.union({move})
        else:
            value = float('inf')
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
        else:   
            move1 = self.find_possible_move()
            bestMove.positions[0].x = move1[0]
            bestMove.positions[0].y = move1[1]
            bestMove.positions[1].x = move1[0]
            bestMove.positions[1].y = move1[1]
            make_move(self.m_board,bestMove,ourColor)
            
            '''#Check game result
            if (is_win_by_premove(self.m_board, bestMove)):
                #Self wins.
                return Defines.MININT + 1;'''
            
            move2 = self.find_possible_move()
            bestMove.positions[1].x = move2[0]
            bestMove.positions[1].y = move2[1]
            make_move(self.m_board,bestMove,ourColor)

        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] == Defines.NOSTONE):
                    return (i,j)
        return (-1,-1)
    # Función de heurística avanzada



def flush_output():
    import sys
    sys.stdout.flush()
