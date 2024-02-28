import unittest
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PromotionWindow import PromotionWindow


class TestPromotionWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def tearDown(self):
        self.app.quit()

    def test_piece_selected(self):
        window = PromotionWindow()
        window.show()

        # Simulate clicking the Queen button
        queen_btn = window.findChild(QPushButton, "queen_btn")
        QTest.mouseClick(queen_btn, Qt.LeftButton)

        # Check if the piece selected signal is emitted
        self.assertEqual(window.selected_piece, "Queen")

        # Simulate clicking the Rook button
        rook_btn = window.findChild(QPushButton, "rook_btn")
        QTest.mouseClick(rook_btn, Qt.LeftButton)

        # Check if the piece selected signal is emitted
        self.assertEqual(window.selected_piece, "Rook")

        # Simulate clicking the Bishop button
        bishop_btn = window.findChild(QPushButton, "bishop_btn")
        QTest.mouseClick(bishop_btn, Qt.LeftButton)

        # Check if the piece selected signal is emitted
        self.assertEqual(window.selected_piece, "Bishop")

        # Simulate clicking the Knight button
        knight_btn = window.findChild(QPushButton, "knight_btn")
        QTest.mouseClick(knight_btn, Qt.LeftButton)

        # Check if the piece selected signal is emitted
        self.assertEqual(window.selected_piece, "Knight")


if __name__ == "__main__":
    unittest.main()
