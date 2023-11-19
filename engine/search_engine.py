from tools import *

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

    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
    
        #Check game result
        if (is_win_by_premove(self.m_board, preMove)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return -1
            else:
                #Self wins.
                return 1
        if depth == 0:
            # Evaluar la posición actual si alcanzamos la profundidad máxima
            return evaluate_position(self.m_board, ourColor)
        possible_moves = generate_moves(self.m_board, ourColor)
        
        if ourColor == self.m_chess_type:  # Nuestro turno (Maximizar)
            value = float('-inf')
            for move in possible_moves:
                make_move(self.m_board, move, ourColor)
                value = max(value, self.alpha_beta_search(depth - 1, alpha, beta, opponent_color(ourColor), move))
                unmake_move(self.m_board, move, ourColor)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Podemos podar el árbol
            return value
        else:  # Turno del oponente (Minimizar)
            value = float('inf')
            for move in possible_moves:
                make_move(self.m_board, move, ourColor)
                value = min(value, self.alpha_beta_search(depth - 1, alpha, beta, opponent_color(ourColor), move))
                unmake_move(self.m_board, move, ourColor)
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Podemos podar el árbol
            return value
        
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

def flush_output():
    import sys
    sys.stdout.flush()
