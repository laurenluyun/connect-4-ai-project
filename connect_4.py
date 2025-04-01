import sys
import numpy as np
import pygame
import math

BLUE_COLOR = (0,0,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,255,0)

NUM_ROWS = 6
NUM_COLUMNS = 7

def create_board():
    board = np.zeros((NUM_ROWS,NUM_COLUMNS))
    return board

def drop_player_piece(board, row, column, piece):
    board[row][column] = piece
    draw_board(board)

def is_valid_location(board, column):
    return board[5][column] == 0

def get_next_open_row(board, column):
    for row in range(NUM_ROWS):
        if board[row][column] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def did_someone_win(board, piece):
    # check horizonal locations for win
    for column in range(NUM_COLUMNS-3):
        for row in range(NUM_ROWS):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True

    # check vertical locations for win
    for column in range(NUM_COLUMNS):
        for row in range(NUM_ROWS-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and board[row+3][column] == piece:
                return True

    # check positively sloped diagonals
    for column in range(NUM_COLUMNS-3):
        for row in range(NUM_ROWS-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] == piece and board[row+3][column+3] == piece:
                return True

    # check negatively sloped diagonals
    for column in range(NUM_COLUMNS-3):
        for row in range(3, NUM_ROWS):
            if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] == piece and board[row-3][column+3] == piece:
                return True
    return False

def draw_board(board):
    for column in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):
            pygame.draw.rect(screen, BLUE_COLOR, (column * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK_COLOR, (int((column + 0.5) * SQUARE_SIZE), int((row + 1.5) * SQUARE_SIZE)), CIRCLE_RADIUS)

    for column in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):
            if board[row][column] == 1:
                pygame.draw.circle(screen, RED_COLOR,(int((column + 0.5) * SQUARE_SIZE), SCREEN_HEIGHT - int((row + 0.5) * SQUARE_SIZE)), CIRCLE_RADIUS)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, YELLOW_COLOR,(int((column + 0.5) * SQUARE_SIZE), SCREEN_HEIGHT - int((row + 0.5) * SQUARE_SIZE)), CIRCLE_RADIUS)
    pygame.display.update()

board = create_board()
game_over = False
turn = 0

pygame.init()
SQUARE_SIZE = 100
SCREEN_WIDTH = NUM_COLUMNS * SQUARE_SIZE
SCREEN_HEIGHT = (NUM_ROWS + 1) * SQUARE_SIZE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CIRCLE_RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(SCREEN_SIZE)
draw_board(board)
pygame.display.update()
SCREEN_FONT = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK_COLOR, (0,0, SCREEN_WIDTH, SQUARE_SIZE))
            x_position = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED_COLOR, (x_position, int(SQUARE_SIZE/2)), CIRCLE_RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW_COLOR, (x_position, int(SQUARE_SIZE / 2)), CIRCLE_RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK_COLOR, (0,0, SCREEN_WIDTH, SQUARE_SIZE))
            x_position = event.pos[0]
            col = int(math.floor(x_position / SQUARE_SIZE))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_player_piece(board, row, col, turn+1)

                if did_someone_win(board, turn+1):
                    if turn == 0:
                        winning_label = SCREEN_FONT.render(f"Player 1 wins!", 1, RED_COLOR)
                    else:
                        winning_label = SCREEN_FONT.render(f"Player 2 wins!", 1, YELLOW_COLOR)
                    screen.blit(winning_label, (40,10))
                    game_over = True

                # print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2

            if game_over:
                pygame.time.wait(3000)