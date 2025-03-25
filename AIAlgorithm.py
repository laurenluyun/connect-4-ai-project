import random
import math


class AIAlgorithm:
    def __init__(self, ai_piece, player_piece):
        self.AI_PIECE = ai_piece
        self.PLAYER_PIECE = player_piece
        self.EMPTY = 0

    def is_valid_location(self, board, col):
        return board[5][col] == 0

    def get_valid_locations(self, board):
        return [col for col in range(7) if self.is_valid_location(board, col)]

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def winning_move(self, board, piece):
        for c in range(4):
            for r in range(6):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True
        for c in range(7):
            for r in range(3):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True
        for c in range(4):
            for r in range(3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True
        for c in range(4):
            for r in range(3, 6):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True
        return False

    def score_position(self, board, piece):
        score = 0
        center_array = [board[i][3] for i in range(6)]
        score += center_array.count(piece) * 3
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations(board)
        if depth == 0 or not valid_locations:
            return (None, self.score_position(board, self.AI_PIECE))
        if maximizing_player:
            value, best_col = -math.inf, random.choice(valid_locations)
            for col in valid_locations:
                row = next(r for r in range(6) if board[r][col] == 0)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, self.AI_PIECE)
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value, best_col = new_score, col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value, best_col = math.inf, random.choice(valid_locations)
            for col in valid_locations:
                row = next(r for r in range(6) if board[r][col] == 0)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value, best_col = new_score, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value
