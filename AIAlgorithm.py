import random
import math


class AIAlgorithm:
    def __init__(self, ai_piece, player_piece):
        # AI's piece identifier (typically 2)
        self.AI_PIECE = ai_piece
        # Player's piece identifier (typically 1)
        self.PLAYER_PIECE = player_piece
        # Empty slot identifier in the board
        self.EMPTY = 0

    def is_valid_location(self, board, col):
        # A column is valid if the top row (row index 5) is empty
        return board[5][col] == 0

    # return a list of all valid columns where a move can be made
    def get_valid_locations(self, board):
        return [col for col in range(7) if self.is_valid_location(board, col)]

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def score_position(self, board, piece):
        score = 0
        # extract the center column
        center_array = [board[i][3] for i in range(6)]
        # center columns are weighted higher
        score += center_array.count(piece) * 3
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations(board)
        # base case is when there is no move available
        if depth == 0 or not valid_locations:
            return (None, self.score_position(board, self.AI_PIECE))
        if maximizing_player:
            value, best_col = -math.inf, random.choice(valid_locations)
            for col in valid_locations:
                # find the available row
                row = next(r for r in range(6) if board[r][col] == 0)
                temp_board = board.copy()
                # simulate the move
                self.drop_piece(temp_board, row, col, self.AI_PIECE)
                # recursively call minimax with the next move from player1
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value, best_col = new_score, col
                alpha = max(alpha, value)
                # prune the search tree
                if alpha >= beta:
                    break
            return best_col, value
        # minimize the player1's best possible move
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
