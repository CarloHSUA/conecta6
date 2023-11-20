


def tuples_divider(conjunto_tuplas):
    # Calcular la mitad del conjunto
    mitad = len(conjunto_tuplas) // 2

    # Dividir el conjunto en dos partes
    parte_1 = set(list(conjunto_tuplas)[:mitad])
    parte_2 = conjunto_tuplas - parte_1
    return parte_1, parte_2

if __name__ == '__main__':
    tuples_divider()