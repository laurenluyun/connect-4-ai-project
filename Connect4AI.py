import numpy as np
import random

class Connect4AI:
    def __init__(self, game):
        self.game = game

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def score_position(self, piece):
        score = 0
        center_column = [int(self.game.board[r][self.game.num_columns // 2]) for r in range(self.game.num_rows)]
        # encourage central column play
        score += center_column.count(piece) * 6

        for r in range(self.game.num_rows):
            row_array = list(self.game.board[r, :])
            for c in range(self.game.num_columns - 3):
                score += self.evaluate_window(row_array[c: c + 4], piece)

        for c in range(self.game.num_columns):
            col_array = list(self.game.board[:, c])
            for r in range(self.game.num_rows - 3):
                score += self.evaluate_window(col_array[r: r+4], piece)

        return score

    def get_valid_columns(self):
        return [c for c in range(self.game.num_columns) if self.game.is_valid_location(c)]

    def minimax(self, depth, alpha, beta, maximizing_player):
        valid_columns = self.get_valid_columns()
        is_terminal = self.game.check_win(1) or self.game.check_win(2) or len(valid_columns) == 0


        if depth == 0 or is_terminal:
            if self.game.check_win(2):
                return (None, 1000000)
            elif self.game.check_win(1):
                return (None, -1000000)
            else:
                return (None, self.score_position(2))

        if maximizing_player:
            value = -np.inf
            best_col = random.choice(valid_columns)

            for col in valid_columns:
                row = self.game.get_next_open_row(col)
                temp_board = self.game.board.copy()
                temp_board[row][col] = 2
                new_score = self.minimax(depth - 1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    best_col = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = np.inf
            best_col = random.choice(valid_columns)

            for col in valid_columns:
                row = self.game.get_next_open_row(col)
                temp_board = self.game.board.copy()
                temp_board[row][col] = 1
                new_score = self.minimax(depth - 1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value


