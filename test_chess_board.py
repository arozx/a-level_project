import unittest
from unittest.mock import patch

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from chess_board import ChessBoard, MainWindow

app = QApplication([])


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_initial_state(self):
        self.assertEqual(self.chess_board.moveCount, 0)
        self.assertEqual(self.chess_board.playerTurn, "white")

    def test_find_piece_coordinates(self):
        self.assertEqual(
            self.chess_board.find_piece_coordinates(self.chess_board.board[0][0]),
            (0, 0),
        )
        self.assertEqual(self.chess_board.find_piece_coordinates(None), None)

    @patch("chess_board.ChessBoard.getValidMoves")
    def test_checkMove(self, mock_getValidMoves):
        mock_getValidMoves.return_value = []
        self.chess_board.checkMove(self.chess_board.board[0][0], "0,0")
        self.assertEqual(
            self.chess_board.selectedButton, self.chess_board.buttons["0,0"]
        )

    def test_calculateMaterialScore(self):
        score = self.chess_board.calculateMaterialScore()
        self.assertEqual(score, 0)

    def test_areYouInCheck(self):
        self.assertEqual(self.chess_board.areYouInCheck("white"), 0)
        self.assertEqual(self.chess_board.areYouInCheck("black"), 0)

    def test_drawSquare(self):
        button = self.chess_board.drawSquare(0, 0)
        self.assertEqual(button.text(), "0,0")

        QTest.mouseClick(button, Qt.LeftButton)
        self.assertEqual(self.chess_board.selectedButton, button)


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.main_window = MainWindow()

    def test_initial_state(self):
        self.assertEqual(self.main_window.windowTitle, "Chess")


if __name__ == "__main__":
    unittest.main()
