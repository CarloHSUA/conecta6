# Representación del tablero: 3x3 matriz (lista de listas)
tablero = [[' ' for _ in range(3)] for _ in range(3)]

# Función para imprimir el tablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print(' | '.join(fila))
        print('---------')

# Función para verificar si el tablero está lleno
def tablero_lleno(tablero):
    for fila in tablero:
        if ' ' in fila:
            return False
    return True

# Función para verificar si alguien ha ganado
def ha_ganado(tablero, jugador):
    # Verificar filas
    for fila in tablero:
        if all(simbolo == jugador for simbolo in fila):
            return True

    # Verificar columnas
    for columna in range(3):
        if all(tablero[fila][columna] == jugador for fila in range(3)):
            return True

    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador or \
       tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True

    return False

# Función para calcular el mejor movimiento usando alfa-beta
def mejor_movimiento(tablero, jugador):
    if tablero_lleno(tablero) or ha_ganado(tablero, 'X') or ha_ganado(tablero, 'O'):
        return None

    mejor_valor = float('-inf')
    mejor_mov = None

    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == ' ':
                tablero[fila][columna] = jugador
                valor = -alfa_beta(tablero, 'O', 'X', float('-inf'), float('inf'))
                tablero[fila][columna] = ' '  # Deshacer el movimiento

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_mov = (fila, columna)

    return mejor_mov

# Función de poda alfa-beta (minimax)
def alfa_beta(tablero, jugador_actual, jugador_max, alfa, beta):
    if ha_ganado(tablero, jugador_max):
        return 1
    elif ha_ganado(tablero, get_opponent(jugador_max)):
        return -1
    elif tablero_lleno(tablero):
        return 0

    if jugador_actual == jugador_max:
        valor = float('-inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador_actual
                    valor = max(valor, alfa_beta(tablero, get_opponent(jugador_actual), jugador_max, alfa, beta))
                    tablero[fila][columna] = ' '
                    alfa = max(alfa, valor)
                    if beta <= alfa:
                        break
        return valor
    else:
        valor = float('inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == ' ':
                    tablero[fila][columna] = jugador_actual
                    valor = min(valor, alfa_beta(tablero, get_opponent(jugador_actual), jugador_max, alfa, beta))
                    tablero[fila][columna] = ' '
                    beta = min(beta, valor)
                    if beta <= alfa:
                        break
        return valor

# Función para obtener el oponente
def get_opponent(jugador):
    return 'X' if jugador == 'O' else 'O'

# Juego
jugador_actual = 'X'

while not tablero_lleno(tablero) and not ha_ganado(tablero, 'X') and not ha_ganado(tablero, 'O'):
    if jugador_actual == 'X':
        fila, columna = mejor_movimiento(tablero, 'X')
        tablero[fila][columna] = 'X'
    else:
        fila, columna = map(int, input("Ingresa tu movimiento (fila y columna): ").split())
        if tablero[fila][columna] == ' ':
            tablero[fila][columna] = 'O'
        else:
            print("Movimiento no válido. Intenta de nuevo.")
            continue

    imprimir_tablero(tablero)
    jugador_actual = get_opponent(jugador_actual)

if ha_ganado(tablero, 'X'):
    print("¡Gana X!")
elif ha_ganado(tablero, 'O'):
    print("¡Gana O!")
else:
    print("Empate.")
    