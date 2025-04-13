import random
import math
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
        '''
        evaluates the board position for the given piece - higher score means better move
        '''
        score = 0
        opponent_piece = self.PLAYER_PIECE if piece == self.AI_PIECE else self.AI_PIECE

        # Score center column (preferable to control center)
        center_array = [board[r][3] for r in range(6)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal positions
        for r in range(6):
            row_array = list(board[r])
            for c in range(4):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score vertical positions
        for c in range(7):
            col_array = [board[r][c] for r in range(6)]
            for r in range(3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score positive diagonal positions
        for r in range(3):
            for c in range(4):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score negative diagonal positions
        for r in range(3):
            for c in range(4):
                window = [board[5 - r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent_piece)

        return score

    def evaluate_window(self, window, piece, opponent_piece):
        """
        Helper method to evaluate a window of 4 positions.
        """
        score = 0

        # Count pieces
        piece_count = window.count(piece)
        empty_count = window.count(self.EMPTY)
        opponent_count = window.count(opponent_piece)

        # Score window based on piece counts
        if piece_count == 4:
            score += 100  # Winning position
        elif piece_count == 3 and empty_count == 1:
            score += 5  # Potential win next move
        elif piece_count == 2 and empty_count == 2:
            score += 2  # Developing position

        # Penalize opponent's potential wins
        if opponent_count == 3 and empty_count == 1:
            score -= 4  # Block opponent's potential win

        return score

    def is_terminal(self, board):
        """Check if the current position is terminal (game over)"""
        # Check for win
        if self.check_win(board, self.PLAYER_PIECE, self.num_columns, self.num_rows):
            return True
        if self.check_win(board, self.AI_PIECE, self.num_columns, self.num_rows):
            return True

        # Check if board is full
        return len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        '''
        Minmax for medium difficulty
        return: (column, score)
        '''
        valid_locations = self.get_valid_locations(board)

        # Terminal node or max depth reached
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                # Terminal scoring
                if self.check_win(board, self.AI_PIECE, self.num_columns, self.num_rows):
                    return (None, 1000000)  # AI win
                elif self.check_win(board, self.PLAYER_PIECE, self.num_columns, self.num_rows):
                    return (None, -1000000)  # Player win
                else:
                    return (None, 0)  # Draw
            else:
                # Heuristic scoring at max depth
                return (None, self.score_position(board, self.AI_PIECE))

        # Introduce some randomness for medium difficulty
        valid_locations = sorted(valid_locations, key=lambda x: 0.1 * random.random())

        # Maximizing player (AI)
        if maximizing_player:
            value, best_col = -math.inf, random.choice(valid_locations)
            for col in valid_locations:
                # find the available row
                row = next(r for r in range(6) if board[r][col] == 0)
                temp_board = copy.deepcopy(board)
                # simulate the move
                self.drop_piece(temp_board, row, col, self.AI_PIECE)

                # Check for immediate win (depth-1 optimization)
                if self.check_win(temp_board, self.AI_PIECE, self.num_columns, self.num_rows):
                    return (col, 1000000)

                # recursively call minimax with the next move from player1
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]

                # update if better move is found
                if new_score > value:
                    value, best_col = new_score, col

                # alpha-beta pruning
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

                # Check for immediate loss (depth-1 optimization)
                if self.check_win(temp_board, self.PLAYER_PIECE, self.num_columns, self.num_rows):
                    return (col, -1000000)

                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value, best_col = new_score, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def monte_carlo_tree_search(self, board, simulations=500):
        '''
        MCTS for AI decision-making in hard mode, simulating 'simulations' number of random games
        for each valid move. The move with the highest win count for AI is chosen.
        - reduce default simulation count for better performance
        - add early termination for clearly winning/losing positions
        - add weighting to favor center positions
        :param board: current game board
        :param simulations: number of random games to simulate per move
        :return: the best column to play based on MCTS simulation results
        '''
        valid_moves = self.get_valid_locations(board)
        if not valid_moves:
            return -1  # No valid moves

        # Quick check for immediate winning move
        for col in valid_moves:
            row = next(r for r in range(6) if board[r][col] == 0)
            temp_board = copy.deepcopy(board)
            self.drop_piece(temp_board, row, col, self.AI_PIECE)
            if self.check_win(temp_board, self.AI_PIECE, self.num_columns, self.num_rows):
                # Return winning move immediately
                return col

        # Quick check for immediate blocking move
        for col in valid_moves:
            row = next(r for r in range(6) if board[r][col] == 0)
            temp_board = copy.deepcopy(board)
            self.drop_piece(temp_board, row, col, self.PLAYER_PIECE)
            if self.check_win(temp_board, self.PLAYER_PIECE, self.num_columns, self.num_rows):
                # Block opponent's winning move
                return col

        # Center column preference weight
        center_weight = 2 if 3 in valid_moves else 1
        move_scores = {col: 0 for col in valid_moves}
        move_simulations = {col: 0 for col in valid_moves}

        # Give initial bias to center columns
        if 3 in move_scores:
            # Small bias for center column
            move_scores[3] += 0.5

        # Track best move
        best_score = -1
        early_stop_threshold = simulations // 4  # 25% of total simulations

        # run simulations for each valid move
        for col in valid_moves:
            wins = 0
            for _ in range(simulations):
                sim_board = copy.deepcopy(board)
                row = next(r for r in range(6) if sim_board[r][col] == 0)
                self.drop_piece(sim_board, row, col, self.AI_PIECE)
                # simulate a random game from this position
                if self.simulate_random_game(sim_board):
                    wins += 1

                move_simulations[col] = _ + 1
                current_win_rate = wins / (_ + 1)

                # Apply center column preference
                if col == 3:
                    move_scores[col] = current_win_rate * center_weight
                else:
                    move_scores[col] = current_win_rate

                # Early termination checks
                if _ > early_stop_threshold:
                    if current_win_rate > best_score:
                        best_score = current_win_rate
                    # If we're significantly behind the best move, stop simulating this move
                    elif current_win_rate < best_score - 0.3:
                        break

        # For moves that didn't complete all simulations, adjust scores
        for col in valid_moves:
            if move_simulations[col] < simulations:
                # Penalize slightly for incomplete simulation (uncertainty)
                confidence_factor = move_simulations[col] / simulations
                move_scores[col] *= confidence_factor

        # Return the column with the highest score
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

    def random_move(self, board):
        """
        Selects a random valid move for easy difficulty
        """
        valid_locations = self.get_valid_locations(board)
        if not valid_locations:
            # The board is full or the game is over
            return -1  # Invalid column to indicate no move is possible

            # Return a random valid column
        return random.choice(valid_locations)

