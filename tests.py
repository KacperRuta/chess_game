import unittest
from package.chess_game_module.game import (check_pawn_move, white_pieces_locations, black_pieces_locations,
                                            check_all_moves, check_rook_move,
                                            check_knight_move, check_bishop_move, check_queen_move, check_king_move)


class TestChessGame(unittest.TestCase):

    def setUp(self):
        """
        Setup before each test. Resets the game state to a default.
        """
        # Reset white and black piece locations to a default state
        self.default_white_pieces_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                               (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.default_black_pieces_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

        white_pieces_locations.clear()
        black_pieces_locations.clear()
        white_pieces_locations.extend(self.default_white_pieces_locations)
        black_pieces_locations.extend(self.default_black_pieces_locations)

    def test_pawn_blocked(self):
        """
        Test that a pawn cannot move forward if blocked.
        """
        # Place a black piece directly in front of a white pawn
        black_pieces_locations.append((1, 5))  # Assuming black piece is at (1, 5), blocking the white pawn at (1, 6)

        result = check_pawn_move(9, 'white')  # Index 9 corresponds to the pawn at (1, 6)
        self.assertNotIn((1, 5), result)  # Pawn should not be able to move to (1, 5)

    def test_pawn_move_starting_position(self):
        # Assuming white pawn at (1,6), expected to move to (1,5) or (1,4)
        result = check_pawn_move(9, 'white')  # Assuming 9 is the index of the pawn in white_pieces
        self.assertIn((1, 5), result)
        self.assertIn((1, 4), result)

    def test_basic_moves(self):
        """
        Smoke test to check if the basic move calculation functions run without errors.
        """
        # Test pawn move
        self.assertIsNotNone(check_pawn_move(9, 'white'))  # Assuming index 9 is a white pawn

        # Test rook move
        self.assertIsNotNone(check_rook_move(0, 'white'))  # Assuming index 0 is a white rook

        # Test knight move
        self.assertIsNotNone(check_knight_move(1, 'white'))  # Assuming index 1 is a white knight

        # Test bishop move
        self.assertIsNotNone(check_bishop_move(2, 'white'))  # Assuming index 2 is a white bishop

        # Test queen move
        self.assertIsNotNone(check_queen_move(3, 'white'))  # Assuming index 3 is a white queen

        # Test king move
        self.assertIsNotNone(check_king_move(4, 'white'))  # Assuming index 4 is a white king

        # Test all moves
        self.assertIsNotNone(check_all_moves('white'))


#if __name__ == '__main__':
   # unittest.main()
