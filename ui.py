from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
import main

# UI
class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.svgWidget = QSvgWidget(parent=self)
        self.svgWidget.setGeometry(0, 0, 800, 800)
        self.svgWidget.load("board.svg")
        self.windowTitle = "Chess"

if __name__ == "__main__":
    board=main.Board()
    svg = board.printBoard("svg")
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()