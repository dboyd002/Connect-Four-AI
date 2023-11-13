import numpy as np
import pygame
import sys
import math

BLUE = (52, 134, 235)
WHITE = (255, 255, 255)
RED = (235, 52, 73)
YELLOW = (235, 195, 52)

def create_board():

    board = np.zeros((6, 7))
    return board

def drop_piece(board, row, col, piece):

    # Place a piece represented by '1' or '2' depending on the player in a given [row][col] index on the board.
    board[row][col] = piece

def is_valid_location(board, col):

    # Returns False if all rows of a given col are filled.
    return board[5][col] == 0

def get_next_open_row(board, col):

    # Starting from the bottom, loop through each row of a given column checking if it is vacant.
    # The first vacancy will be returned resulting in the next open row.
    for row in range(6):
        if board[row][col] == 0:
            return row
        
def print_board(board):

    print(np.flip(board, 0))

def check_if_winning_move(board, piece):
    
    # Check horizontally
    for col in range(4):
        for row in range(6):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                return True
            
    # Check vertically
    for col in range(7):
        for row in range(3):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                return True
            
    # Check diagonally (positive)
    for col in range(4):
        for row in range(3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                return True
            
    # Check diagonally (negative)
    for col in range(4):
        for row in range(3, 6):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                return True
            
def draw_board(board):

    for col in range(7):
        for row in range(6):
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, WHITE, ((int(col * CELL_SIZE + CELL_SIZE / 2)), int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)

    for col in range(7):
        for row in range(6):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, ((int(col * CELL_SIZE + CELL_SIZE / 2)), (height + CELL_SIZE) - int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, ((int(col * CELL_SIZE + CELL_SIZE / 2)), (height + CELL_SIZE) - int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    
    pygame.display.update()

game_board = create_board()
print_board(game_board)
game_ended = False
turn = 0

pygame.init()

CELL_SIZE = 100

width = 700
height = 700

window_size = (width, height)

RADIUS = int(CELL_SIZE / 2 - 5)

screen = pygame.display.set_mode(window_size)

draw_board(game_board)
pygame.display.update()

font = pygame.font.SysFont("arialblack", 75)

while not game_ended:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:

            pygame.draw.rect(screen, WHITE, (0, 0, width, CELL_SIZE))
            pos_x = event.pos[0]

            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(CELL_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(CELL_SIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.draw.rect(screen, WHITE, (0, 0, width, CELL_SIZE))

            # Get input from P1
            if turn == 0:

                pos_x = event.pos[0]
                col = int(math.floor(pos_x / CELL_SIZE))

                if is_valid_location(game_board, col):

                    row = get_next_open_row(game_board, col)
                    drop_piece(game_board, row, col, 1)

                    if check_if_winning_move(game_board, 1):
                        
                        win_label = font.render("P1 Wins!", 1, RED)
                        screen.blit(win_label, (40, 10))
                        game_ended = True

                else:
                    turn += 1

            # Get input from P2
            else:

                pos_x = event.pos[0]
                col = int(math.floor(pos_x / CELL_SIZE))

                if is_valid_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    drop_piece(game_board, row, col, 2)

                    if check_if_winning_move(game_board, 2):
                        
                        win_label = font.render("P2 Wins!", 2, YELLOW)
                        screen.blit(win_label, (40, 10))
                        game_ended = True

                else:
                    turn += 1

            turn += 1
            turn = turn % 2
 
        print_board(game_board)
        draw_board(game_board)

        while game_ended:
            pass