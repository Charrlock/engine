import pygame as p
import chess
import Valid
import Engine

p.init()

WIDTH = 480
HEIGHT = 480
DIMENSIONS = 8
SQUARE_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 12
IMAGE = {}


def load_images():
    IMAGE["r"] = p.transform.scale(p.image.load("images/br.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["n"] = p.transform.scale(p.image.load("images/bn.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["b"] = p.transform.scale(p.image.load("images/bb.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["q"] = p.transform.scale(p.image.load("images/bq.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["k"] = p.transform.scale(p.image.load("images/bk.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["p"] = p.transform.scale(p.image.load("images/bp.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["R"] = p.transform.scale(p.image.load("images/wR.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["N"] = p.transform.scale(p.image.load("images/wN.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["B"] = p.transform.scale(p.image.load("images/wB.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["Q"] = p.transform.scale(p.image.load("images/wQ.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["K"] = p.transform.scale(p.image.load("images/wK.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGE["P"] = p.transform.scale(p.image.load("images/wP.png"), (SQUARE_SIZE, SQUARE_SIZE))


def highlight_squares(screen, game_state, valid_moves, square_selected):
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column].isupper() if game_state.whiteToMove else game_state.board[row][column].islower():
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(30)
            s.fill(p.Color("darkslateblue"))
            screen.blit(s, (column*SQUARE_SIZE, row*SQUARE_SIZE))
            s.fill(p.Color("navy"))
            for move in valid_moves:
                if move.start_row == row and move.start_column == column:
                    screen.blit(s, (move.end_column*SQUARE_SIZE, move.end_row*SQUARE_SIZE))


def draw_board(screen, board):
    colors = [p.Color("light grey"), p.Color("dark grey")]
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][column]
            if piece != "_":
                screen.blit(IMAGE[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, True)
    text_object = font.render(text, 0, p.Color('Black'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
    load_images()
    clock = p.time.Clock()
    game_state = Valid.BoardState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    square_selected = ()
    clicks = []
    running = True
    game_over = False
    player_white = True
    player_black = False
    while running:
        human_turn = (game_state.whiteToMove and player_white) or ( not game_state.whiteToMove and player_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    mouse_position = p.mouse.get_pos()
                    row = mouse_position[1]//SQUARE_SIZE
                    column = mouse_position[0]//SQUARE_SIZE
                    if square_selected == (row, column):
                        square_selected = ()
                        clicks = []
                    else:
                        square_selected = (row, column)
                        clicks.append(square_selected)
                    if len(clicks) == 2:
                        move = Valid.Move(clicks[0], clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                square_selected = ()
                                clicks = []
                        if not move_made:
                            clicks = [square_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game_state.undo_move()
                    game_state.undo_move()
                    move_made = True
                if e.key == p.K_r:
                    game_state = Valid.BoardState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    clicks = []
                    move_made = False
                    game_over = False

        if not game_over and not human_turn:
            ai_move = Engine.find_best_min_max_move(game_state, valid_moves)
            if ai_move is None:
                ai_move = Engine.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_board(screen, game_state.board)
        highlight_squares(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            game_over = True
            if game_state.whiteToMove:
                draw_text(screen, "0-1 black wins")
            else:
                draw_text(screen, "1-0 white wins")
        elif game_state.stalemate:
            game_over = True
            draw_text(screen, "1/2-1/2 draw")

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
