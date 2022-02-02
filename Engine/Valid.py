class BoardState():
    def __init__(self):
        # Plansza 8x8, lista 2d, czarne figury oznaczone są małymi literami, białe figury oznaczone są wielkimi literami
        # R/r - wieża, N/n - skoczek, B/b - goniec, Q/q - królowa, K/k - król, "_" - puste pole
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_", "_", "_", "_"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]]

        self.moveFunctions = {}
        self.moveLog = []
        self.whiteToMove = True
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "_"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece_moved == "K":
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == "k":
            self.black_king_location = (move.end_row, move.end_column)

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.whiteToMove = not self.whiteToMove
            if move.piece_moved == "K":
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == "k":
                self.black_king_location = (move.start_row, move.start_column)

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def in_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, column):
        self.whiteToMove = not self.whiteToMove
        opponent_moves = self.get_all_possible_moves()
        self.whiteToMove = not self.whiteToMove
        for move in opponent_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                piece = self.board[row][column][0]
                if (piece.isupper() and self.whiteToMove) or (piece.islower() and not self.whiteToMove):
                    if piece == "p" or piece == "P":
                        self.get_pawn_moves(row, column, moves)
                    elif piece == "r" or piece == "R":
                        self.get_rook_moves(row, column, moves)
                    elif piece == "n" or piece == "N":
                        self.get_knight_moves(row, column, moves)
                    elif piece == "b" or piece == "B":
                        self.get_bishop_moves(row, column, moves)
                    elif piece == "q" or piece == "Q":
                        self.get_queen_moves(row, column, moves)
                    elif piece == "k" or piece == "K":
                        self.get_king_moves(row, column, moves)
        return moves

    def get_pawn_moves(self, row, column, moves):
        if self.whiteToMove:
            if self.board[row - 1][column] == "_":
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "_":
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1].islower():
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1].islower():
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
        else:
            if self.board[row + 1][column] == "_":
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "_":
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1].isupper():
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1].isupper():
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_column = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "_":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif self.whiteToMove and end_piece.islower():
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    elif not self.whiteToMove and end_piece.isupper():
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, column, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = row + m[0]
            end_column = column + m[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if self.whiteToMove and not end_piece.isupper():
                    moves.append(Move((row, column), (end_row, end_column), self.board))
                elif not self.whiteToMove and not end_piece.islower():
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_column = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "_":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif self.whiteToMove and end_piece.islower():
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    elif not self.whiteToMove and end_piece.isupper():
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, column, moves):
        self.get_bishop_moves(row, column, moves)
        self.get_rook_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        king_moves = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_column = column + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if self.whiteToMove and not end_piece.isupper():
                    moves.append(Move((row, column), (end_row, end_column), self.board))
                elif not self.whiteToMove and not end_piece.islower():
                    moves.append(Move((row, column), (end_row, end_column), self.board))


class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3,
                        "e": 4, "f": 5, "g": 6, "h": 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)
