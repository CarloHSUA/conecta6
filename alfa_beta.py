def player(board):
    count_X = sum(row.count("X") for row in board)
    count_O = sum(row.count("O") for row in board)
    if count_X <= count_O:
        return "X"
    else:
        return "O"

def actions(board):
    possible_moves = set()
    for i in range(19):
        for j in range(19):
            if board[i][j] == "-":
                possible_moves.add((i, j))
    return possible_moves

def result(board, action):
    i, j = action
    if board[i][j] != "-":
        raise ValueError("Invalid move")
    player_turn = player(board)
    new_board = [row[:] for row in board]
    new_board[i][j] = player_turn
    return new_board

# def winner(board):
#     for i in range(3):
#         if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
#             return board[i][0]
#         if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "-":
#             return board[0][i]

#     if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
#         return board[0][0]
#     if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
#         return board[0][2]

#     return None

def terminal(board, current_player):
    return winner(board, current_player) is not None or "-" not in [cell for row in board for cell in row]

def utility(board):
    winner_player = winner(board)
    if winner_player == "X":
        return 1000
    elif winner_player == "O":
        return -1000
    else:
        return heuristic(board)

def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == "X":
        best_value = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_move = action
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move
    else:
        best_value = float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_move = action
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -float("inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 19)
        

def heuristic(board):
        # Valor base
    score = 0

    # Evaluación de filas, columnas y diagonales
    for i in range(3):
        row = board[i]
        col = [board[j][i] for j in range(3)]
        if row.count("X") == 2 and row.count("-") == 1:
            score += 10
        if col.count("X") == 2 and col.count("-") == 1:
            score += 10
        if row.count("O") == 2 and row.count("-") == 1:
            score -= 10
        if col.count("O") == 2 and col.count("-") == 1:
            score -= 10

    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2 - i] for i in range(3)]

    if diag1.count("X") == 2 and diag1.count("-") == 1:
        score += 10
    if diag2.count("X") == 2 and diag2.count("-") == 1:
        score += 10
    if diag1.count("O") == 2 and diag1.count("-") == 1:
        score -= 10
    if diag2.count("O") == 2 and diag2.count("-") == 1:
        score -= 10

    # Evaluación de esquinas
    corners = [board[0][0], board[0][2], board[2][0], board[2][2]]
    if corners.count("X") == 1 and corners.count("-") == 3:
        score += 5
    if corners.count("O") == 1 and corners.count("-") == 3:
        score -= 5

    # Evaluación del centro
    if board[1][1] == "X":
        score += 2
    elif board[1][1] == "O":
        score -= 2

    return score    

#Comprueba si ha ganado algún jugador
def winner(board, player):
    # Verificar victoria horizontal
    for row in board:
        if ''.join(row).count(player * 6) > 0:
            return player

    # Verificar victoria vertical
    for col in range(len(board[0])):
        column = ''.join([row[col] for row in board])
        if column.count(player * 6) > 0:
            return player

    # Verificar victoria en diagonal (ascendente)
    for i in range(len(board) - 5):
        for j in range(len(board[0]) - 5):
            diagonal = ''.join([board[i + k][j + k] for k in range(6)])
            if diagonal.count(player * 6) > 0:
                return player

    # Verificar victoria en diagonal (descendente)
    for i in range(len(board) - 5):
        for j in range(5, len(board[0])):
            diagonal = ''.join([board[i + k][j - k] for k in range(6)])
            if diagonal.count(player * 6) > 0:
                return player

    return None
        

# Función main para bucle de juego
def main():
    # Inicializa el tablero
    board = [
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
        ["-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-", "-", "-","-"],
    ]

    # Define al jugador actual
    current_player = "X"

    print("¡Bienvenido al juego de Tic-Tac-Toe!")

    while True:
        # Imprime el tablero actual
        print_board(board)

        # Verifica si el juego ha terminado
        if terminal(board,current_player):
            winner_player = winner(board, current_player)
            if winner_player:
                print(f"¡El jugador {winner_player} ha ganado!")
            else:
                print("¡Es un empate!") 
            break

        # Turno del jugador humano
        if current_player == "X":
            row = int(input("Ingrese el número de fila (0-18): "))
            column = int(input("Ingrese el número de columna (0-18): "))

            if (row, column) not in actions(board):
                print("Movimiento inválido. Intente de nuevo.")
                continue

            board = result(board, (row, column))
        else:
            # Turno de la IA (usando el algoritmo minimax)
            print("Turno de la IA (O)...")
            best_move = minimax(board)
            board = result(board, best_move)

        # Cambia al siguiente jugador
        current_player = "X" if current_player == "O" else "O"

    print("¡Gracias por jugar!")

if __name__ == "__main__":
    main()