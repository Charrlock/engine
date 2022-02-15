import pygame as p
import chess
import Valid
import Engine
from multiprocessing import Process, Queue

p.init()

WIDTH = 480
HEIGHT = 480
DIMENSIONS = 8
SQUARE_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 12
IMAGE = {}
MOVE_LOG_PANEL_WIDTH = 320
MOVE_LOG_PANEL_HEIGHT = HEIGHT


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
    text_object = font.render(text, False, p.Color('Black'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)


def draw_move_log(screen, game_state, font):
    move_log_area = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("Grey"), move_log_area)
    move_log = game_state.moveLog
    move_texts = move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i//2 + 1) + ". " + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i+1]) + "  "
        move_texts.append(move_string)
    moves_per_row = 4
    padding = 5
    line_spacing = 2
    textY = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i+j]
        text_object = font.render(text, True, p.Color('Black'))
        text_location = move_log_area.move(padding, textY)
        screen.blit(text_object, text_location)
        textY += text_object.get_height() + line_spacing


def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
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
    ai_thinking = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Helvetica", 12, False, False)
    move_undone = False
    while running:
        human_turn = (game_state.whiteToMove and player_white) or ( not game_state.whiteToMove and player_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    mouse_position = p.mouse.get_pos()
                    row = mouse_position[1]//SQUARE_SIZE
                    column = mouse_position[0]//SQUARE_SIZE
                    if square_selected == (row, column) or column >= 8:
                        square_selected = ()
                        clicks = []
                    else:
                        square_selected = (row, column)
                        clicks.append(square_selected)
                    if len(clicks) == 2 and human_turn:
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
                    square_selected = ()
                    clicks = []
                    move_made = True
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

                    if not player_white and not player_black:
                        game_state.undo_move()
                if e.key == p.K_r:
                    game_state = Valid.BoardState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    clicks = []
                    move_made = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()
                move_finder_process = Process(target=Engine.find_best_move, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()
            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = Engine.find_random_move(valid_moves)
                game_state.make_move(ai_move)
                move_made = True
                ai_thinking = False

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False
            move_undone = False

        draw_board(screen, game_state.board)
        highlight_squares(screen, game_state, valid_moves, square_selected)
        draw_move_log(screen, game_state, move_log_font)

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
