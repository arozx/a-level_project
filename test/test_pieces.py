import unittest
from pieces import Rook


class TestRook(unittest.TestCase):
    def setUp(self):
        self.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        self.rook = Rook("white")

    def test_getValidMoves_emptyBoard(self):
        x = 3
        y = 3
        expected_moves = [
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7),
            (3, 2),
            (3, 1),
            (3, 0),
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
            (2, 3),
            (1, 3),
            (0, 3),
        ]
        valid_moves = self.rook.getValidMoves(self.board, x, y)
        self.assertEqual(valid_moves, expected_moves)

    def test_getValidMoves_withPieces(self):
        self.board[3][4] = Rook("black")
        self.board[3][6] = Rook("white")
        self.board[4][3] = Rook("black")
        self.board[6][3] = Rook("white")
        x = 3
        y = 3
        expected_moves = [
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 2),
            (3, 1),
            (3, 0),
            (4, 3),
            (2, 3),
            (1, 3),
            (0, 3),
        ]
        valid_moves = self.rook.getValidMoves(self.board, x, y)
        self.assertEqual(valid_moves, expected_moves)


if __name__ == "__main__":
    unittest.main()
