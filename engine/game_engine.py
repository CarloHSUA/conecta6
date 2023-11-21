from defines import *
from tools import *
from game import Game
import sys
from search_engine import SearchEngine
import time
from rich import print

class GameEngine:
    def __init__(self, name=Defines.ENGINE_NAME):
        if name and len(name) > 0:
            if len(name) < Defines.MSG_LENGTH:
                self.m_engine_name = name
            else:
                print(f"Too long Engine Name: {name}, should be less than: {Defines.MSG_LENGTH}")
        self.m_alphabeta_depth = 6
        self.m_board = t = [ [0]*Defines.GRID_NUM for i in range(Defines.GRID_NUM)]
        self.init_game()
        self.m_search_engine = SearchEngine()
        self.m_best_move = StoneMove()
        self.game = Game(depth = 1,
                    weights = [
                            # 3,
                               5, 4, 3, 2, 1, 
                               3,             
                               4,
                               0.5,             
                            #    4,             
                            #    10**20,        
                            #    10**25
                               ],
                    size = (21,21),
                    have_border=True,
                    border = 3,
                    empty = 0,
                    player_black = 1,
                    player_white = 2)

    def init_game(self):
        init_board(self.m_board)

    def on_help(self):
        print(
            f"On help for GameEngine {self.m_engine_name}\n"
            " name        - print the name of the Game Engine.\n"
            " print       - print the board.\n"
            " exit/quit   - quit the game.\n"
            " black XXXX  - place the black stone on the position XXXX on the board.\n"
            " white XXXX  - place the white stone on the position XXXX on the board, X is from A to S.\n"
            " next        - the engine will search the move for the next step.\n"
            " move XXXX   - tell the engine that the opponent made the move XXXX,\n"
            "              and the engine will search the move for the next step.\n"
            " new black   - start a new game and set the engine to black player.\n"
            " new white   - start a new game and set it to white.\n"
            " depth d     - set the alpha beta search depth, default is 6.\n"
            " vcf         - set vcf search.\n"
            " unvcf       - set none vcf search.\n"
            " help        - print this help.\n")

    def run(self):
        msg = ""
        self.on_help()
        while True:
            msg = input().strip()
            # log_to_file(msg)
            if msg == "name":
                print(f"name {self.m_engine_name}")
            elif msg == "exit" or msg == "quit":
                break
            elif msg == "print":
                print_board(self.m_board, self.m_best_move)
            elif msg == "vcf":
                self.m_vcf = True
            elif msg == "unvcf":
                self.m_vcf = False
            elif msg.startswith("black"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.BLACK)
                self.m_chess_type = Defines.BLACK
            elif msg.startswith("white"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.WHITE)
                self.m_chess_type = Defines.WHITE
            elif msg == "next":

                ### OUR CODE START HERE ###
                self.m_chess_type = self.m_chess_type ^ 3
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    # make_move(self.m_board, self.m_best_move, self.m_chess_type)
                    msg = f"move {move2msg(self.m_best_move)}"
                    print(msg)
                    flush_output()
                ### OUR CODE END HERE ###
                



                #########################
                
            elif msg.startswith("new"):
                self.init_game()
                if msg[4:] == "black":
                    self.m_best_move = msg2move("JJ")
                    make_move(self.m_board, self.m_best_move, Defines.BLACK)
                    self.m_chess_type = Defines.BLACK
                    msg = "move JJ"
                    print(msg)
                    flush_output()
                else:
                    self.m_chess_type = Defines.WHITE
            elif msg.startswith("move"):
                self.m_best_move = msg2move(msg[5:])
                make_move(self.m_board, self.m_best_move, self.m_chess_type ^ 3)
                if self.game.has_won(self.m_board, self.m_chess_type ^ 3):
                    print(f"PLAYER {self.m_chess_type ^ 3} ha ganado!!!")
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    msg = f"move {move2msg(self.m_best_move)}"
                    print(msg)
                    flush_output()
            elif msg.startswith("depth"):
                d = int(msg[6:])
                if 0 < d < 10:
                    self.m_alphabeta_depth = d
                print(f"Set the search depth to {self.m_alphabeta_depth}.\n")
            elif msg == "help":
                self.on_help()
        return 0

    def search_a_move(self, player, bestMove):
        score = 0
        start = 0
        end = 0
        start = time.perf_counter()
        self.m_search_engine.before_search(self.m_board, self.m_chess_type, self.m_alphabeta_depth)
        
        # TODO #################################
        score, best_move = self.m_search_engine.alfa_beta(self.game, self.m_board, player, self.m_alphabeta_depth)
        self.m_best_move = best_move
        make_move(self.m_board, best_move, player)
        print_board(self.m_board)
        # if self.game.has_won(self.m_board, player):
        #     print(f"PLAYER {player} ha ganado!!!")
        ########################################

        end = time.perf_counter()
        
        print(f"AB Time:\t{end - start:.3f}")
        print(f"Node:\t{self.m_search_engine.m_total_nodes}\n")
        print(f"Score:\t{score:.3f}")
        return True
    
     

def flush_output():
    sys.stdout.flush()

# Create an instance of GameEngine and run the game
if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
