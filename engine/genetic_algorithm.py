# from window_search import *
import random
from rich import print
from game import Game
import concurrent.futures

NUM_PLAYERS = 32

# Creación inicial de pesos para la población
population_size = 20
w = [
        5, 4, 3, 2, 1,     # w
        3,                 # final_val_weight
        5,                 # enemy_busy_places_weight (int)
        0.5,               # val_weight
        20                 # N_best_moves_weight (int)
        ]

g = Game(depth = 3,
             weights = w,
             size = (21,21),
             time_limit = 15,
             have_border=True,
             border = '$',
             empty = '-',
             player_black = 'X',
             player_white = 'O')

initial_population_X = w # [random.uniform(-1, 1) for _ in range(11)]  
initial_population_O = w # [random.uniform(-1, 1) for _ in range(11)]  


# Función para generar una variante de lista de pesos a partir de una inicial
def generate_variant_weights(initial_weights):
    # variant_weights = [weight + random.uniform(-0.5, 0.5) for weight in initial_weights]
    variant_weights = []
    for idx, weight in enumerate(initial_weights):
        if idx == 6:
            random_num = weight + random.randint(-2, 2)
        elif idx == 8:
            random_num = weight + random.randint(-10, 10)
        else:
            random_num = weight + random.uniform(-0.5, 0.5)
            
        variant_weights.append(random_num)
    return variant_weights

# Generar variantes de estas listas de pesos para el torneo
variant_weights_X_list = [generate_variant_weights(initial_population_X) for _ in range(NUM_PLAYERS)]
variant_weights_O_list = [generate_variant_weights(initial_population_O) for _ in range(NUM_PLAYERS)]

# Función para evaluar el rendimiento de los pesos en el juego de Connect 6
def evaluate_weights(w_player_X_list, w_player_O_list):
    # Lógica para enfrentar los motores de IA con sus respectivas listas de pesos
    # Devuelve una lista de ganadores de cada enfrentamiento
    winners = []
    for weights_X, weights_O in zip(w_player_X_list, w_player_O_list):
        winner = g.play_connect6(weights_X, weights_O)
        if winner == 'X':
            winners.append(weights_X)
        elif winner == 'O':
            winners.append(weights_O)
    #winners = [(play_connect6(weights_X, weights_O)) for weights_X, weights_O in zip(w_player_X_list, w_player_O_list)]
    return winners

def evaluate_weights_parallel(w_player_X_list, w_player_O_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Lógica para enfrentar los motores de IA con sus respectivas listas de pesos
        # Devuelve una lista de ganadores de cada enfrentamiento
        future_results = {
            executor.submit(g.play_connect6, weights_X, weights_O): (weights_X, weights_O)
            for weights_X, weights_O in zip(w_player_X_list, w_player_O_list)
        }
        winners = []
        for future in concurrent.futures.as_completed(future_results):
            weights_X, weights_O = future_results[future]
            winner = future.result()
            if winner == 'X':
                winners.append(weights_X)
            elif winner == 'O':
                winners.append(weights_O)
    return winners


# Realizar el torneo
# tournament_winners = evaluate_weights(variant_weights_X_list, variant_weights_O_list)
tournament_winners = evaluate_weights_parallel(variant_weights_X_list, variant_weights_O_list)

count = 1
while len(tournament_winners) > 1:
    print(f'RONDA {count}')
    count += 1
    mitad_1 = tournament_winners[:len(tournament_winners)//2]
    mitad_2 = tournament_winners[len(tournament_winners)//2:]
    tournament_winners = evaluate_weights_parallel(mitad_1, mitad_2)

print("BEST WEIGHT -> ", tournament_winners)

# Ahora tournament_winners contiene una lista con los ganadores de cada enfrentamiento en el torneo

print('Final fight')
print('Weights player', tournament_winners[0])
print('Weights opponent', w)

g.play_connect6(tournament_winners[0], w, verbose = True)