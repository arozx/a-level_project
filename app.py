from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


# Piece classes
class Piece:
    def __init__(self, colour):
        self.colour = colour
        self.x = int
        self.y = int


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def getValidMoves(self, board, x, y):
        valid_moves = []
        valid_moves.append((x, y))

        # Check if the square in front of the rook is empty
        for i in range(1, 8):
            if y + i <= 7:
                if board[x][y + i] is None:
                    valid_moves.append((x, y + i))
                elif board[x][y + i].colour != board[x][y].colour:
                    valid_moves.append((x, y + i))
                    break
                else:
                    break
            else:
                break

            if board[x][y + i] is not None:
                break
        # check if the square behind the rook is empty
        for i in range(1, 8):
            if y - i >= 0:
                if board[x][y - i] is None:
                    valid_moves.append((x, y - i))
                elif board[x][y - i].colour != board[x][y].colour:
                    valid_moves.append((x, y - i))
                    break
                else:
                    break
        # check if the square to the left of the rook is empty
        for i in range(1, 8):
            if x + i <= 7:
                if board[x + i][y] is None:
                    valid_moves.append((x + i, y))
                elif board[x + i][y].colour != board[x][y].colour:
                    valid_moves.append((x + i, y))
                    break
                else:
                    break
        # check if the square to the right of the rook is empty
        for i in range(1, 8):
            if x - i >= 0:
                if board[x - i][y] is None:
                    valid_moves.append((x - i, y))
                elif board[x - i][y].colour != board[x][y].colour:
                    valid_moves.append((x - i, y))
                    break
                else:
                    break
        return valid_moves


class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    # TODO fix bug where bishop is duplicated after a move
    def getValidMoves(self, board, x, y):
        valid_moves = []
        # Check diagonal up-right
        i = 1
        while x + i <= 7 and y + i <= 7:
            if board[x + i][y + i] is None:
                valid_moves.append((x + i, y + i))
            elif board[x + i][y + i].colour != self.colour:
                valid_moves.append((x + i, y + i))
                break
            else:
                break
            i += 1
        # Check diagonal up-left
        i = 1
        while x + i <= 7 and y - i >= 0:
            if board[x + i][y - i] is None:
                valid_moves.append((x + i, y - i))
            elif board[x + i][y - i].colour != self.colour:
                valid_moves.append((x + i, y - i))
                break
            else:
                break
            i += 1
        # Check diagonal down-right
        i = 1
        while x - i >= 0 and y + i <= 7:
            if board[x - i][y + i] is None:
                valid_moves.append((x - i, y + i))
            elif board[x - i][y + i].colour != self.colour:
                valid_moves.append((x - i, y + i))
                break
            else:
                break
            i += 1
        # Check diagonal down-left
        i = 1
        while x - i >= 0 and y - i >= 0:
            if board[x - i][y - i] is None:
                valid_moves.append((x - i, y - i))
            elif board[x - i][y - i].colour != self.colour:
                valid_moves.append((x - i, y - i))
                break
            else:
                break
            i += 1
        return valid_moves


class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)


class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.firstMove = True

    def getValidMoves(self, board, x, y):
        valid_moves = []
        valid_moves.append((x, y))
        # Check if the square in front of the pawn is empty
        if self.colour == "black" and x - 1 >= 0:
            if board[x - 1][y] is None:
                valid_moves.append((x - 1, y))
                # Check if the pawn is on its first move and if the square two squares in front of the pawn is empty
                if self.firstMove and x - 2 >= 0 and board[x - 2][y] is None:
                    valid_moves.append((x - 2, y))

        if self.colour == "white" and x + 1 < len(board):
            if board[x + 1][y] is None:
                valid_moves.append((x + 1, y))
                # Check if the pawn is on its first move and if the square two squares in front of the pawn is empty
                if self.firstMove and x + 2 < len(board) and board[x + 2][y] is None:
                    valid_moves.append((x + 2, y))

        # * Capturing pieces diagonally forward
        direction = 1 if self.colour == "white" else -1
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[nx]):
                if board[nx][ny] is not None and board[nx][ny].colour != self.colour:
                    valid_moves.append((nx, ny))
        return valid_moves


class ChessBoard:
    def __init__(self):
        self.moveCount = 0

        self.board = [[None for x in range(8)] for y in range(8)]
        self.buttons = {}
        self.selectedButton = None
        self.highlightedSquares = []

        # Create white pieces
        self.board[0][0] = Rook("white")
        self.board[0][1] = Knight("white")
        self.board[0][2] = Bishop("white")
        self.board[0][3] = Queen("white")
        self.board[0][4] = King("white")
        self.board[0][5] = Bishop("white")
        self.board[0][6] = Knight("white")
        self.board[0][7] = Rook("white")
        for i in range(8):
            self.board[1][i] = Pawn("white")

        # Create black pieces
        self.board[7][0] = Rook("black")
        self.board[7][1] = Knight("black")
        self.board[7][2] = Bishop("black")
        self.board[7][3] = Queen("black")
        self.board[7][4] = King("black")
        self.board[7][5] = Bishop("black")
        self.board[7][6] = Knight("black")
        self.board[7][7] = Rook("black")
        for i in range(8):
            self.board[6][i] = Pawn("black")

        #! For development purposes / Debugging
        """
        for x in range(8):
            for y in range(8):
                print(f"{self.board[x][y]} : {x} : {y} : {self.board[x][y].colour if self.board[x][y] is not None else None}")
        """

    # * Checks if a piece & square have been clicked, Then call movePiece
    def checkMove(self, piece, square):
        if piece is not None and square is not None:
            x, y = [int(i) for i in square.split(",")]
            if self.selectedButton is None:
                self.selectedButton = self.buttons[square]
                self.selectedButton.setStyleSheet(
                    "background-color: yellow; border: None"
                )
                try:
                    valid_moves = self.getValidMoves(self.board, x, y)
                    print(f"cur x = {valid_moves[0][0]} cur y = {valid_moves[0][1]}")
                except:
                    print("no valid moves")
                self.highlightSquares(piece, valid_moves)

            else:
                # TODO get the current position of the piece
                current_x = self.buttons.get(
                    self.selectedButton.objectName().split(",")[0]
                )
                current_y = self.buttons.get(
                    self.selectedButton.objectName().split(",")[1]
                )

                print(f"{current_x} : current x\n {current_y} : current y")

                # Pass new_x and new_y to highlightSquares
                # Check that the squares are defined
                if current_x is not None and current_y is not None:
                    self.drawSquare(
                        current_x, current_y
                    )  # Reset the background color of the previously selected button
                    # * deselct the currently selected button
                    self.selectedButton = None

    # Draw the board squares
    def drawSquare(self, x, y):
        button = QPushButton()
        button.setFixedSize(100, 100)

        if x is not None and y is not None:
            if (x + y) % 2 == 0:
                button.setProperty("class", "white")
                button.setStyleSheet("background-color: white; border: None")
            else:
                button.setProperty("class", "black")
                button.setStyleSheet("background-color: green; border: None")

        #! For development purposes / Debugging
        button.setText(f"{x},{y}")

        self.buttons[f"{x},{y}"] = button

        button.setObjectName(
            f"{x},{y}"
        )  # Set the objectName property to the square coordinates

        # Connect the clicked signal of the button to check if a piece and a square have been clicked
        print(
            f"{button.objectName()} : button object name, {self.board[x][y]} : {x} : {y}"
        )
        button.clicked.connect(
            lambda _, piece=self.board[x][
                y
            ], square=button.objectName(): self.checkMove(piece, square)
        )
        """
        button.clicked.disconnect(
            # TODO fix bug where the button is not deselected
        )
        """
        return button

    # Draw the chess board
    def drawBoard(self, layout):
        for x in range(8):
            for y in range(8):
                button = self.drawSquare(x, y)
                layout.addWidget(button, x, y)

        # Check if there is a piece on the square and call drawPiece
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None:
                    self.drawPiece(self.buttons[f"{x},{y}"], self.board[x][y])

    # Draw image on a button
    def drawPiece(self, button, piece):
        if piece is not None and piece.__class__.__name__ != "None":
            icon = QIcon(f"media/{piece.colour}/{piece.__class__.__name__}.svg")
            button.setIcon(icon)
            button.setIconSize(button.size())
            button.setObjectName(
                f"{piece.x},{piece.y}"
            )  # Set the objectName property to the piece coordinates
        else:
            button.setIcon(QIcon())

    # Calls the getValidMoves function of the selected piece and returns an array of valid moves
    def getValidMoves(self, board, x, y):
        x = int(x)
        y = int(y)
        if self.board[x][y] is not None:
            print(self.board[x][y].getValidMoves(board, x, y))
            return self.board[x][y].getValidMoves(board, x, y)
        else:
            return []

    def highlightSquares(self, piece, squares):
        # get the coordinates of the previously selected button
        current_x = squares[0][0]
        current_y = squares[0][1]

        # remove the coordinates of the previously selected button
        squares.pop(0)

        print(f"{self.highlightedSquares} : highlighted squares")
        for button in self.highlightedSquares:
            if button.property("class") == "white":
                button.setStyleSheet("background-color: white; border: None")
            elif button.property("class") == "black":
                button.setStyleSheet("background-color: green; border: None")

            button.clicked.disconnect()
        self.highlightedSquares = []

        # Iterate through the squares array and highlight the squares
        for square in squares:
            if isinstance(square, tuple) and len(square) == 2:
                if (
                    square[0] >= 0
                    and square[0] <= 7
                    and square[1] >= 0
                    and square[1] <= 7
                ):
                    button = self.buttons[f"{square[0]},{square[1]}"]
                    self.highlightedSquares.append(button)
                    button.setStyleSheet("background-color: blue; border: None")

                    button.clicked.connect(
                        lambda _, piece=piece, current_x=current_x, current_y=current_y, new_x=square[
                            0
                        ], new_y=square[
                            1
                        ]: self.movePiece(
                            piece, current_x, current_y, new_x, new_y
                        )
                    )

    def movePiece(self, piece, current_x, current_y, new_x, new_y):
        print(f"{self.moveCount} move count")  #! For development purposes / Debugging

        # Remove the line causing the error
        # print(f"{self.selectedButton[0].objectName()} : selected button")

        # check if the piece is not None and if it is the correct players turn
        if piece is not None:
            # Prevent the player from moving the pawn two squares twice
            if piece.__class__.__name__ == "Pawn":
                piece.firstMove = False

            self.board[current_x][current_y] = None
            self.board[new_x][new_y] = piece

            self.drawPiece(self.buttons[f"{new_x},{new_y}"], piece)
            self.drawPiece(self.buttons[f"{current_x},{current_y}"], None)

            if self.buttons[f"{current_x},{current_y}"].icon() is not None:
                self.drawPiece(self.buttons[f"{current_x},{current_y}"], None)
                # increase move count
                self.moveCount += 1
                self.playerTurn = "White" if self.moveCount % 2 == 0 else "Black"
                self.highlightSquares(
                    piece, self.getValidMoves(self.board, new_x, new_y)
                )
            else:
                print("invalid move")
        else:
            print("invalid move")
            self.highlightSquares(None, [])

        #! For development purposes / Debugging
        """
        for x in range(8):
            for y in range(8):
                print(self.board[x][y])
        """
        # check for pawn promotion
        # self.checkForPromotion()

        # * deselect the currently selected button
        self.buttons[f"{current_x},{current_y}"].setStyleSheet(
            "background-color: orange; border: None"
        )
        self.selectedButton.setStyleSheet(
            "background-color: purple; border: None"
        )  # original square

        # deslect whole board
        for i in range(0, 7):
            for j in range(0, 7):
                self.buttons[f"{i},{j}"].setDown(False)
        self.selectedButton.setDown(False)


# TODO finish pawn promotion window / UI
"""
    def checkForPromotion(self):
        # white pawn promotion
        for x in range(8):
            if isinstance(self.board[7][x], Pawn):
                self.board[7][x] = getPromotionPiece("white", x=x, y=7)
                self.drawPiece(self.buttons[f"7,{x}"], self.board[7][x])
    


# Promotion UI
class PromotionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Create buttons for each piece
        queen_btn = QPushButton('Queen')
        queen_btn.setIcon(QIcon('media/white/Queen.svg'))
        queen_btn.clicked.connect(lambda: self.piece_selected('queen'))

        rook_btn = QPushButton('Rook')
        rook_btn.setIcon(QIcon('media/white/Rook.svg'))
        rook_btn.clicked.connect(lambda: self.piece_selected('rook'))

        bishop_btn = QPushButton('Bishop')
        bishop_btn.setIcon(QIcon('media/white/Bishop.svg'))
        bishop_btn.clicked.connect(lambda: self.piece_selected('bishop'))

        knight_btn = QPushButton('Knight')
        knight_btn.setIcon(QIcon('media/white/Knight.svg'))
        knight_btn.clicked.connect(lambda: self.piece_selected('knight'))

        # Add buttons to grid layout
        grid.addWidget(queen_btn, 0, 0)
        grid.addWidget(rook_btn, 0, 1)
        grid.addWidget(bishop_btn, 1, 0)
        grid.addWidget(knight_btn, 1, 1)

        self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle('Promotion')
        self.show()

    def piece_selected(self, piece):
        self.close()
        return piece

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PromotionWindow()
    sys.exit(app.exec_())
"""


# UI
class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.windowTitle = "Chess"

        # Create layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Create chess board

        board = ChessBoard()
        board.drawBoard(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
