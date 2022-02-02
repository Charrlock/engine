import pygame as p
import chess
import Valid

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


def draw_board(screen, board):
    colors = [p.Color("light grey"), p.Color("dark grey")]
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][column]
            if piece != "_":
                screen.blit(IMAGE[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


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
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                        square_selected = ()
                        clicks = []
                    else:
                        clicks = [square_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game_state.undo_move()
                    move_made = True
        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_board(screen, game_state.board)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
