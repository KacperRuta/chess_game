import pygame
from typing import List, Tuple

pygame.init()

# Set the title of the pygame window
pygame.display.set_caption('CHESS')

# Define background color for the game
BACKGROUND_COLOR = 'light gray'

# Define window dimensions and create the display surface
WIDTH = 800
HEIGHT = 900
window_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(window_size)

# Define font for displaying text and colors
font = pygame.font.Font('freesansbold.ttf', 50)
winning_font = pygame.font.Font('freesansbold.ttf', 100)
font_color = 'black'
winning_font_color = 'red'

# Define colors for the chess board
LIGHT_SQUARE_COLOR = 'light gray'
DARK_SQUARE_COLOR = 'dark gray'
SEPARATING_LINE_COLOR = 'black'
HIGHLIGHTING_USED_PIECE_COLOR = 'red'
HIGHLIGHTING_LAST_MOVED_PIECE = 'yellow'
HIGHLIGHTING_MOVE_SQUARE_COLOR = 'blue'

# Define size of squares on the chess board and pieces
SQUARE_SIZE = 100
PIECE_SIZE = 80

# Load and scale chess piece images
# Black pieces
black_pawn = pygame.transform.scale(pygame.image.load('chess_pieces/black_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
black_rook = pygame.transform.scale(pygame.image.load('chess_pieces/black_rook.png'), (PIECE_SIZE, PIECE_SIZE))
black_knight = pygame.transform.scale(pygame.image.load('chess_pieces/black_knight.png'), (PIECE_SIZE, PIECE_SIZE))
black_bishop = pygame.transform.scale(pygame.image.load('chess_pieces/black_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
black_king = pygame.transform.scale(pygame.image.load('chess_pieces/black_king.png'), (PIECE_SIZE, PIECE_SIZE))
black_queen = pygame.transform.scale(pygame.image.load('chess_pieces/black_queen.png'), (PIECE_SIZE, PIECE_SIZE))

# White pieces
white_pawn = pygame.transform.scale(pygame.image.load('chess_pieces/white_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
white_rook = pygame.transform.scale(pygame.image.load('chess_pieces/white_rook.png'), (PIECE_SIZE, PIECE_SIZE))
white_knight = pygame.transform.scale(pygame.image.load('chess_pieces/white_knight.png'), (PIECE_SIZE, PIECE_SIZE))
white_bishop = pygame.transform.scale(pygame.image.load('chess_pieces/white_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
white_king = pygame.transform.scale(pygame.image.load('chess_pieces/white_king.png'), (PIECE_SIZE, PIECE_SIZE))
white_queen = pygame.transform.scale(pygame.image.load('chess_pieces/white_queen.png'), (PIECE_SIZE, PIECE_SIZE))

# Create lists of images for easier access
white_images = [white_pawn, white_rook, white_knight, white_bishop, white_king, white_queen]
black_images = [black_pawn, black_rook, black_knight, black_bishop, black_king, black_queen]
# Indexes: 0 - pawn, 1 - rook, 2 - knight, 3 - bishop, 4 - king, 5 - queen
piece_list = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']


def draw_chess_board(turn: str) -> None:
    """
    Draws the chess board on the screen.

    This function draws the chess board with alternating light and dark squares.
    It also displays the current turn or the winning message when the game ends.

    Args:
    turn (str): The current turn in the game or the game's outcome. It can be 'white',
    'black', 'white_won', or 'black_won'.
    """
    global screen, BACKGROUND_COLOR, LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR, SEPARATING_LINE_COLOR, SQUARE_SIZE, font,\
        winning_font, font_color, winning_font_color

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw each square of the chess board
    for row in range(8):
        for column in range(8):
            # Alternate colors for the squares
            color = LIGHT_SQUARE_COLOR if (row + column) % 2 == 0 else DARK_SQUARE_COLOR

            # Define the position and size of the square
            rect = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

            # Draw the square
            pygame.draw.rect(screen, color, rect)

    # Draw separating line below the chess board
    pygame.draw.rect(screen, SEPARATING_LINE_COLOR, [0, WIDTH, WIDTH, 100], 2)

    # Define text messages for different game states
    turn_text = ['WHITE TO MOVE!', 'BLACK TO MOVE!', 'WHITE WON!', 'BLACK WON!']

    # Display the appropriate message based on the game state
    if turn == 'white':
        screen.blit(font.render(turn_text[0], True, font_color), (175, 825))
    elif turn == 'black':
        screen.blit(font.render(turn_text[1], True, font_color), (175, 825))
    elif turn == 'white_won':
        screen.blit(winning_font.render(turn_text[2], True, winning_font_color), (75, 350))
        screen.blit(font.render('ZAGRAJ PONOWNIE', True, font_color), (150, 825))
    elif turn == 'black_won':
        screen.blit(winning_font.render(turn_text[3], True, winning_font_color), (75, 350))
        screen.blit(font.render('ZAGRAJ PONOWNIE', True, font_color), (150, 825))


def draw_pieces(white_pieces: List[str], white_pieces_locations: List[Tuple[int, int]],
                black_pieces: List[str], black_pieces_locations: List[Tuple[int, int]],
                turn: str, white_last_move: int, black_last_move: int, selection: int) -> None:
    """
    Draws chess pieces on the board based on their current locations.

    This function iterates through all pieces of both colors and places them on the
    board. It also highlights the last moved piece and the currently selected piece.

    Args:
    white_pieces (List[str]): A list of white piece types.
    white_pieces_locations (List[Tuple[int, int]]): A list of tuples representing the locations of white pieces.
    black_pieces (List[str]): A list of black piece types.
    black_pieces_locations (List[Tuple[int, int]]): A list of tuples representing the locations of black pieces.
    turn (str): The current turn in the game.
    white_last_move (int): Index of the last moved white piece.
    black_last_move (int): Index of the last moved black piece.
    selection (int): Index of the currently selected piece.
    """
    global screen, white_images, black_images, piece_list, HIGHLIGHTING_LAST_MOVED_PIECE, HIGHLIGHTING_USED_PIECE_COLOR

    # Draw white pieces on the board
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_pieces_locations[i][0] * 100 + 10,
                                          white_pieces_locations[i][1] * 100 + 10))

        # Highlight the last moved piece and the selected piece for white
        if turn == 'white':
            if black_last_move == i:
                pygame.draw.rect(screen, HIGHLIGHTING_LAST_MOVED_PIECE,
                                 [black_pieces_locations[i][0] * 100 + 1,
                                  black_pieces_locations[i][1] * 100 + 1, 98, 98], 2)
            if selection == i:
                pygame.draw.rect(screen, HIGHLIGHTING_USED_PIECE_COLOR,
                                 [white_pieces_locations[i][0] * 100 + 1,
                                  white_pieces_locations[i][1] * 100 + 1, 98, 98], 2)

    # Draw black pieces on the board
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_pieces_locations[i][0] * 100 + 10,
                                          black_pieces_locations[i][1] * 100 + 10))

        # Highlight the last moved piece and the selected piece for black
        if turn == 'black':
            if white_last_move == i:
                pygame.draw.rect(screen, HIGHLIGHTING_LAST_MOVED_PIECE,
                                 [white_pieces_locations[i][0] * 100 + 1,
                                  white_pieces_locations[i][1] * 100 + 1, 98, 98], 2)
            if selection == i:
                pygame.draw.rect(screen, HIGHLIGHTING_USED_PIECE_COLOR,
                                 [black_pieces_locations[i][0] * 100 + 1,
                                  black_pieces_locations[i][1] * 100 + 1, 98, 98], 2)


def draw_valid_moves(valid_moves: List[Tuple[int, int]]) -> None:
    """
    Draws highlighting squares on the chess board for valid moves.

    This function iterates over a list of valid moves and highlights each corresponding square on the board.
    It's used to visually indicate to the player where a selected piece can legally move.

    Args:
    valid_moves (List[Tuple[int, int]]): A list of tuples where each tuple represents the coordinates (x, y)
    of a valid move on the chess board.
    """
    global screen, HIGHLIGHTING_MOVE_SQUARE_COLOR, SQUARE_SIZE

    # Iterate through the valid moves and draw a highlighting rectangle on each
    for move in valid_moves:
        pygame.draw.rect(screen, HIGHLIGHTING_MOVE_SQUARE_COLOR,
                         [move[0] * SQUARE_SIZE + 1, move[1] * SQUARE_SIZE + 1,
                          SQUARE_SIZE - 2, SQUARE_SIZE - 2], 2)
