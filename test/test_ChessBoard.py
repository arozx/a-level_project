import unittest
from ChessBoard import ChessBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()

    def test_find_piece_coordinates(self):
        # Test finding the coordinates of a piece
        piece = self.board.board[0][0]
        coordinates = self.board.find_piece_coordinates(piece)
        self.assertEqual(coordinates, (0, 0))

    def test_find_piece_coordinates_not_found(self):
        # Test finding the coordinates of a piece that does not exist on the board
        piece = None
        coordinates = self.board.find_piece_coordinates(piece)
        self.assertIsNone(coordinates)

    def test_get_valid_moves(self):
        # Test getting valid moves for a piece
        piece = self.board.board[0][0]
        valid_moves = self.board.getValidMoves(self.board.board, 0, 0)
        self.assertEqual(len(valid_moves), 0)

    def test_highlight_squares(self):
        # Test highlighting squares on the board
        piece = self.board.board[0][0]
        squares = [(1, 0), (2, 0)]
        self.board.highlightSquares(piece, squares)
        highlighted_buttons = self.board.highlightedSquares
        self.assertEqual(len(highlighted_buttons), 2)

    def test_calculate_material_score(self):
        # Test calculating the material score of the board
        score = self.board.calculateMaterialScore()
        self.assertEqual(score, 0)

    def test_are_you_in_check(self):
        # Test checking if a player is in check
        player_colour = "white"
        in_check = self.board.areYouInCheck(player_colour)
        self.assertFalse(in_check)


if __name__ == "__main__":
    unittest.main()
