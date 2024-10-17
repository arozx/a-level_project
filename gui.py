import sys

from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget

from chess_board_1 import ChessBoard


class ChessPiece(QLabel):
    def __init__(self, piece, color, parent=None):
        super().__init__(parent)
        self.piece = piece
        self.color = color
        self.setPixmap(QPixmap(f"media/{color}/{piece}.svg"))
        self.setScaledContents(True)
        self.setFixedSize(60, 60)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (
            event.pos() - self.drag_start_position
        ).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.piece)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        drag.exec_(Qt.MoveAction)


class ChessBoardUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess")
        self.setGeometry(100, 100, 480, 480)

        self.chess_board = ChessBoard()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)

        self.init_board()

    def init_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_board.board[row][col]
                if piece:
                    piece_label = ChessPiece(piece.__class__.__name__, piece.colour)
                    self.grid_layout.addWidget(piece_label, row, col)
                else:
                    empty_label = QLabel()
                    empty_label.setFixedSize(60, 60)
                    empty_label.setStyleSheet(
                        "background-color: white;"
                        if (row + col) % 2 == 0
                        else "background-color: gray;"
                    )
                    self.grid_layout.addWidget(empty_label, row, col)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        source = event.source()
        if isinstance(source, ChessPiece):
            position = event.pos()
            target_widget = self.childAt(position)
            if target_widget:
                source_pos = self.grid_layout.indexOf(source)
                target_pos = self.grid_layout.indexOf(target_widget)
                source_row, source_col = divmod(source_pos, 8)
                target_row, target_col = divmod(target_pos, 8)

                if self.chess_board.move_piece(
                    source_row, source_col, target_row, target_col
                ):
                    self.grid_layout.addWidget(source, target_row, target_col)
                    empty_label = QLabel()
                    empty_label.setFixedSize(60, 60)
                    empty_label.setStyleSheet(
                        "background-color: white;"
                        if (source_row + source_col) % 2 == 0
                        else "background-color: gray;"
                    )
                    self.grid_layout.addWidget(empty_label, source_row, source_col)
                    event.acceptProposedAction()
                else:
                    event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessBoardUI()
    window.show()
    sys.exit(app.exec_())
