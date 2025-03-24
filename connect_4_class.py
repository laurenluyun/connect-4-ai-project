import pygame
import numpy as np
import sys
import math

class Connect4:
    def __init__(self, render_delay_sec=0.5):
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

        # global variables
        self.game_over = False
        self.turn = 0
        self.board = self.create_board()

        # initialize graphical interface
        pygame.init()
        self.screen_font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption("Connect 4")
        self.draw_board()

    def create_board(self):
        board = np.zeros((self.num_rows, self.num_columns))
        return board

    def draw_grid(self, screen):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                pygame.draw.rect(screen, self.blue,(column * self.square_size, (row + 1) * self.square_size,
                                                    self.square_size, self.square_size))
                pygame.draw.circle(screen, self.black,(int((column + 0.5) * self.square_size),
                                                       int((row + 1.5) * self.square_size)), self.circle_radius)

    def draw_pieces(self, screen, board):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                if board[row][column] == 1:
                    pygame.draw.circle(screen, self.red, (int((column + 0.5) * self.square_size),
                                                          self.screen_height - int((row + 0.5) * self.square_size)), self.circle_radius)
                elif board[row][column] == 2:
                    pygame.draw.circle(screen, self.yellow, (int((column + 0.5) * self.square_size),
                                                             self.screen_height - int((row + 0.5) * self.square_size)),self.circle_radius)

    def draw_board(self):
        self.draw_grid(self.screen)
        self.draw_pieces(self.screen, self.board)
        pygame.display.update()

    def drop_player_piece(self, board, row, column, current_piece_color):
        board[row][column] = current_piece_color
        self.draw_board()

    def is_valid_location(self, board, column):
        return board[5][column] == 0

    def get_next_open_row(self, board, column):
        for row in range(self.num_rows):
            if board[row][column] == 0:
                return row

    def check_win(self, board, current_piece_color):
        # check horizonal locations for win
        for column in range(self.num_columns - 3):
            for row in range(self.num_rows):
                if (board[row][column] == current_piece_color and board[row][column + 1] == current_piece_color
                        and board[row][column + 2] == current_piece_color and board[row][column + 3] == current_piece_color):
                    return True

        # check vertical locations for win
        for column in range(self.num_columns):
            for row in range(self.num_rows - 3):
                if (board[row][column] == current_piece_color and board[row + 1][column] == current_piece_color
                        and board[row + 2][column] == current_piece_color and board[row + 3][column] == current_piece_color):
                    return True

        # check positively sloped diagonals
        for column in range(self.num_columns - 3):
            for row in range(self.num_rows - 3):
                if (board[row][column] == current_piece_color and board[row + 1][column + 1] == current_piece_color
                        and board[row + 2][column + 2] == current_piece_color and board[row + 3][column + 3] == current_piece_color):
                    return True

        # check negatively sloped diagonals
        for column in range(self.num_columns - 3):
            for row in range(3, self.num_rows):
                if (board[row][column] == current_piece_color and board[row - 1][column + 1] == current_piece_color
                        and board[row - 2][column + 2] == current_piece_color and board[row - 3][column + 3] == current_piece_color):
                    return True
        return False

    def main_game(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.black, (0, 0, self.screen_width, self.square_size))
                    x_position = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(self.screen, self.red, (x_position, int(self.square_size / 2)), self.circle_radius)
                    else:
                        pygame.draw.circle(self.screen, self.yellow, (x_position, int(self.square_size / 2)), self.circle_radius)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.black, (0, 0, self.screen_width, self.square_size))
                    x_position = event.pos[0]
                    col = int(math.floor(x_position / self.square_size))
                    if self.is_valid_location(self.board, col):
                        row = self.get_next_open_row(self.board, col)
                        self.drop_player_piece(self.board, row, col, self.turn + 1)

                        if self.check_win(self.board, self.turn + 1):
                            if self.turn == 0:
                                winning_label = self.screen_font.render(f"Player 1 wins!", 1, self.red)
                            else:
                                winning_label = self.screen_font.render(f"Player 2 wins!", 1, self.yellow)
                            self.screen.blit(winning_label, (40, 10))
                            self.game_over = True

                    # print_board(board)
                    self.draw_board()
                    self.turn += 1
                    self.turn = self.turn % 2

                    if self.game_over:
                        pygame.time.wait(3000)

if __name__ == "__main__":
    game = Connect4()
    game.main_game()