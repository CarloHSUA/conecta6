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
        if depth == 0:
            return evaluate_advanced(self.m_board, action, player, all_actions, w_player):


        '''
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
        '''
        
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

def evaluate_advanced(board, position, player, all_actions, w_player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    
    player_score = 0
    opponent_score = 0
    a = 0

    # print("ALL ACTIONS -------------", all_actions)
    
    if has_won(board, player):
        return float('inf')
    elif has_won(board, opponent):
        return float('-inf')
    else:
        player_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player and (i,j) in all_actions}
        # opponent_positions = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == opponent and (i,j) in all_actions}
        # all_board = {(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == player or val == opponent}
        # print(f"player_positions({player}) -> {player_positions}")
        # print(f"opponent_positions({opponent}) -> {opponent_positions}")
        # Obtenemos el score del Player X
        
        # print("PLAYER ", player, player_positions, ' -----------------------------------------------')
        # print("YEEEE ", all_actions, player_positions)
        for pos in player_positions:
            aux, amenazas = evaluate_star(board, pos, player, w_player)
            player_score += aux
            a += amenazas

        player_score = player_score * (10**(12 * a))

        '''
        if a == 1:
            player_score = player_score * (10**(12 * a))
        if a >= 2:
            print_board(board)
            print(f"AMENZA POTENCIAL {player_positions}")
            player_score = float('inf')
            print(f"{player_score} {len(str(player_score))}\t\t {player_positions} {a}")
            # print_board(board)
            # print("AMENAZAS", a, player_positions, player)
            # player_score = player_score * 1000000000000000**a
        '''

        # if player == 'O':
        #     player_score = - player_score
        
        # print(f"EVALUATE STAR -> {position} {evaluate_star(board, position, player)} {l}" )
        # Obtenemos el score del Player O
        
        # print("OPPONENT ", opponent, opponent_positions, ' -----------------------------------------------')
        # for pos in opponent_positions:
        #     opponent_score += evaluate_star(board, pos, opponent, w_player)
        

        # print(player, position, )
        # player_score = evaluate_star(board, position, player, w_player)
        # print(player, position, '\t', player_score, len(str(player_score)))

    return player_score - opponent_score

def flush_output():
    import sys
    sys.stdout.flush()
