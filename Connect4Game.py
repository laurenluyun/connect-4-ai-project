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

        # initialize game state
        self.game_over = False
        self.turn = random.choice([0, 1])
        self.turn = 0
        self.board = self.create_board()
        self.game_mode = None
        self.difficulty = None

        # initialize graphical interface
        pygame.init()
        self.screen_font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption("Connect 4")

        # AI constants for AIAlgorithm
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.ai = AIAlgorithm(self.AI_PIECE, self.PLAYER_PIECE)
        self.DEPTH = 3
        self.ALPHA = -math.inf
        self.BETA = math.inf

    def create_board(self):
        """
        Creates a board full of zeros for Connect 4 game
        """
        return np.zeros((self.num_rows, self.num_columns))

    # generate a main menu on the screen
    def menu(self):
        """Ask the user to select the game mode."""
        while True:
            self.reset_game()
            self.game_mode = None
            self.difficulty = None

            # create main menu screen
            self.screen.fill(self.gray)
            connect_4_text = self.screen_font.render(f"Connect 4", 1, self.blue)
            self.screen.blit(connect_4_text, (self.screen_width / 4 - 20, 60))
            main_menu_text = self.screen_font.render(f"Main Menu", 1, self.blue)
            self.screen.blit(main_menu_text, (self.screen_width / 4 - 20, 150))
            play_button = Button(position=(self.screen_width / 2, 350), text_input="Play", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            quit_button = Button(position=(self.screen_width / 2, 550), text_input="Quit", font=self.screen_font, base_color=self.blue, hovering_color=self.green)

            mouse_position = pygame.mouse.get_pos() # tracking mouse position in main menu

            # this highlights button that mouse is currently on
            for button in [play_button, quit_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_button_input(mouse_position):  # click play button goes to single or two player mode screen
                        self.one_player_or_two_player_menu()
                    if quit_button.check_for_button_input(mouse_position):  # click quit closes program
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def one_player_or_two_player_menu(self):
        """
        Creating play screen to choose between 1 player and 2 players options
        """
        while True:
            # creating game mode selection screen
            self.screen.fill(self.gray)
            single_player_button = Button(position=(self.screen_width / 2, 150), text_input="1 Player", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            two_players_button = Button(position=(self.screen_width / 2, 350), text_input="2 Players", font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            back_button = Button(position=(self.screen_width / 2, 550), text_input="Back", font=self.screen_font, base_color=self.blue, hovering_color=self.green)

            mouse_position = pygame.mouse.get_pos() # tracking mouse position in game mode menu

            # this highlights button that mouse is currently on
            for button in [single_player_button, two_players_button, back_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if single_player_button.check_for_button_input(mouse_position): # click single player button goes to select difficulty screen
                        self.game_mode = "PvAI"
                        self.choose_difficulty_level_menu()
                        if self.game_over:
                            return
                    if two_players_button.check_for_button_input(mouse_position): # click two player button goes to play a 2 player game
                        self.game_mode = "PvP"
                        self.start_game()
                        return
                    if back_button.check_for_button_input(mouse_position): # click back button goes back to main menu
                        return

            pygame.display.update()

    def choose_difficulty_level_menu(self):
        """
        creating a choose difficulty level for single player mode
        """
        while True:
            # creating difficulty level selection screen
            self.screen.fill(self.gray)
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

            mouse_position = pygame.mouse.get_pos() # tracking mouse position in difficulty selection menu

            # this highlights button that mouse is currently on
            for button in [easy_mode_button, medium_mode_button,hard_mode_button, back_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_mode_button.check_for_button_input(mouse_position): # click easy button to play against easy AI
                        self.difficulty = "easy"
                        self.start_game()
                        return
                    if medium_mode_button.check_for_button_input(mouse_position): # click medium button to play against medium AI
                        self.difficulty = "medium"
                        self.start_game()
                        return
                    if hard_mode_button.check_for_button_input(mouse_position): # click hard button to play against hard AI
                        self.difficulty = "hard"
                        self.start_game()
                        return
                    if back_button.check_for_button_input(mouse_position): # click back button to go back to choose between 1 and 2 player options
                        return

            pygame.display.update()

    def draw_grid(self):
        """
        Draw game board on screen
        """
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                pygame.draw.rect(self.screen, self.gray,(column * self.square_size, (row + 1) * self.square_size,
                                                    self.square_size, self.square_size))
                pygame.draw.circle(self.screen, self.white,(int((column + 0.5) * self.square_size),
                                                       int((row + 1.5) * self.square_size)), self.circle_radius)

    def draw_pieces(self):
        """
        Draw player pieces on screen
        """
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                if self.board[row][column] == 1:
                    pygame.draw.circle(self.screen, self.pink, (int((column + 0.5) * self.square_size),
                                                          self.screen_height - int((row + 0.5) * self.square_size)), self.circle_radius)
                elif self.board[row][column] == 2:
                    pygame.draw.circle(self.screen, self.orange, (int((column + 0.5) * self.square_size),
                                                             self.screen_height - int((row + 0.5) * self.square_size)),self.circle_radius)

    def draw_board(self):
        """
        Draw entire board on screen
        """
        self.draw_grid()
        self.draw_pieces()
        pygame.display.update()

    def drop_player_piece(self,row, column, piece):
        """
        Draw the piece that a player played
        Args:
            row: the row the player's piece is played on
            column: the column the player's piece is played on
            piece: whether player 1 or player 2 played the piece
        """
        self.board[row][column] = piece
        self.draw_board()

    def make_move(self, col, piece):
        """
        Executes a move and checks for a win
        Args:
            col: the column that the piece is placed in
            piece: whether player 1 or player 2 played the piece
        Returns: whether a move was made on the board or not
        """
        if self.ai.is_valid_location(self.board, col): # if the move is valid, place piece down and return true, or else return false
            row = next(r for r in range(6) if self.board[r][col] == 0)
            self.drop_player_piece(row, col, piece)

            if self.ai.check_win(self.board, piece, self.num_columns, self.num_rows): # checks if a player has won or not
                self.game_over = True
                self.ai.game_over = True
                self.ai.check_win(self.board, piece, self.num_columns, self.num_rows) # gets list of winning pieces

                if piece == self.PLAYER_PIECE: # player wins
                    winning_label = self.screen_font.render(f"Player 1 wins!", 1, self.pink)
                else: # player 2 / AI wins
                    winning_label = self.screen_font.render(f"Player 2 wins!", 1, self.orange)
                self.screen.blit(winning_label, (40, 10))

                # marks winning pieces on board
                for i in range(4):
                    piece_center_coordinates = ((self.ai.winning_pieces[i][1] + 0.5) * self.square_size,
                                                self.screen_width - (
                                                            self.ai.winning_pieces[i][0] + 0.5) * self.square_size)
                    triangle_coordinate_list = [
                        (piece_center_coordinates[0], piece_center_coordinates[1] - self.circle_radius),
                        (piece_center_coordinates[0] + int(self.circle_radius * math.sin(math.radians(45))),
                         piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45)))),
                        (piece_center_coordinates[0] - int(self.circle_radius * math.sin(math.radians(45))),
                         piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45))))]
                    pygame.draw.polygon(surface=self.screen, color=self.green, points=triangle_coordinate_list)
                pygame.display.update()
                return True

            self.draw_board() # draws updated board if nobody has won yet
            return True

        return False

    def ai_move(self):
        """
        Determines how the AI makes it move in single player mode
        """
        valid_moves = self.ai.get_valid_locations(self.board) # checks for any valid moves on the board
        if not valid_moves: # if there's no valid moves, the game is over and return false
            self.game_over = True
            return False

        if self.difficulty == 'easy': # easy mode: random move selection
            col = self.ai.random_move(self.board)
        elif self.difficulty == "medium": # medium mode: minmax with alpha-beta pruning
            col, _ = self.ai.minimax(self.board, self.DEPTH, self.ALPHA, self.BETA, True)
        else: # hard mode: monte carlo tree search
            col = self.ai.monte_carlo_tree_search(self.board)

        if col == -1 or col not in valid_moves: # Check if we got a valid column or else just pick the first valid move
            col = valid_moves[0] if valid_moves else 0

        self.make_move(col, self.AI_PIECE)  # AI makes the move

    def reset_game(self):
        """
        Resets the Connect 4 game after it is finished
        """
        self.game_over = False
        self.ai.game_over = False
        self.board = self.create_board()
        self.ai.winning_pieces = []

    def restart_screen(self):
        """
        This screen gives the player options to play the same game mode again, go back to the main menu to choose a
        different game mode, or quit the game
        """
        while True:
            # creating after game selection screen
            self.screen.fill(self.gray)
            play_again_button = Button(position=(self.screen_width / 2, 200), text_input="Play Again",
                                          font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            main_menu_button = Button(position=(self.screen_width / 2, 350), text_input="Main Menu",
                                        font=self.screen_font, base_color=self.blue, hovering_color=self.green)
            quit_button = Button(position=(self.screen_width / 2, 500), text_input="Quit", font=self.screen_font,
                                 base_color=self.blue, hovering_color=self.green)

            mouse_position = pygame.mouse.get_pos() # tracking mouse position in after game selection menu

            # this highlights button that mouse is currently on
            for button in [play_again_button, main_menu_button, quit_button]:
                button.change_button_color(mouse_position)
                button.update_button(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.check_for_button_input(mouse_position): # click play button restarts the game for player to play again
                        self.reset_game()
                        self.screen.fill(self.white)
                        self.draw_board()
                        self.turn = random.choice([0, 1])
                        return
                    if main_menu_button.check_for_button_input(mouse_position): # click main menu button goes back to Connect 4 main menu
                        return
                    if quit_button.check_for_button_input(mouse_position): # click quit button exits Connect 4 application
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def start_game(self):
        """
        Starts a game of Connect 4 for players until player chooses to quit or go back to main menu
        """
        # reset game before starting game
        self.reset_game()
        self.screen.fill(self.white)
        self.draw_board()
        while not self.game_over:
            if self.game_mode == "PvAI" and self.turn == 1 and not self.game_over: # If it's AI's turn, make the move automatically
                pygame.time.wait(500)  # Add a slight delay for realism
                self.ai_move()
                self.turn = 0  # Switch back to player
                if self.game_over: # if game is over, mark out winning pieces and go to restart_screen
                    for i in range(4):
                        piece_center_coordinates = ((self.ai.winning_pieces[i][1] + 0.5) * self.square_size,
                                                    self.screen_width - (
                                                                self.ai.winning_pieces[i][0] + 0.5) * self.square_size)
                        triangle_coordinate_list = [
                            (piece_center_coordinates[0], piece_center_coordinates[1] - self.circle_radius),
                            (piece_center_coordinates[0] + int(self.circle_radius * math.sin(math.radians(45))),
                             piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45)))),
                            (piece_center_coordinates[0] - int(self.circle_radius * math.sin(math.radians(45))),
                             piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45))))]
                        pygame.draw.polygon(surface=self.screen, color=self.green, points=triangle_coordinate_list)
                    pygame.time.wait(4000)
                    self.restart_screen()
                    if self.game_over: # this goes back to main menu
                        return

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION: # Make sure the piece follows the mouse
                        pygame.draw.rect(self.screen, self.white, (0, 0, self.screen_width, self.square_size))  # this keeps background of where mouse is moving to be white
                        x_position = event.pos[0] # tracking position of mouse
                        if self.turn == 0:  # Player1's turn
                            pygame.draw.circle(self.screen, self.pink, (x_position, int(self.square_size / 2)), self.circle_radius)
                        else:  # another player's turn
                            pygame.draw.circle(self.screen, self.orange, (x_position, int(self.square_size / 2)), self.circle_radius)
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.screen, self.white, (0, 0, self.screen_width, self.square_size))
                        x_position = event.pos[0]
                        col = int(math.floor(x_position / self.square_size))    # column that player will place piece down on

                        if self.make_move(col, self.turn + 1):  # current player takes turn
                            self.turn = 1 - self.turn   # Switch player
                        self.draw_board() # update board

                        if self.game_over:  # if game is over, mark out winning pieces and go to restart_screen
                            for i in range(4):
                                piece_center_coordinates = ((self.ai.winning_pieces[i][1] + 0.5) * self.square_size,
                                                            self.screen_width - (self.ai.winning_pieces[i][0] + 0.5) * self.square_size)
                                triangle_coordinate_list = [(piece_center_coordinates[0], piece_center_coordinates[1] - self.circle_radius),
                                                        (piece_center_coordinates[0] + int(self.circle_radius * math.sin(math.radians(45))), piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45)))),
                                                        (piece_center_coordinates[0] - int(self.circle_radius * math.sin(math.radians(45))), piece_center_coordinates[1] + int(self.circle_radius * math.sin(math.radians(45))))]
                                pygame.draw.polygon(surface=self.screen, color=self.green, points=triangle_coordinate_list)
                            pygame.display.update()
                            pygame.time.wait(4000)
                            self.restart_screen()
                            if self.game_over:
                                return


# Start the game
if __name__ == "__main__":
    game = Connect4Game()
    game.menu()
