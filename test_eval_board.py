import unittest

from eval_board import eval_board
from pieces import Bishop, King, Knight, Pawn, Queen, Rook


class TestEvalBoard(unittest.TestCase):
    def test_eval_board_empty(self):
        # Create a sample chess board
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]

        # Set the color of the player to move
        colour = "white"

        # Call the eval_board function
        score = eval_board(board, colour)

        # Assert that the score is 0 (since the board is empty)
        self.assertEqual(score, 0)

    def test_eval_board_standard(self):
        # Case where board is standard starting position
        board = [[None] * 8 for _ in range(8)]

        board[0][0] = Rook("white")
        board[0][1] = Knight("white")
        board[0][2] = Bishop("white")
        board[0][4] = Queen("white")
        board[0][3] = King("white")
        board[0][5] = Bishop("white")
        board[0][6] = Knight("white")
        board[0][7] = Rook("white")
        for i in range(8):
            board[1][i] = Pawn("white")

        # Create black pieces
        board[7][0] = Rook("black")
        board[7][1] = Knight("black")
        board[7][2] = Bishop("black")
        board[7][4] = Queen("black")
        board[7][3] = King("black")
        board[7][5] = Bishop("black")
        board[7][6] = Knight("black")
        board[7][7] = Rook("black")
        for i in range(8):
            board[6][i] = Pawn("black")

        colour = "white"

        # Call the eval_board function
        score = eval_board(board, colour)
        self.assertEqual(score, 0)

    def test_eval_board_all_white(self):
        # Case where all pieces are white
        board = [[None] * 8 for _ in range(8)]

        board[0][0] = Rook("white")
        board[0][1] = Knight("white")
        board[0][2] = Bishop("white")
        board[0][4] = Queen("white")
        board[0][3] = King("white")
        board[0][5] = Bishop("white")
        board[0][6] = Knight("white")
        board[0][7] = Rook("white")
        for i in range(8):
            board[1][i] = Pawn("white")

        colour = "white"

        # Call the eval_board function
        score = eval_board(board, colour)
        self.assertEqual(score, 226.0)


if __name__ == "__main__":
    unittest.main()
