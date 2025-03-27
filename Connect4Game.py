import numpy as np
import random
import math
import pygame
import sys
from AIAlgorithm import AIAlgorithm


class Connect4Game:
    def __init__(self):
        # constants
        self.num_rows = 6
        self.num_columns = 7
        self.square_size = 100
        self.screen_width = self.num_columns * self.square_size
        self.screen_height = (self.num_rows + 1) * self.square_size
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.circle_radius = int(self.square_size / 2 - 5)

        # color definitions
        self.blue = (0, 0, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)

        self.game_over = False
        self.turn = random.choice([0, 1])
        self.board = self.create_board()

        # initialize graphical interface
        pygame.init()
        self.screen_font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption("Connect 4")
        self.draw_board()

        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.ai = AIAlgorithm(self.AI_PIECE, self.PLAYER_PIECE)
        self.DEPTH = 5
        self.ALPHA = -math.inf
        self.BETA = math.inf

        self.game_mode = self.get_game_mode()

    def create_board(self):
        return np.zeros((self.num_rows, self.num_columns))

    # generate a menu on the board
    def get_game_mode(self):
        """Ask the user to select the game mode."""
        while True:
            mode = input("Choose game mode: (1) Player vs. Player, (2) Player vs. AI: ")
            if mode in {"1", "2"}:
                return "PvP" if mode == "1" else "PvAI"
            print("Invalid choice. Enter 1 or 2.")

    def draw_grid(self):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                pygame.draw.rect(self.screen, self.blue,(column * self.square_size, (row + 1) * self.square_size,
                                                    self.square_size, self.square_size))
                pygame.draw.circle(self.screen, self.black,(int((column + 0.5) * self.square_size),
                                                       int((row + 1.5) * self.square_size)), self.circle_radius)

    def draw_pieces(self):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                if self.board[row][column] == 1:
                    pygame.draw.circle(self.screen, self.red, (int((column + 0.5) * self.square_size),
                                                          self.screen_height - int((row + 0.5) * self.square_size)), self.circle_radius)
                elif self.board[row][column] == 2:
                    pygame.draw.circle(self.screen, self.yellow, (int((column + 0.5) * self.square_size),
                                                             self.screen_height - int((row + 0.5) * self.square_size)),self.circle_radius)

    def draw_board(self):
        self.draw_grid()
        self.draw_pieces()
        pygame.display.update()

    def drop_player_piece(self,row, column, piece):
        self.board[row][column] = piece
        self.draw_board()

    def check_win(self, piece):
        # check horizontal locations for win
        for column in range(self.num_columns - 3):
            for row in range(self.num_rows):
                if (self.board[row][column] == piece and self.board[row][column + 1] == piece
                        and self.board[row][column + 2] == piece and self.board[row][column + 3] == piece):
                    return True

        # check vertical locations for win
        for column in range(self.num_columns):
            for row in range(self.num_rows - 3):
                if (self.board[row][column] == piece and self.board[row + 1][column] == piece
                        and self.board[row + 2][column] == piece and self.board[row + 3][column] == piece):
                    return True

        # check positively sloped diagonals
        for column in range(self.num_columns - 3):
            for row in range(self.num_rows - 3):
                if (self.board[row][column] == piece and self.board[row + 1][column + 1] == piece
                        and self.board[row + 2][column + 2] == piece and self.board[row + 3][column + 3] == piece):
                    return True

        # check negatively sloped diagonals
        for column in range(self.num_columns - 3):
            for row in range(3, self.num_rows):
                if (self.board[row][column] == piece and self.board[row - 1][column + 1] == piece
                        and self.board[row - 2][column + 2] == piece and self.board[row - 3][column + 3] == piece):
                    return True
        return False

    # executes a move and checks for win
    def make_move(self, col, piece):
        if self.ai.is_valid_location(self.board, col):
            row = next(r for r in range(6) if self.board[r][col] == 0)
            self.drop_player_piece(row, col, piece)
            if self.check_win(piece):
                self.game_over = True
                if piece == self.PLAYER_PIECE:
                    winning_label = self.screen_font.render(f"Player 1 wins!", 1, self.red)
                else:
                    winning_label = self.screen_font.render(f"Player 2 wins!", 1, self.yellow)
                self.screen.blit(winning_label, (40, 10))
            return True
        return False

    def ai_move(self):
        # AI selects the best move
        col, _ = self.ai.minimax(self.board, self.DEPTH, self.ALPHA, self.BETA, True)
        # AI makes the move
        self.make_move(col, self.AI_PIECE)

    def start_game(self):
        while not self.game_over:
            # If it's AI's turn, make the move automatically
            if self.game_mode == "PvAI" and self.turn == 1 and not self.game_over:
                pygame.time.wait(500)  # Add a slight delay for realism
                self.ai_move()
                self.turn = 0  # Switch back to player
                self.draw_board()
                if self.game_over:
                    pygame.time.wait(4000)

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    # Make sure the piece follows the mouse even during AI turn
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.screen, self.black, (0, 0, self.screen_width, self.square_size))
                        x_position = event.pos[0]
                        if self.turn == 0:  # Player1's turn
                            pygame.draw.circle(self.screen, self.red, (x_position, int(self.square_size / 2)), self.circle_radius)
                        else:  # another player's turn
                            pygame.draw.circle(self.screen, self.yellow, (x_position, int(self.square_size / 2)), self.circle_radius)
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.screen, self.black, (0, 0, self.screen_width, self.square_size))
                        x_position = event.pos[0]
                        col = int(math.floor(x_position / self.square_size))
                        if self.make_move(col, self.turn + 1):
                            self.turn = 1 - self.turn  # Switch player
                        self.draw_board()
                        if self.game_over:
                            pygame.time.wait(4000)


# Start the game
if __name__ == "__main__":
    game = Connect4Game()
    game.start_game()
