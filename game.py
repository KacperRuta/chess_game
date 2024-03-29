import pygame
from package.chess_game_module.board_drawing import draw_chess_board, draw_pieces, draw_valid_moves
from typing import List, Tuple

pygame.init()

# list of all starting pieces and their locations
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_pieces_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                          (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_pieces_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                          (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

turn = 'white'  # black's or white's turn
selection = None
white_pre_last_move = None  # for checking en-passant, will contain only number of a row
white_last_move = None
black_pre_last_move = None
black_last_move = None
valid_moves = []  # valid moves of a selected piece
black_valid_moves = []  # list of all black valid moves
white_valid_moves = []  # list of all white valid moves
king_moved = [0, 0]

TIMER = pygame.time.Clock()
FPS = 60


# CHECKING MOVES:
def check_pawn_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
    Calculates valid moves for a pawn at a given position.

    This function considers normal pawn moves (single and double steps),
    capturing moves, and special moves like en-passant.

    Args:
    i (int): Index of the pawn in the piece list.
    color (str): Color of the pawn ('white' or 'black').

    Returns:
    list: A list of tuples representing valid moves for the pawn.
    """
    piece_move_list = []

    # Process moves for white pawns
    if color == 'white':
        # Check normal pawn moves and double step from starting position
        if ((white_pieces_locations[i][0], white_pieces_locations[i][1] - 1) not in white_pieces_locations and
                (white_pieces_locations[i][0], white_pieces_locations[i][1] - 1) not in black_pieces_locations):
            piece_move_list.append((white_pieces_locations[i][0], white_pieces_locations[i][1] - 1))
            if white_pieces_locations[i][1] == 6 and (white_pieces_locations[i][0], white_pieces_locations[i][1] - 2) \
                    not in white_pieces_locations and (white_pieces_locations[i][0], white_pieces_locations[i][1] - 2) \
                    not in black_pieces_locations:
                piece_move_list.append((white_pieces_locations[i][0], white_pieces_locations[i][1] - 2))
        # Check capturing moves and en-passant for white pawns
        if (white_pieces_locations[i][0] - 1, white_pieces_locations[i][1] - 1) in black_pieces_locations:
            piece_move_list.append((white_pieces_locations[i][0] - 1, white_pieces_locations[i][1] - 1))
        if (white_pieces_locations[i][0] + 1, white_pieces_locations[i][1] - 1) in black_pieces_locations:
            piece_move_list.append((white_pieces_locations[i][0] + 1, white_pieces_locations[i][1] - 1))
        # en-passant mechanics
        if black_last_move is not None:
            if (white_pieces_locations[i][1] == 3 and black_pieces_locations[black_last_move][0] ==
                    white_pieces_locations[i][0] - 1 and black_pieces_locations[black_last_move][1] == 3 and
                    black_pieces[black_last_move] == 'pawn' and black_pre_last_move == 1):
                piece_move_list.append((white_pieces_locations[i][0] - 1, white_pieces_locations[i][1] - 1))
            if (white_pieces_locations[i][1] == 3 and black_pieces_locations[black_last_move][0] ==
                    white_pieces_locations[i][0] + 1 and black_pieces_locations[black_last_move][1] == 3 and
                    black_pieces[black_last_move] == 'pawn' and black_pre_last_move == 1):
                piece_move_list.append((white_pieces_locations[i][0] + 1, white_pieces_locations[i][1] - 1))

    # Process moves for black pawns
    if color == 'black':
        # Check normal pawn moves and double step from starting position
        if ((black_pieces_locations[i][0], black_pieces_locations[i][1] + 1) not in black_pieces_locations and
                (black_pieces_locations[i][0], black_pieces_locations[i][1] + 1) not in white_pieces_locations):
            piece_move_list.append((black_pieces_locations[i][0], black_pieces_locations[i][1] + 1))
            if (black_pieces_locations[i][1] == 1 and (black_pieces_locations[i][0], black_pieces_locations[i][1] + 2)
                    not in black_pieces_locations and (black_pieces_locations[i][0], black_pieces_locations[i][1] + 2)
                    not in white_pieces_locations):
                piece_move_list.append((black_pieces_locations[i][0], black_pieces_locations[i][1] + 2))
        # Check capturing moves and en-passant for black pawns
        if (black_pieces_locations[i][0] - 1, black_pieces_locations[i][1] + 1) in white_pieces_locations:
            piece_move_list.append((black_pieces_locations[i][0] - 1, black_pieces_locations[i][1] + 1))
        if (black_pieces_locations[i][0] + 1, black_pieces_locations[i][1] + 1) in white_pieces_locations:
            piece_move_list.append((black_pieces_locations[i][0] + 1, black_pieces_locations[i][1] + 1))
        # en-passant mechanics
        if white_last_move is not None:
            if (black_pieces_locations[i][1] == 4 and white_pieces_locations[white_last_move][0] ==
                    black_pieces_locations[i][0] - 1 and white_pieces_locations[white_last_move][1] == 4 and
                    white_pieces[white_last_move] == 'pawn' and white_pre_last_move == 6):
                piece_move_list.append((black_pieces_locations[i][0] - 1, black_pieces_locations[i][1] + 1))
            if (black_pieces_locations[i][1] == 4 and white_pieces_locations[white_last_move][0] ==
                    black_pieces_locations[i][0] + 1 and white_pieces_locations[white_last_move][1] == 4 and
                    white_pieces[white_last_move] == 'pawn' and white_pre_last_move == 6):
                piece_move_list.append((black_pieces_locations[i][0] + 1, black_pieces_locations[i][1] + 1))

    return piece_move_list


def check_rook_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
    Calculates valid moves for a rook at a given position.

    This function considers all possible straight-line moves for the rook,
    stopping at the first piece encountered in each direction. It includes
    moves where the rook captures an opponent's piece.

    Args:
    i (int): Index of the rook in the piece list.
    color (str): Color of the rook ('white' or 'black').

    Returns:
    List[Tuple[int, int]]: A list of tuples representing valid moves for the rook.
    """

    def add_rook_moves(piece_locations: List[Tuple[int, int]], opponent_locations: List[Tuple[int, int]], dx: int,
                       dy: int) -> List[Tuple[int, int]]:
        """
        Helper function to add valid rook moves in a given direction.

        Args:
        piece_locations (List[Tuple[int, int]]): Locations of the player's pieces.
        opponent_locations (List[Tuple[int, int]]): Locations of the opponent's pieces.
        dx (int): Delta x, the horizontal direction of movement.
        dy (int): Delta y, the vertical direction of movement.

        Returns:
        List[Tuple[int, int]]: Valid moves in the specified direction.
        """
        moves = []
        for index in range(1, 8):
            new_x, new_y = piece_locations[i][0] + dx * index, piece_locations[i][1] + dy * index
            if (new_x, new_y) in piece_locations or not 0 <= new_y < 8:
                break
            moves.append((new_x, new_y))
            if (new_x, new_y) in opponent_locations:
                break
        return moves

    if color == 'white':
        own_pieces, opponent_pieces = white_pieces_locations, black_pieces_locations
    else:
        own_pieces, opponent_pieces = black_pieces_locations, white_pieces_locations

    # list 'directions' stores tuples representing the four directions a rook can move: up, down, left, and right
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    piece_move_list = [move for dx, dy in directions for move in add_rook_moves(own_pieces, opponent_pieces, dx, dy)]

    return piece_move_list


def check_knight_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
    Calculates valid moves for a knight at a given position.

    This function considers all possible L-shaped moves for the knight,
    ensuring that it does not move onto a square occupied by a piece of the same color.

    Args:
    i (int): Index of the knight in the piece list.
    color (str): Color of the knight ('white' or 'black').

    Returns:
    List[Tuple[int, int]]: A list of tuples representing valid moves for the knight.
    """
    # list stores tuples representing all possible knight moves:
    knight_moves = [(-2, -1), (-1, -2), (-1, 2), (-2, 1), (1, -2), (2, -1), (2, 1), (1, 2)]
    # Determine the piece locations based on the color
    if color == 'white':
        own_pieces, board_limit = white_pieces_locations, 8
    else:
        own_pieces, board_limit = black_pieces_locations, 8

    piece_move_list = [(own_pieces[i][0] + dx, own_pieces[i][1] + dy)
                       for dx, dy in knight_moves
                       if (own_pieces[i][0] + dx, own_pieces[i][1] + dy) not in own_pieces and
                       0 <= own_pieces[i][1] + dy < board_limit]

    return piece_move_list


def check_bishop_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
        Calculates valid moves for a bishop at a given position.

        This function considers all possible diagonal moves for the bishop,
        stopping at the first piece encountered in each direction. It includes
        moves where the bishop captures an opponent's piece.

        Args:
        i (int): Index of the bishop in the piece list.
        color (str): Color of the bishop ('white' or 'black').
        Returns:
        List[Tuple[int, int]]: A list of tuples representing valid moves for the bishop.
    """

    def add_bishop_moves(own_locations: List[Tuple[int, int]], opponent_locations: List[Tuple[int, int]], dx: int,
                         dy: int) -> List[Tuple[int, int]]:
        """
           Helper function to add valid bishop moves in a given diagonal direction.

           Args:
           own_locations (List[Tuple[int, int]]): Locations of the player's pieces.
           opponent_locations (List[Tuple[int, int]]):
            Locations of the opponent's pieces.
            dx (int): Delta x, the horizontal direction of movement.
            dy (int): Delta y, the vertical direction of movement.

           Returns:
           List[Tuple[int, int]]: Valid moves in the specified diagonal direction.
           """
        moves = []
        for index in range(1, 8):
            new_x, new_y = own_locations[i][0] + dx * index, own_locations[i][1] + dy * index
            if (new_x, new_y) in own_locations or not 0 <= new_y < 8:
                break
            moves.append((new_x, new_y))
            if (new_x, new_y) in opponent_locations:
                break
        return moves

    if color == 'white':
        own_pieces, opponent_pieces = white_pieces_locations, black_pieces_locations
    else:
        own_pieces, opponent_pieces = black_pieces_locations, white_pieces_locations

    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # Diagonal directions
    piece_move_list = [move for dx, dy in directions for move in add_bishop_moves(own_pieces, opponent_pieces, dx, dy)]

    return piece_move_list


def check_queen_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
    Calculates valid moves for a queen at a given position.

    This function combines the moves of a rook and a bishop, as the queen's movement
    is a combination of both these pieces. It includes all possible straight-line and
    diagonal moves, stopping at the first piece encountered in each direction and
    including captures of opponent's pieces.

    Args:
    i (int): Index of the queen in the piece list.
    color (str): Color of the queen ('white' or 'black').

    Returns:
    List[Tuple[int, int]]: A list of tuples representing valid moves for the queen.
    """

    # Combine rook and bishop moves to get queen's moves
    piece_move_list = check_rook_move(i, color) + check_bishop_move(i, color)

    return piece_move_list


def check_king_move(i: int, color: str) -> List[Tuple[int, int]]:
    """
       Calculates valid moves for a king at a given position.

       This function considers all possible one-square moves around the king in all directions.
       It also includes castling moves if the conditions are met (king and rook have not moved,
       there are no pieces between them and there is no valid enemy piece move in any of castling squares).

       Args:
       i (int): Index of the king in the piece list.
       color (str): Color of the king ('white' or 'black').

       Returns:
       List[Tuple[int, int]]: A list of tuples representing valid moves for the king.
    """

    def king_moves(piece_locations: List[Tuple[int, int]], dx_dy: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Helper function to add valid king moves.

        Args:
        piece_locations (List[Tuple[int, int]]): Locations of the player's pieces.
        dx_dy (List[Tuple[int, int]]): List of tuples representing move directions.

        Returns:
        List[Tuple[int, int]]: Valid moves for the king.
        """
        moves = []
        for dx, dy in dx_dy:
            new_x, new_y = piece_locations[i][0] + dx, piece_locations[i][1] + dy
            if (new_x, new_y) not in piece_locations and 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append((new_x, new_y))

        # Castling logic here
        if color == 'white':
            if king_moved[0] == 0 and (white_pieces_locations[i][0], white_pieces_locations[i][1]) == (3, 7) and (
                    3, 7) not in black_valid_moves:
                if (0, 7) in white_pieces_locations:
                    index1 = white_pieces_locations.index((0, 7))
                if (7, 7) in white_pieces_locations:
                    index2 = white_pieces_locations.index((7, 7))
                if (0, 7) in white_pieces_locations and white_pieces[index1] == 'rook':
                    if (1, 7) not in white_pieces_locations and (1, 7) not in black_valid_moves and (
                            1, 7) not in black_pieces_locations and (2, 7) not in white_pieces_locations and (
                            2, 7) not in black_valid_moves and (2, 7) not in black_pieces_locations:
                        moves.append((1, 7))
                if (7, 7) in white_pieces_locations and white_pieces[index2] == 'rook':
                    if (4, 7) not in white_pieces_locations and (4, 7) not in black_valid_moves and (
                            4, 7) not in black_pieces_locations and (5, 7) not in white_pieces_locations and (
                            5, 7) not in black_valid_moves and (5, 7) not in black_pieces_locations and (
                            6, 7) not in white_pieces_locations and (6, 7) not in black_valid_moves and (
                            6, 7) not in black_pieces_locations:
                        moves.append((6, 7))
        else:
            if king_moved[1] == 0 and (black_pieces_locations[i][0], black_pieces_locations[i][1]) == (3, 0) and (
                    3, 0) not in white_valid_moves:
                if (0, 0) in black_pieces_locations:
                    index1 = black_pieces_locations.index((0, 0))
                if (7, 0) in black_pieces_locations:
                    index2 = black_pieces_locations.index((7, 0))
                if (0, 0) in black_pieces_locations and black_pieces[index1] == 'rook':
                    if (1, 0) not in black_pieces_locations and (1, 0) not in white_valid_moves and (
                            1, 0) not in white_pieces_locations and (2, 0) not in black_pieces_locations and (
                            2, 0) not in white_valid_moves and (2, 0) not in white_pieces_locations:
                        moves.append((1, 0))
                if (7, 0) in black_pieces_locations and black_pieces[index2] == 'rook':
                    if (4, 0) not in black_pieces_locations and (4, 0) not in white_valid_moves and (
                            4, 0) not in white_pieces_locations and (5, 0) not in black_pieces_locations and (
                            5, 0) not in white_valid_moves and (5, 0) not in white_pieces_locations and (
                            6, 0) not in black_pieces_locations and (6, 0) not in white_valid_moves and (
                            6, 0) not in white_pieces_locations:
                        moves.append((6, 0))

        return moves

    # All 8 directions around the king
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if color == 'white':
        return king_moves(white_pieces_locations, directions)
    else:
        return king_moves(black_pieces_locations, directions)


def check_all_moves(color: str) -> List[List[Tuple[int, int]]]:
    """
    Calculates all valid moves for all pieces of the specified color.

    This function iterates through each piece of the given color and
    accumulates a list of valid moves for each piece, considering the type
    of each piece (pawn, rook, knight, bishop, king, queen).

    Args:
    color (str): Color of the pieces ('white' or 'black').

    Returns:
    List[List[Tuple[int, int]]]: A list containing lists of tuples, where each inner list
    represents valid moves for a single piece and each tuple represents a move's coordinates.
    """

    piece_move_list = []  # List of moves for one chess piece
    all_move_list = []  # List of moves for all pieces of one color

    # Assign the correct piece set based on color
    pieces = white_pieces if color == 'white' else black_pieces

    # Iterate through each piece and accumulate their valid moves
    for i in range(len(pieces)):
        if pieces[i] == 'pawn':
            piece_move_list = check_pawn_move(i, color)
        elif pieces[i] == 'rook':
            piece_move_list = check_rook_move(i, color)
        elif pieces[i] == 'knight':
            piece_move_list = check_knight_move(i, color)
        elif pieces[i] == 'bishop':
            piece_move_list = check_bishop_move(i, color)
        elif pieces[i] == 'king':
            piece_move_list = check_king_move(i, color)
        elif pieces[i] == 'queen':
            piece_move_list = check_queen_move(i, color)

        all_move_list.append(piece_move_list)

    return all_move_list


def check_valid_moves() -> List[Tuple[int, int]]:
    """
    Retrieves valid moves for the currently selected piece based on the turn.

    This function checks which player's turn it is and returns the valid moves for
    the selected piece from that player's valid moves list.

    Returns:
    List[Tuple[int, int]]: A list of tuples representing valid moves for the selected piece.
    """
    global selection, white_valid_moves, black_valid_moves, turn

    if turn == 'white':
        return white_valid_moves[selection]
    else:
        return black_valid_moves[selection]


def start():
    global turn, white_pieces, white_pieces_locations, black_pieces, black_pieces_locations, white_last_move, black_last_move, selection, white_valid_moves, black_valid_moves, valid_moves, white_pre_last_move, black_pre_last_move
    # Main game loop
    run = True
    while run:
        TIMER.tick(FPS)

        # Draw the chess board and the pieces
        draw_chess_board(turn)
        draw_pieces(white_pieces, white_pieces_locations, black_pieces, black_pieces_locations, turn, white_last_move,
                    black_last_move, selection)

        # Handle piece selection and valid move display
        if selection is not None:
            valid_moves = check_valid_moves()
            draw_valid_moves(valid_moves)

        # Winning condition handling
        if turn != 'white' and turn != 'black':
            draw_chess_board(turn)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    y = event.pos[1] // 100
                    if y == 8:
                        # Restart the game logic here
                        turn = 'white'
                        white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        white_pieces_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

                        black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        black_pieces_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                        white_last_move = None
                        black_last_move = None
                        break

        # Game event handling
        for event in pygame.event.get():
            # Quitting event handling
            if event.type == pygame.QUIT:
                run = False
            # Clicking on board event handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0] // 100
                y = event.pos[1] // 100
                click_position = (x, y)

                # Update valid moves for each color
                black_valid_moves = check_all_moves('black')
                white_valid_moves = check_all_moves('white')

                # Player turn handling and piece movement logic
                if turn == 'white':
                    # White player's turn logic
                    # Includes selection, movement, special moves (e.g., en-passant, castling), and capture handling
                    if click_position in white_pieces_locations:
                        selection = white_pieces_locations.index(click_position)
                        white_pre_last_move = y
                    if click_position in valid_moves and selection is not None:
                        white_pieces_locations[selection] = click_position
                        white_last_move = selection
                        # Promoting
                        if white_pieces[white_last_move] == 'pawn' and white_pieces_locations[selection][1] == 0:
                            white_pieces[white_last_move] = 'queen'
                        # En-passant handling
                        if (black_last_move is not None and white_pieces[white_last_move] == 'pawn' and
                                white_pieces_locations[selection] ==
                                (black_pieces_locations[black_last_move][0],
                                 black_pieces_locations[black_last_move][1] - 1)):
                            black_pieces.pop(black_last_move)
                            black_pieces_locations.pop(black_last_move)
                        # Castle handling
                        if (white_pieces[white_last_move] == 'king' and white_pieces_locations[white_last_move] == (
                                1, 7)
                                and king_moved[0] == 0):
                            white_pieces_locations[white_pieces_locations.index((0, 7))] = (2, 7)
                        if (white_pieces[white_last_move] == 'king' and white_pieces_locations[white_last_move] == (
                                6, 7)
                                and king_moved[0] == 0):
                            white_pieces_locations[white_pieces_locations.index((7, 7))] = (5, 7)
                        if white_pieces[white_last_move] == 'king':
                            king_moved[0] = 1

                        # Capturing piece handling
                        if click_position in black_pieces_locations:
                            black_pieces.pop(black_pieces_locations.index(click_position))
                            black_pieces_locations.pop(black_pieces_locations.index(click_position))
                        black_valid_moves = check_all_moves('black')
                        white_valid_moves = check_all_moves('white')

                        if 'king' not in black_pieces:
                            turn = 'white_won'
                            break

                        turn = 'black'
                        selection = None
                        valid_moves = []
                        draw_chess_board(turn)
                        draw_pieces(white_pieces, white_pieces_locations, black_pieces, black_pieces_locations, turn,
                                    white_last_move,
                                    black_last_move, selection)
                else:
                    # Black player's turn logic
                    # Similar to white's logic with appropriate adjustments for black pieces
                    if click_position in black_pieces_locations:
                        selection = black_pieces_locations.index(click_position)
                        black_pre_last_move = y
                    if click_position in valid_moves and selection is not None:
                        black_pieces_locations[selection] = click_position
                        black_last_move = selection
                        # Promoting
                        if black_pieces[white_last_move] == 'pawn' and black_pieces_locations[selection][1] == 7:
                            black_pieces[white_last_move] = 'queen'
                        # En passant
                        if (white_last_move is not None and black_pieces[black_last_move] == 'pawn' and
                                black_pieces_locations[selection] ==
                                (white_pieces_locations[white_last_move][0],
                                 white_pieces_locations[white_last_move][1] + 1)):
                            white_pieces.pop(white_last_move)
                            white_pieces_locations.pop(white_last_move)
                        # Castle
                        if (black_pieces[black_last_move] == 'king' and black_pieces_locations[black_last_move] == (
                                1, 0)
                                and king_moved[1] == 0):
                            black_pieces_locations[black_pieces_locations.index((0, 0))] = (2, 0)
                        if (black_pieces[black_last_move] == 'king' and black_pieces_locations[black_last_move] == (
                                6, 0)
                                and king_moved[1] == 0):
                            black_pieces_locations[black_pieces_locations.index((7, 0))] = (5, 0)
                        if black_pieces[black_last_move] == 'king':
                            king_moved[1] = 1
                        # Capturing
                        if click_position in white_pieces_locations:
                            white_pieces.pop(white_pieces_locations.index(click_position))
                            white_pieces_locations.pop(white_pieces_locations.index(click_position))
                        black_valid_moves = check_all_moves('black')
                        white_valid_moves = check_all_moves('white')

                        if 'king' not in white_pieces:
                            turn = 'black_won'
                            break

                        turn = 'white'
                        selection = None
                        valid_moves = []

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start()
