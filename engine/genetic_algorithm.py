from window_search import *
import random
from rich import print

NUM_PLAYERS = 32

# Creación inicial de pesos para la población
population_size = 20
initial_population_X = [3, 5, 4, 3, 2, 1, 3, 5, 4, 10**20, 10**25, 0.5] # [random.uniform(-1, 1) for _ in range(11)]  
initial_population_O = [3, 5, 4, 3, 2, 1, 3, 5, 4, 10**20, 10**25, 0.5] # [random.uniform(-1, 1) for _ in range(11)]  


# Función para generar una variante de lista de pesos a partir de una inicial
def generate_variant_weights(initial_weights):
    variant_weights = [weight + random.uniform(-0.5, 0.5) for weight in initial_weights]
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
        winner = play_connect6(weights_X, weights_O)
        if winner == 'X':
            winners.append(weights_X)
        elif winner == 'O':
            winners.append(weights_O)
    #winners = [(play_connect6(weights_X, weights_O)) for weights_X, weights_O in zip(w_player_X_list, w_player_O_list)]
    return winners

# Realizar el torneo
tournament_winners = evaluate_weights(variant_weights_X_list, variant_weights_O_list)
count = 1
while len(tournament_winners) > 1:
    print(f'RONDA {count}')
    count += 1
    mitad_1 = tournament_winners[:len(tournament_winners)//2]
    mitad_2 = tournament_winners[len(tournament_winners)//2:]
    tournament_winners = evaluate_weights(mitad_1, mitad_2)

print("BEST WEIGHT -> ", tournament_winners)

# Ahora tournament_winners contiene una lista con los ganadores de cada enfrentamiento en el torneo