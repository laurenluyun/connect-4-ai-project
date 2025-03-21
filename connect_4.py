import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # check horizonal locations for win
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True

    # check vertical locations for win
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and board[row+3][column] == piece:
                return True

    # check positively sloped diagonals
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] == piece and board[row+3][column+3] == piece:
                return True

    # check negatively sloped diagonals
    for column in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] == piece and board[row-3][column+3] == piece:
                return True

board = create_board()
game_over = False
turn = 0

while not game_over:
    # ask for player 1 input
    if turn == 0:
        col = int(input("Player 1 Make your Selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                game_over = True

    # ask for player 2 input
    else:
        col = int(input("Player 2 Make your Selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                game_over = True

    turn += 1
    turn = turn % 2
