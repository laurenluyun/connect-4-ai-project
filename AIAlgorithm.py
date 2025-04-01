import random
import math
import numpy as np
import copy


class AIAlgorithm:
    def __init__(self, ai_piece, player_piece):
        # AI's piece identifier (typically 2)
        self.AI_PIECE = ai_piece
        # Player's piece identifier (typically 1)
        self.PLAYER_PIECE = player_piece
        # Empty slot identifier in the board
        self.EMPTY = 0
        self.num_rows = 6
        self.num_columns = 7

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
                temp_board = copy.deepcopy(board)
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
                temp_board = copy.deepcopy(board)
                self.drop_piece(temp_board, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value, best_col = new_score, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def monte_carlo_tree_search(self, board, simulations=1000):
        '''
        MCTS for AI decision-making in hard mode, simulating 'simulations' number of random games
        for each valid move. The move with the highest win count for AI is chosen
        :param board:
        :param simulations:
        :return: the best column to play based on MCTS simulation results
        '''
        valid_moves = self.get_valid_locations(board)
        move_scores = {col: 0 for col in valid_moves}

        # run simulations for each valid move
        for col in valid_moves:
            for _ in range(simulations):
                sim_board = copy.deepcopy(board)
                row = next(r for r in range(6) if sim_board[r][col] == 0)
                self.drop_piece(sim_board, row, col, self.AI_PIECE)
                # simulate a random game from this position
                if self.simulate_random_game(sim_board):
                    move_scores[col] += 1
        # return the column with the highest simulation win rate
        return max(move_scores, key=move_scores.get)

    def simulate_random_game(self, board):
        '''
        Simulates a complete game from a given board state using random moves.
        - Players take turns making random valid moves.
        - The game continues until a winner is found or no moves are left.
        :param board:
        :return: True if AI wins, False otherwise
        '''
        # start with the opponent's turn
        current_piece = self.PLAYER_PIECE
        while True:
            valid_moves = self.get_valid_locations(board)
            if not valid_moves:
                return False

            # select a random valid move
            col = random.choice(valid_moves)
            row = next(r for r in range(6) if board[r][col] == 0)
            self.drop_piece(board, row, col, current_piece)

            # check if the current move results in a win
            if self.check_win(board, current_piece, self.num_columns, self.num_rows):
                # return True if AI wins
                return current_piece == self.AI_PIECE

            # switch turns between AI and player
            current_piece = self.PLAYER_PIECE if current_piece == self.AI_PIECE else self.AI_PIECE

    def check_win(self, board, piece, num_columns, num_rows):
        # check horizontal locations for win
        for column in range(num_columns - 3):
            for row in range(num_rows):
                if (board[row][column] == piece and board[row][column + 1] == piece
                        and board[row][column + 2] == piece and board[row][column + 3] == piece):
                    return True

        # check vertical locations for win
        for column in range(num_columns):
            for row in range(num_rows - 3):
                if (board[row][column] == piece and board[row + 1][column] == piece
                        and board[row + 2][column] == piece and board[row + 3][column] == piece):
                    return True

        # check positively sloped diagonals
        for column in range(num_columns - 3):
            for row in range(num_rows - 3):
                if (board[row][column] == piece and board[row + 1][column + 1] == piece
                        and board[row + 2][column + 2] == piece and board[row + 3][column + 3] == piece):
                    return True

        # check negatively sloped diagonals
        for column in range(num_columns - 3):
            for row in range(3, num_rows):
                if (board[row][column] == piece and board[row - 1][column + 1] == piece
                        and board[row - 2][column + 2] == piece and board[row - 3][column + 3] == piece):
                    return True
        return False

