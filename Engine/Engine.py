import random




def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]