import random

piece_values = {"K": 60000, "k": 60000,
                "Q": 900, "q": 900,
                "R": 500, "r": 500,
                "B": 315, "b": 315,
                "N": 300, "n": 300,
                "P": 100, "p": 100}

white_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [78, 83, 86, 73, 102, 82, 85, 90],
                     [7, 29, 21, 44, 40, 31, 44, 7],
                     [-17, 16, -2, 15, 14, 0, 15, -13],
                     [-26, 3, 10, 9, 6, 1, 0, -23],
                     [-22, 9, 5, -11, -10, -2, 3, -19],
                     [-31, 8, -7, -37, -36, -14, 3, -31],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [-31, 8, -7, -37, -36, -14, 3, -31],
                     [-22, 9, 5, -11, -10, -2, 3, -19],
                     [-26, 3, 10, 9, 6, 1, 0, -23],
                     [-17, 16, -2, 15, 14, 0, 15, -13],
                     [7, 29, 21, 44, 40, 31, 44, 7],
                     [78, 83, 86, 73, 102, 82, 85, 90],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

white_knight_scores = [[-66, -53, -75, -75, -10, -55, -58, -70],
                       [-3, -6, 100, -36, 4, 62, -4, -14],
                       [10, 67, 1, 74, 73, 27, 62, -2],
                       [24, 24, 45, 37, 33, 41, 25, 17],
                       [-1, 5, 31, 21, 22, 35, 2, 0],
                       [-18, 10, 13, 22, 18, 15, 11, -14],
                       [-23, -15, 2, 0, 2, 0, -23, -20],
                       [-74, -23, -26, -24, -19, -35, -22, -69]]

white_bishop_scores = [[-59, -78, -82, -76, -23, -107, -37, -50],
                       [-11, 20, 35, -42, -39, 31, 2, -22],
                       [-9, 39, -32, 41, 52, -10, 28, -14],
                       [25, 17, 20, 34, 26, 25, 15, 10],
                       [13, 10, 17, 23, 17, 16, 0, 7],
                       [14, 25, 24, 15, 8, 25, 20, 15],
                       [19, 20, 11, 6, 7, 6, 20, 16],
                       [-7, 2, -15, -12, -14, -15, -10, -10]]

white_rook_scores = [[35, 29, 33, 4, 37, 33, 56, 50],
                     [55, 29, 56, 67, 55, 62, 34, 60],
                     [19, 35, 28, 33, 45, 27, 25, 15],
                     [0, 5, 16, 13, 18, -4, -9, -6],
                     [-28, -35, -16, -21, -13, -29, -46, -30],
                     [-42, -28, -42, -25, -25, -35, -26, -46],
                     [-53, -38, -31, -26, -29, -43, -44, -53],
                     [-30, -24, -18, 5, -2, -18, -31, -32]]

white_queen_scores = [[6, 1, -8, -104, 69, 24, 88, 26],
                      [14, 32, 60, -10, 20, 76, 57, 24],
                      [-2, 43, 32, 60, 72, 63, 43, 2],
                      [1, -16, 22, 17, 25, 20, -13, -6],
                      [-14, -15, -2, -5, -1, -10, -20, -22],
                      [-30, -6, -13, -11, -16, -11, -16, -27],
                      [-36, -18, 0, -19, -15, -15, -21, -38],
                      [-39, -30, -31, -13, -31, -36, -34, -42]]

white_king_early_scores = [[4, 54, 47, -99, -99, 60, 83, -62],
                           [-32, 10, 55, 56, 56, 55, 10, 3],
                           [-62, 12, -57, 44, -67, 28, 37, -31],
                           [-55, 50, 11, -4, -19, 13, 0, -49],
                           [-55, -43, -52, -28, -51, -47, -8, -50],
                           [-47, -42, -43, -79, -64, -32, -29, -32],
                           [-4, 3, -14, -50, -57, -18, 13, 4],
                           [17, 30, -3, -14, 6, -1, 40, 18]]

white_king_late_scores = [[-66, -53, -75, -75, -10, -55, -58, -70],
                          [-3, -6, 100, -36, 4, 62, -4, -14],
                          [10, 67, 1, 74, 73, 27, 62, -2],
                          [24, 24, 45, 37, 33, 41, 25, 17],
                          [-1, 5, 31, 21, 22, 35, 2, 0],
                          [-18, 10, 13, 22, 18, 15, 11, -14],
                          [-23, -15, 2, 0, 2, 0, -23, -20],
                          [-74, -23, -26, -24, -19, -35, -22, -69]]

DEPTH = 2


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move_worse(game_state, valid_moves):
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

    if whiteToMove:
        max_score = float('-inf')
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_min_max_move(game_state, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undo_move()
        return max_score
    else:
        min_score = float('inf')
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = find_min_max_move(game_state, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undo_move()
        return min_score


def find_best_move(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_move_nega_max_alpha_beta(game_state, valid_moves, DEPTH, float('-inf'), float('inf'),
                                  1 if game_state.whiteToMove else -1)
    return next_move


def find_move_nega_max(game_state, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_material(game_state.board)

    max_score = float('-inf')
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max(game_state, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
    return max_score


def find_move_nega_max_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = float('-inf')
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def score_board(game_state):
    if game_state.checkmate:
        if game_state.whiteToMove:
            return float('-inf')
        else:
            return float('inf')
    elif game_state.stalemate:
        return 0

    score = 0
    for row in game_state.board:
        for square in row:
            if square.isupper():
                score += piece_values[square]
            elif square.islower():
                score -= piece_values[square]
    return score


def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square.isupper():
                score += piece_values[square]
            elif square.islower():
                score -= piece_values[square]

    return score
