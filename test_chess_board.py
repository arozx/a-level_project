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
        self.assertEqual(self.chess_board.move_count, 0)
        self.assertEqual(self.chess_board.player_turn, "white")

    def test_find_piece_coordinates(self):
        self.assertEqual(
            self.chess_board.find_piece_coordinates(self.chess_board.board[0][0]),
            (0, 0),
        )
        self.assertEqual(self.chess_board.find_piece_coordinates(None), (None, None))

    @patch("chess_board.ChessBoard.get_valid_moves")
    def test_check_move(self, mock_get_valid_moves):
        mock_get_valid_moves.return_value = []
        self.chess_board.check_move(self.chess_board.board[0][0], "0,0")
        self.assertEqual(
            self.chess_board.selected_button, self.chess_board.buttons["0,0"]
        )

    def test_are_you_in_check(self):
        self.assertEqual(self.chess_board.are_you_in_check("white"), 2)
        self.assertEqual(self.chess_board.are_you_in_check("black"), 2)

    def test_draw_square(self):
        button = self.chess_board.draw_square(0, 0)
        self.assertEqual(button.text(), "0,0")
        QTest.mouseClick(button, Qt.LeftButton)
        self.assertEqual(self.chess_board.selected_button, button)


if __name__ == "__main__":
    unittest.main()
