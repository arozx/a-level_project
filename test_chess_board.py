# test_chess_board.py
import unittest
from unittest.mock import MagicMock, patch

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QGridLayout

from chess_board import ChessBoard

app = QApplication([])


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.layout = QGridLayout()
        self.patcher = patch(
            "sys.argv", ["test_chess_board.py", "255,255,255", "0,0,0"]
        )
        self.mock_argv = self.patcher.start()
        self.chess_board = ChessBoard(self.layout)

        self.chess_board.buttons = {
            f"{x},{y}": MagicMock() for x in range(8) for y in range(8)
        }

        # create a board with all pieces
        self.chess_board.board = [[MagicMock() for _ in range(8)] for _ in range(8)]

        # set the board to have a rook at 0,0
        self.chess_board.board[0][0] = MagicMock()

    def tearDown(self):
        self.patcher.stop()

    def test_initial_state(self):
        self.assertEqual(self.chess_board.moveCount, 0)
        self.assertEqual(self.chess_board.playerTurn, "white")

    def test_find_piece_coordinates(self):
        self.assertEqual(
            self.chess_board.find_piece_coordinates(self.chess_board.board[0][0]),
            (0, 0),
        )
        self.assertEqual(self.chess_board.find_piece_coordinates(None), (None, None))

    @patch("chess_board.ChessBoard.getValidMoves")
    def test_checkMove(self, mock_getValidMoves):
        mock_getValidMoves.return_value = []
        self.chess_board.checkMove(self.chess_board.board[0][0], "0,0")
        self.assertEqual(
            self.chess_board.selectedButton, self.chess_board.buttons["0,0"]
        )

    def test_areYouInCheck(self):
        self.assertEqual(self.chess_board.areYouInCheck("white"), 2)
        self.assertEqual(self.chess_board.areYouInCheck("black"), 2)

    def test_drawSquare(self):
        button = self.chess_board.drawSquare(0, 0)
        self.assertEqual(button.text(), "0,0")
        QTest.mouseClick(button, Qt.LeftButton)
        self.assertEqual(self.chess_board.selectedButton, button)


if __name__ == "__main__":
    unittest.main()
