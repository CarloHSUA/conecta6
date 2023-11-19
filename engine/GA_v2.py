from window_search import *
import random
from rich import print

NUM_PLAYERS = 16

# Creación inicial de pesos para la población
initial_population_X = [3, 5, 4, 3, 2, 1, 3, 5, 4, 10**20, 10**25, 0.5] # [random.uniform(-1, 1) for _ in range(11)]  
initial_population_O = [3, 5, 4, 3, 2, 1, 3, 5, 4, 10**20, 10**25, 0.5] # [random.uniform(-1, 1) for _ in range(11)]  

# Función para generar una variante de lista de pesos a partir de una inicial
def generate_variant_weights(initial_weights):
    variant_weights = [weight + random.uniform(-0.5, 0.5) for weight in initial_weights]
    return variant_weights

# Función para mutar una lista de pesos
def mutate_weights(weights, mutation_rate=0.1):
    mutated_weights = [weight + random.uniform(-0.5, 0.5) if random.uniform(0, 1) < mutation_rate else weight for weight in weights]
    return mutated_weights

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
    return winners

# Función para realizar el torneo y evolucionar los pesos
def evolve_weights_tournament(initial_population_X, initial_population_O, num_generations):
    variant_weights_X_list = [initial_population_X[:] for _ in range(NUM_PLAYERS)]
    variant_weights_O_list = [initial_population_O[:] for _ in range(NUM_PLAYERS)]

    for generation in range(num_generations):
        print(f'Generación {generation + 1}')

        # Evaluar los pesos actuales en el torneo
        tournament_winners = evaluate_weights(variant_weights_X_list, variant_weights_O_list)

        # TODO: Falta sacar el mejor del torneo anterior y aplicarle todo lo de abajo 

        # Evolucionar los pesos para la siguiente generación
        new_variant_weights_X_list = []
        new_variant_weights_O_list = []

        for weights_X, weights_O in zip(variant_weights_X_list, variant_weights_O_list):
            # Aplicar mutación a los pesos
            mutated_weights_X = mutate_weights(weights_X)
            mutated_weights_O = mutate_weights(weights_O)

            # Generar variantes a partir de los pesos mutados
            variant_weights_X = generate_variant_weights(mutated_weights_X)
            variant_weights_O = generate_variant_weights(mutated_weights_O)

            new_variant_weights_X_list.append(variant_weights_X)
            new_variant_weights_O_list.append(variant_weights_O)

        # Reemplazar los pesos antiguos con los nuevos para la siguiente generación
        variant_weights_X_list = new_variant_weights_X_list
        variant_weights_O_list = new_variant_weights_O_list

    # Retornar los ganadores finales
    return tournament_winners

# Ejecutar el torneo y evolución de pesos
final_winners = evolve_weights_tournament(initial_population_X, initial_population_O, num_generations=10)

print("BEST WEIGHTS -> ", final_winners)