import numpy as np
import random
import math
from AIAlgorithm import AIAlgorithm


class Connect4Game:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.ai = AIAlgorithm(ai_piece=2, player_piece=1)
        self.game_over = False
        self.turn = random.choice([0, 1])
        self.game_mode = self.get_game_mode()

    def get_game_mode(self):
        """Ask the user to select the game mode."""
        while True:
            mode = input("Choose game mode: (1) Player vs. Player, (2) Player vs. AI: ")
            if mode in {"1", "2"}:
                return "PvP" if mode == "1" else "PvAI"
            print("Invalid choice. Enter 1 or 2.")

    def print_board(self):
        print(np.flip(self.board, 0))

    def make_move(self, col, piece):
        if self.ai.is_valid_location(self.board, col):
            row = next(r for r in range(6) if self.board[r][col] == 0)
            self.ai.drop_piece(self.board, row, col, piece)
            if self.ai.winning_move(self.board, piece):
                self.game_over = True
            return True
        return False

    def ai_move(self):
        col, _ = self.ai.minimax(self.board, 5, -math.inf, math.inf, True)
        self.make_move(col, self.ai.AI_PIECE)

    def start_game(self):
        """Main game loop."""
        print("Welcome to Connect 4!")
        self.print_board()

        while not self.game_over:
            if self.game_mode == "PvAI":
                if self.turn == 0:
                    col = int(input("Enter column (0-6): "))
                    if self.make_move(col, 1):
                        self.turn = 1
                else:
                    self.ai_move()
                    self.turn = 0
            else:  # PvP Mode
                col = int(input(f"Player {self.turn + 1}, enter column (0-6): "))
                if self.make_move(col, self.turn + 1):
                    self.turn = 1 - self.turn  # Switch player

            self.print_board()

        print(f"Game Over! Player {self.turn + 1} wins!")


# Start the game
if __name__ == "__main__":
    game = Connect4Game()
    game.start_game()
