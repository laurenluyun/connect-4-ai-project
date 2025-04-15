import numpy as np
import random
import math
from tqdm import tqdm


class AIEvaluator:
    """
    Evaluator that calculates win rates between AI algorithms
    """

    def __init__(self, ai_algorithm_class):
        self.AIAlgorithm = ai_algorithm_class
        self.num_rows = 6
        self.num_columns = 7
        # track wins/losses/draws
        self.stats = {
            "random_vs_minimax": {"random_wins": 0, "minimax_wins": 0, "draws": 0, "total_games": 0},
            "random_vs_mcts": {"random_wins": 0, "mcts_wins": 0, "draws": 0, "total_games": 0},
            "minimax_vs_mcts": {"minimax_wins": 0, "mcts_wins": 0, "draws": 0, "total_games": 0}
        }

    def create_board(self):
        # Create an empty Connect Four board
        return np.zeros((self.num_rows, self.num_columns))

    def get_next_open_row(self, board, col):
        # Find the next available row in the given column
        for r in range(self.num_rows):
            if board[r][col] == 0:
                return r
        return -1

    def drop_piece(self, board, row, col, piece):
        # Place a piece on the board
        board[row][col] = piece

    def is_valid_location(self, board, col):
        # Check if a column has space for another piece
        return col >= 0 and col < self.num_columns and board[self.num_rows - 1][col] == 0

    def get_algorithm_move(self, algorithm_type, board, ai_instance, piece=2):
        # Get the next move from the specified algorithm type
        if algorithm_type == "random":
            col = ai_instance.random_move(board)
        elif algorithm_type == "minimax":
            col, _ = ai_instance.minimax(board, 3, -math.inf, math.inf, True)
        elif algorithm_type == "mcts":
            col = ai_instance.monte_carlo_tree_search(board)

        return col

    def play_game(self, algo1, algo2):
        """
        Simulate a full game between two AI algorithms

        Parameters:
        - algo1: first algorithm ("random", "minimax", or "mcts")
        - algo2: second algorithm ("random", "minimax", or "mcts")

        Returns:
        - winner: 1 for algo1, 2 for algo2, 0 for draw
        """
        # Create a new board
        board = self.create_board()

        # Initialize AI instances with proper piece assignments
        ai1 = self.AIAlgorithm(1, 2)  # AI 1 uses piece 1
        ai2 = self.AIAlgorithm(2, 1)  # AI 2 uses piece 2

        # Game variables
        game_over = False
        turn = 0  # 0 for algo1, 1 for algo2

        # Play until game is over
        while not game_over:
            # Get column based on current algorithm's turn
            if turn == 0:
                col = self.get_algorithm_move(algo1, board, ai1, piece=1)
            else:
                col = self.get_algorithm_move(algo2, board, ai2, piece=2)

            # Make sure the move is valid
            if not self.is_valid_location(board, col):
                # If invalid move, pick a random valid column
                valid_cols = [c for c in range(self.num_columns) if self.is_valid_location(board, c)]
                if not valid_cols:
                    # No valid moves left, it's a draw
                    return 0
                col = random.choice(valid_cols)

            # Get the next open row
            row = self.get_next_open_row(board, col)

            # Drop the piece
            piece = 1 if turn == 0 else 2
            self.drop_piece(board, row, col, piece)

            # Check for win
            if self.check_win(board, piece):
                game_over = True
                return 1 if turn == 0 else 2

            # Check for draw (board is full)
            if self.is_board_full(board):
                game_over = True
                return 0

            # Switch turns
            turn = 1 - turn

        return 0  # Should not reach here, but return draw if it does

    def is_board_full(self, board):
        """Check if the board is full (no valid moves left)"""
        return all(board[self.num_rows - 1][col] != 0 for col in range(self.num_columns))

    def check_win(self, board, piece):
        """Check if the current player has won"""
        # Check horizontal
        for c in range(self.num_columns - 3):
            for r in range(self.num_rows):
                if (board[r][c] == piece and board[r][c + 1] == piece and
                        board[r][c + 2] == piece and board[r][c + 3] == piece):
                    return True

        # Check vertical
        for c in range(self.num_columns):
            for r in range(self.num_rows - 3):
                if (board[r][c] == piece and board[r + 1][c] == piece and
                        board[r + 2][c] == piece and board[r + 3][c] == piece):
                    return True

        # Check positively sloped diagonals
        for c in range(self.num_columns - 3):
            for r in range(self.num_rows - 3):
                if (board[r][c] == piece and board[r + 1][c + 1] == piece and
                        board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                    return True

        # Check negatively sloped diagonals
        for c in range(self.num_columns - 3):
            for r in range(3, self.num_rows):
                if (board[r][c] == piece and board[r - 1][c + 1] == piece and
                        board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                    return True

        return False

    def run_competition(self, num_games=50):
        """
        Run a competition between all algorithm pairs, focusing only on win rates

        Parameters:
        - num_games: number of games to play for each pairing

        Returns:
        - Dictionary with win rate results
        """
        matchups = [
            ("random", "minimax"),
            ("random", "mcts"),
            ("minimax", "mcts")
        ]

        for algo1, algo2 in matchups:
            matchup_key = f"{algo1}_vs_{algo2}"
            print(f"\nRunning competition: {algo1.title()} vs {algo2.title()} - {num_games} games")

            # Play games with each algorithm going first half the time
            for i in tqdm(range(num_games)):
                # Alternate which algorithm goes first to ensure fairness
                if i % 2 == 0:
                    first, second = algo1, algo2
                else:
                    first, second = algo2, algo1

                # Play the game
                winner = self.play_game(first, second)

                # Update statistics based on the winner
                if winner == 0:
                    # Draw
                    self.stats[matchup_key]["draws"] += 1
                elif (winner == 1 and i % 2 == 0) or (winner == 2 and i % 2 == 1):
                    # First algorithm won
                    self.stats[matchup_key][f"{algo1}_wins"] += 1
                else:
                    # Second algorithm won
                    self.stats[matchup_key][f"{algo2}_wins"] += 1

                self.stats[matchup_key]["total_games"] += 1

        return self.get_win_rates()

    def get_win_rates(self):
        """Generate win rate results only"""
        results = {}

        # Calculate win rates
        for matchup, data in self.stats.items():
            algo1, algo2 = matchup.split("_vs_")
            total_games = data["total_games"]
            if total_games > 0:
                algo1_win_rate = (data[f"{algo1}_wins"] / total_games) * 100
                algo2_win_rate = (data[f"{algo2}_wins"] / total_games) * 100
                draw_rate = (data["draws"] / total_games) * 100

                results[matchup] = {
                    f"{algo1}_win_rate": algo1_win_rate,
                    f"{algo2}_win_rate": algo2_win_rate,
                    "draw_rate": draw_rate
                }

        return results

    def print_win_rates(self):
        """Print the win rates in a table format"""
        results = self.get_win_rates()

        print("\n=== ALGORITHM WIN RATES ===\n")
        print(f"{'Matchup':<20} | {'Algorithm 1 Win %':<20} | {'Algorithm 2 Win %':<20} | {'Draw %':<10}")
        print("-" * 75)

        for matchup, data in results.items():
            algo1, algo2 = matchup.split("_vs_")
            print(f"{algo1.title()} vs {algo2.title():<10} | "
                  f"{data[f'{algo1}_win_rate']:<20.2f} | "
                  f"{data[f'{algo2}_win_rate']:<20.2f} | "
                  f"{data['draw_rate']:<10.2f}")


# Example usage
if __name__ == "__main__":
    from AIAlgorithm import AIAlgorithm  # Import your AI algorithm class

    # Create evaluator
    evaluator = AIEvaluator(AIAlgorithm)

    # Run a competition with 50 games per matchup
    results = evaluator.run_competition(num_games=50)

    # Print just the win rates
    evaluator.print_win_rates()
