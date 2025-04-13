import numpy as np
import random
import math
import pygame
import sys
from AIAlgorithm import AIAlgorithm
from Button import Button

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
        self.pink = (255, 0, 239)
        self.orange = (255, 145, 0)
        self.white = (255, 255, 255)
        self.gray = (196, 196, 196)
        self.blue = (0, 0, 255)
        self.black = (0, 0, 0)
        self.green = (3, 155, 49)

        self.game_over = False
        self.turn = random.choice([0, 1])
        self.turn = 0
        self.board = self.create_board()

        # initialize graphical interface
        pygame.init()
        self.screen_font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption("Connect 4")

        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.ai = AIAlgorithm(self.AI_PIECE, self.PLAYER_PIECE)
        self.DEPTH = 3
        self.ALPHA = -math.inf
        self.BETA = math.inf

        self.game_mode = None
        self.difficulty = None

    def create_board(self):
        return np.zeros((self.num_rows, self.num_columns))

    # generate a main menu on the screen
    def menu(self):
        """Ask the user to select the game mode."""
        while True:
            self.reset_game()
            self.game_mode = None
            self.difficulty = None
            self.screen.fill(self.gray)
            mouse_position = pygame.mouse.get_pos()
            connect_4_text = self.screen_font.render(f"Connect 4", 1, self.blue)
            self.screen.blit(connect_4_text, (self.screen_width / 4 - 20, 60))
            main_menu_text = self.screen_font.render(f"Main Menu", 1, self.blue)
            self.screen.blit(main_menu_text, (self.screen_width / 4 - 20, 150))
            play_button = Button(position=(self.screen_width / 2, 350), text_input="Play", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            quit_button = Button(position=(self.screen_width / 2, 550), text_input="Quit", font=self.screen_font, base_color=self.blue, hovering_color=self.green)

            for button in [play_button, quit_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_button_input(mouse_position):
                        self.one_player_or_two_player_menu()
                    if quit_button.check_for_button_input(mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    # creating play screen to choose between 1 player and 2 player options
    def one_player_or_two_player_menu(self):
        while True:
            self.screen.fill(self.gray)
            mouse_position = pygame.mouse.get_pos()
            single_player_button = Button(position=(self.screen_width / 2, 150), text_input="1 Player", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            two_players_button = Button(position=(self.screen_width / 2, 350), text_input="2 Players", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            back_button = Button(position=(self.screen_width / 2, 550), text_input="Back", font=self.screen_font, base_color=self.blue, hovering_color=self.green)

            for button in [single_player_button, two_players_button, back_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if single_player_button.check_for_button_input(mouse_position):
                        self.game_mode = "PvAI"
                        self.choose_difficulty_level_menu()
                        if self.game_over:
                            return
                    if two_players_button.check_for_button_input(mouse_position):
                        self.game_mode = "PvP"
                        self.start_game()
                        return
                    if back_button.check_for_button_input(mouse_position):
                        return

            pygame.display.update()

    # creating 1 player screen to choose between easy, medium, hard mode AI
    def choose_difficulty_level_menu(self):
        while True:
            self.screen.fill(self.gray)
            mouse_position = pygame.mouse.get_pos()
            difficulty_screen_font = pygame.font.SysFont("monospace", 60)
            difficulty_mode_text = difficulty_screen_font.render(f"AI Difficulty Mode", 1, self.blue)
            self.screen.blit(difficulty_mode_text, (30, 60))
            easy_mode_button = Button(position=(self.screen_width / 2, 200), text_input="Easy",
                                          font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            medium_mode_button = Button(position=(self.screen_width / 2, 350), text_input="Medium",
                                        font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            hard_mode_button = Button(position=(self.screen_width / 2, 500), text_input="Hard", font=self.screen_font,
                                 base_color=self.blue, hovering_color=self.green)
            back_button = Button(position=(self.screen_width / 2, 650), text_input="Back", font=self.screen_font, base_color=self.blue, hovering_color=self.green)

            for button in [easy_mode_button, medium_mode_button,hard_mode_button, back_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_mode_button.check_for_button_input(mouse_position):
                        self.difficulty = "easy"
                        self.start_game()
                        return
                    if medium_mode_button.check_for_button_input(mouse_position):
                        # print()
                        self.difficulty = "medium"
                        self.start_game()
                        return
                    if hard_mode_button.check_for_button_input(mouse_position):
                        self.difficulty = "hard"
                        self.start_game()
                        return
                    if back_button.check_for_button_input(mouse_position):
                        return

            pygame.display.update()

    def draw_grid(self):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                pygame.draw.rect(self.screen, self.gray,(column * self.square_size, (row + 1) * self.square_size,
                                                    self.square_size, self.square_size))
                pygame.draw.circle(self.screen, self.white,(int((column + 0.5) * self.square_size),
                                                       int((row + 1.5) * self.square_size)), self.circle_radius)

    def draw_pieces(self):
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                if self.board[row][column] == 1:
                    pygame.draw.circle(self.screen, self.pink, (int((column + 0.5) * self.square_size),
                                                          self.screen_height - int((row + 0.5) * self.square_size)), self.circle_radius)
                elif self.board[row][column] == 2:
                    pygame.draw.circle(self.screen, self.orange, (int((column + 0.5) * self.square_size),
                                                             self.screen_height - int((row + 0.5) * self.square_size)),self.circle_radius)

    def draw_board(self):
        self.draw_grid()
        self.draw_pieces()
        pygame.display.update()

    def drop_player_piece(self,row, column, piece):
        self.board[row][column] = piece
        self.draw_board()

    # executes a move and checks for win
    def make_move(self, col, piece):
        if self.ai.is_valid_location(self.board, col):
            row = next(r for r in range(6) if self.board[r][col] == 0)
            self.drop_player_piece(row, col, piece)
            if self.ai.check_win(self.board, piece, self.num_columns, self.num_rows):
                self.game_over = True
                if piece == self.PLAYER_PIECE:
                    winning_label = self.screen_font.render(f"Player 1 wins!", 1, self.pink)
                else:
                    winning_label = self.screen_font.render(f"Player 2 wins!", 1, self.orange)
                self.screen.blit(winning_label, (40, 10))
            return True
        return False

    def ai_move(self):
        # First check if there are any valid moves
        valid_moves = self.ai.get_valid_locations(self.board)
        if not valid_moves:
            # No valid moves - game should be over
            self.game_over = True
            return False

        if self.difficulty == 'easy':
            # easy mode: random move selection
            col = self.ai.random_move(self.board)
        elif self.difficulty == "medium":
            # medium mode: minmax with alpha-beta pruning
            col, _ = self.ai.minimax(self.board, self.DEPTH, self.ALPHA, self.BETA, True)
        else:
            # hard mode: monte carlo tree search
            col = self.ai.monte_carlo_tree_search(self.board)

        # Check if we got a valid column
        if col == -1 or col not in valid_moves:
            # Something went wrong, just pick the first valid move
            col = valid_moves[0] if valid_moves else 0

        # AI makes the move
        self.make_move(col, self.AI_PIECE)

    def reset_game(self):
        self.game_over = False
        self.board = self.create_board()

    def restart_screen(self):
        while True:
            self.screen.fill(self.gray)
            mouse_position = pygame.mouse.get_pos()
            play_again_button = Button(position=(self.screen_width / 2, 200), text_input="Play Again",
                                          font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            main_menu_button = Button(position=(self.screen_width / 2, 350), text_input="Main Menu",
                                        font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            quit_button = Button(position=(self.screen_width / 2, 500), text_input="Quit", font=self.screen_font,
                                 base_color=self.blue, hovering_color=self.green)

            for button in [play_again_button, main_menu_button, quit_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.check_for_button_input(mouse_position):
                        self.reset_game()
                        self.screen.fill(self.white)
                        self.draw_board()
                        self.turn = random.choice([0, 1])
                        return
                    if main_menu_button.check_for_button_input(mouse_position):
                        return
                    if quit_button.check_for_button_input(mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def start_game(self):
        self.reset_game()
        self.screen.fill(self.white)
        self.draw_board()
        while not self.game_over:
            # If it's AI's turn, make the move automatically
            if self.game_mode == "PvAI" and self.turn == 1 and not self.game_over:
                pygame.time.wait(500)  # Add a slight delay for realism
                self.ai_move()
                self.turn = 0  # Switch back to player
                self.draw_board()
                if self.game_over:
                    pygame.time.wait(4000)
                    self.restart_screen()
                    if self.game_over:
                        return

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    # Make sure the piece follows the mouse even during AI turn
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.screen, self.white, (0, 0, self.screen_width, self.square_size))
                        x_position = event.pos[0]
                        if self.turn == 0:  # Player1's turn
                            pygame.draw.circle(self.screen, self.pink, (x_position, int(self.square_size / 2)), self.circle_radius)
                        else:  # another player's turn
                            pygame.draw.circle(self.screen, self.orange, (x_position, int(self.square_size / 2)), self.circle_radius)
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.screen, self.white, (0, 0, self.screen_width, self.square_size))
                        x_position = event.pos[0]
                        col = int(math.floor(x_position / self.square_size))
                        if self.make_move(col, self.turn + 1):
                            self.turn = 1 - self.turn  # Switch player
                        self.draw_board()
                        if self.game_over:
                            pygame.time.wait(4000)
                            self.restart_screen()
                            if self.game_over:
                                return



# Start the game
if __name__ == "__main__":
    game = Connect4Game()
    game.menu()
