import random

piece_values = {"K": 60000, "k": 60000,
                "Q": 900, "q": 900,
                "R": 500, "r": 500,
                "B": 315, "b": 315,
                "N": 300, "n": 300,
                "P": 100, "p": 100}
DEPTH = 4


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]


def find_best_move(game_state, valid_moves):
    turn_multiplier = 1 if game_state.whiteToMove else -1
    opponent_min_max_score = float('inf')
    best_player_move = None
    for player_move in valid_moves:
        game_state.make_move(player_move)
        opponent_moves = game_state.get_valid_moves()
        opponent_max_score = float('-inf')
        for opponent_move in opponent_moves:
            game_state.make_move(opponent_move)
            if game_state.checkmate:
                score = - turn_multiplier * float('inf')
            elif game_state.stalemate:
                score = 0
            else:
                score = - turn_multiplier * score_material(game_state.board)
            if score > opponent_max_score:
                opponent_max_score = score
            game_state.undo_move()
        if opponent_max_score > opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        game_state.undo_move()
    return best_player_move


def find_min_max_move(game_state, valid_moves, depth, whiteToMove):
    global next_move
    if depth == 0:
        return score_material(game_state.board)


def score_board


def find_best_min_max_move(game_state, valid_moves):
    global next_move
    next_move = None
    find_min_max_move(game_state, valid_moves, DEPTH, game_state.whiteToMove)
    return next_move


def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square.isupper():
                score += piece_values[square]
            elif square.islower():
                score -= piece_values[square]

    return score
