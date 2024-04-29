from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget


class PromotionWindow(QWidget):
    pieceSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Create buttons for each piece
        queen_btn = QPushButton("Queen")
        queen_btn.setIcon(QIcon("media/white/Queen.svg"))
        queen_btn.clicked.connect(lambda: self.pieceSelected.emit("Queen"))

        rook_btn = QPushButton("Rook")
        rook_btn.setIcon(QIcon("media/white/Rook.svg"))
        rook_btn.clicked.connect(lambda: self.pieceSelected.emit("Rook"))

        bishop_btn = QPushButton("Bishop")
        bishop_btn.setIcon(QIcon("media/white/Bishop.svg"))
        bishop_btn.clicked.connect(lambda: self.pieceSelected.emit("Bishop"))

        knight_btn = QPushButton("Knight")
        knight_btn.setIcon(QIcon("media/white/Knight.svg"))
        knight_btn.clicked.connect(lambda: self.pieceSelected.emit("Knight"))

        # Add buttons to grid layout
        grid.addWidget(queen_btn, 0, 0)
        grid.addWidget(rook_btn, 0, 1)
        grid.addWidget(bishop_btn, 1, 0)
        grid.addWidget(knight_btn, 1, 1)

        self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle("Promotion")
        self.show()
