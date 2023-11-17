import argparse
import random
import numpy as np
import pygame
import sys
import math
import copy

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

# If a player has won, returns 1 or -1 for P1 winning and P2 winning respectively. Returns 0 if all spaces are occupied and no player won.
def check_if_winning_move(board, piece):
    
    # Check horizontally
    for col in range(4):
        for row in range(6):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                if piece == 1:
                    return 1
                elif piece == 2:
                    return -1
            
    # Check vertically
    for col in range(7):
        for row in range(3):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                if piece == 1:
                    return 1
                elif piece == 2:
                    return -1
            
    # Check diagonally (positive)
    for col in range(4):
        for row in range(3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                if piece == 1:
                    return 1
                elif piece == 2:
                    return -1
            
    # Check diagonally (negative)
    for col in range(4):
        for row in range(3, 6):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                if piece == 1:
                    return 1
                elif piece == 2:
                    return -1

    # Search board for an empty cell to confirm game is not a tie    
    tie_game = True
    for col in range(7):
        for row in range(6):
            if board[row][col] == 0.0:
                tie_game = False
                break

    # Return 0 for tie if no empty cell was found
    if tie_game: return 0

    # If game is not over, return False
    return False
            
def is_terminal(board):
    value_P1 = check_if_winning_move(board, 1)
    value_P2 = check_if_winning_move(board, 1)

    if value_P1 == 1 or value_P2 == -1:
        return True
    else:
        return False

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

# Takes a board state and returns the board state resulting from each possible move for a given player
def generate_all_possible_moves(board, player):

    new_boards = []

    if player == 1:
        for col in range(7):
            new_board = board.copy()
            row = get_next_open_row(new_board, col)
            if is_valid_location(new_board, col):
                drop_piece(new_board, row, col, 1)
                new_boards.append(new_board)
    elif player == 2:
        for col in range(7):
            new_board = board.copy()
            row = get_next_open_row(new_board, col)
            if is_valid_location(new_board, col):
                drop_piece(new_board, row, col, 2)
                new_boards.append(new_board)

    return new_boards

def evaluate_position(board, player):

    score = 0

    # Positively weight the center column
    center_arr = [int(i) for i in list(board[:, 3])]
    center_count = center_arr.count(player)
    score -= center_count * 5

    # Evaluate horizontally
    for row in range(6):
        rows = [int(i) for i in list(board[row, :])]
        for col in range(4):
            window = rows[col:col+4]
            score += evaluate_window(window, player)

    # Evaluate vertically
    for col in range(7):
        cols = [int(i) for i in list(board[:, col])]
        for row in range(3):
            window = cols[col:col+4]
            score += evaluate_window(window, player)

    # Score positive diagonals
    for row in range(3):
        for col in range(4):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score negative diagonals
    for row in range(3):
        for col in range(4):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def evaluate_window(window, player):

    score = 0

    player_piece = 1
    ai_piece = 2

    if player == 2:

        if window.count(ai_piece) == 4:
            score -= 100
        elif window.count(ai_piece) == 3 and window.count(0) == 1:
            score -= 50
        elif window.count(ai_piece) == 2 and window.count(0) == 2:
            score -= 10

        # Heavily incentivize blocking if the player has 3 in a row
        if window.count(player_piece) == 3 and window.count(0) == 1:
            score += 1000

    elif player == 1:

        if window.count(player_piece) == 4:
            score -= 100
        elif window.count(player_piece) == 3 and window.count(0) == 1:
            score -= 50
        elif window.count(player_piece) == 2 and window.count(0) == 2:
            score -= 10

        # Heavily incentivize blocking if the ai has 3 in a row
        if window.count(ai_piece) == 3 and window.count(0) == 1:
            score += 1000

    return score

# Returns the column selection with the lowest score evaluation (AI player is minimizing score)
def evaluate_all_moves(board, player):

    lowest_score = float('inf')
    best_col = float('inf')
    best_board = board

    for col in range(7):
        if is_valid_location(board, col):
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, player)
            score = evaluate_position(temp_board, player)
            if score < lowest_score:
                best_board = temp_board
                lowest_score = score

    return lowest_score, best_board

def minimax(board, alpha, beta, depth, player):
    
    terminal_check = is_terminal(board)
    if terminal_check or depth == 0:
        if terminal_check:
            # Player won, return highest score possible.
            if check_if_winning_move(board, 1) == 1:
                return 1000000000
            # AI won, return lowest score possible.
            elif check_if_winning_move(board, 2) == -1:
                return -1000000000
            else:
                return 0
        else: # Depth 0
            return evaluate_position(board, 2), board
    
    # P1 is max player. Searching for highest value.
    if player == 1:
        # Init value to largest possible
        value = float('-inf')
        best_board = board.copy()
        # Loop through states resulting from each possible column selection for P2
        for move in generate_all_possible_moves(board, 1):
            return_value = minimax(move, alpha, beta, depth - 1, 1)[0]
            if return_value > value:
                value = return_value
                best_board = move
            alpha = max(alpha, return_value)
            if beta <= alpha:
                break
        # Return the lowest value after exploring all moves, return the board state associated with that value.
        return value, best_board
    elif player == 2:
        # Init value to largest possible
        value = float('inf')
        best_board = board.copy()
        # Loop through states resulting from each possible column selection for P2
        for move in generate_all_possible_moves(board, 2):
            return_value = minimax(move, alpha, beta, depth - 1, 2)[0]
            if return_value < value:
                value = return_value
                best_board = move
            beta = min(beta, return_value)
            if beta <= alpha:
                break
        # Return the lowest value after exploring all moves, return the board state associated with that value.
        return value, best_board
    
pygame.init()

CELL_SIZE = 100

width = 700
height = 700

window_size = (width, height)

RADIUS = int(CELL_SIZE / 2 - 5)

screen = pygame.display.set_mode(window_size)

def game_loop(max_depth):

    game_board = create_board()
    game_ended = False
    turn = 0

    draw_board(game_board)
    pygame.display.update()

    font = pygame.font.SysFont("arialblack", 75)

    alpha = float('-inf')
    beta = float('inf')

    while not game_ended:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION and turn == 0:

                pygame.draw.rect(screen, WHITE, (0, 0, width, CELL_SIZE))
                pos_x = event.pos[0]

                if turn == 0:
                    pygame.draw.circle(screen, RED, (pos_x, int(CELL_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(CELL_SIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN or turn == 1:

                pygame.draw.rect(screen, WHITE, (0, 0, width, CELL_SIZE))

                # Get input from P1
                if turn == 0:

                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / CELL_SIZE))

                    if is_valid_location(game_board, col):

                        row = get_next_open_row(game_board, col)
                        drop_piece(game_board, row, col, 1)

                        # Score the player's chosen position
                        score = evaluate_position(game_board, 1)

                        # Update alpha
                        alpha = min(alpha, score)

                        win_check = check_if_winning_move(game_board, 1)

                        if win_check == 1:
                            
                            win_label = font.render("P1 Wins!", 2, RED)
                            screen.blit(win_label, (40, 10))
                            game_ended = True

                        elif win_check == 0 and win_check is not False:

                            win_label = font.render("Tie!", 2, BLUE)
                            screen.blit(win_label, (40, 10))
                            game_ended = True

                    else:
                        turn += 1

                # Get input from P2 (Minimax AI)
                else:

                    value, chosen_board = minimax(game_board, alpha, beta, max_depth, 2)

                    # Update the value of beta to the evaluation score of the chosen_board
                    beta = max(beta, score)
                    beta = value

                    game_board = chosen_board

                    win_check = check_if_winning_move(game_board, 2)

                    if win_check == -1:
                        
                        win_label = font.render("P2 Wins!", 2, YELLOW)
                        screen.blit(win_label, (40, 10))
                        game_ended = True

                    elif win_check == 0 and win_check is not False:

                        win_label = font.render("Tie!", 2, BLUE)
                        screen.blit(win_label, (40, 10))
                        game_ended = True

                turn += 1
                turn = turn % 2
    
            draw_board(game_board)

            while game_ended:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect Four game with AI using Minimax algorithm with alpha-beta pruning.")
    parser.add_argument("--depth", type=int, default=4, help="Max depth for the Minimax algorithm (4 is a good starting place).")

    args = parser.parse_args()
    max_depth = args.depth

    game_loop(max_depth)