from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PromotionWindow import *
from pieces import *
import logging


class ChessBoard:
    def __init__(self):
        self.moveCount = 0
        self.playerTurn = "white"

        self.board = [[None for x in range(8)] for y in range(8)]
        self.buttons = {}
        self.selectedButton = None
        self.highlightedSquares = []

        self.promotionWindow = None

        # Create white pieces
        self.board[0][0] = Rook("white")
        self.board[0][1] = Knight("white")
        self.board[0][2] = Bishop("white")
        self.board[0][3] = Queen("white")
        self.board[0][4] = King("white")
        self.board[0][5] = Bishop("white")
        self.board[0][6] = Knight("white")
        self.board[0][7] = Rook("white")
        for i in range(1, 8):
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

    def find_piece_coordinates(self, piece):
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == piece:
                    return x, y
        return None  # Return None if the piece is not found

    # Checks if a piece & square have been clicked, Then call movePiece
    def checkMove(self, piece, square):
        print(f"CheckMove; Piece: {piece} : Square: {square}")
        if piece is not None and square is not None:
            x, y = [int(i) for i in square.split(",")]
            if self.selectedButton is None:
                self.selectedButton = self.buttons[square]
                self.selectedButton.setStyleSheet(
                    "background-color: yellow; border: None"
                )
                """
                if (
                    self.board[x][y] is not None
                    and self.board[x][y].colour == self.playerTurn
                ):
                    print(f"{self.board[x][y].__class__.__name__} : is the same colour")
                else:
                    print(
                        f"{self.board[x][y].__class__.__name__} : is not the same colour"
                    )
                """
                try:
                    valid_moves = self.getValidMoves(self.board, x, y)
                    print(f"cur x = {valid_moves[0][0]} cur y = {valid_moves[0][1]}")
                except:
                    logging.error("No valid moves")
                self.highlightSquares(piece, valid_moves)

            else:
                current_x, current_y = self.find_piece_coordinates(piece)
                print(f"{current_x} : current x\n {current_y} : current y")

                # Pass new_x and new_y to highlightSquares
                # Check that the squares are defined
                if current_x is not None and current_y is not None:
                    self.drawSquare(current_x, current_y)  # Reset the background colour
                    # Deselct the current button
                    self.selectedButton = None

    # Draw the board
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

        #! WTF is this (if delete is breaks program)
        self.buttons[f"{x},{y}"] = button

        button.setObjectName(f"{x},{y}")

        # Connect the clicked signal of the button to check if a piece and a square have been clicked
        """
        print(
            f"{button.objectName()} : button object name, {self.board[x][y]} : {x} : {y}"
        )
        """

        # Disconnect existing connections
        try:
            button.clicked.disconnect()
        except TypeError:
            pass  # Ignore if no connections were present

        # Connect the clicked signal of the button to check if a piece and a square have been clicked
        button.clicked.connect(
            lambda _, piece=self.board[x][
                y
            ], square=button.objectName(): self.checkMove(piece, square)
        )
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

        print(f"Squares to be highlighted :{self.highlightedSquares}")
        for button in self.highlightedSquares:
            if button.property("class") == "white":
                button.setStyleSheet("background-color: white; border: None")
            elif button.property("class") == "black":
                button.setStyleSheet("background-color: green; border: None")

        # reset values
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

                    # * Removing breaks code
                    button.clicked.connect(
                        lambda _, piece=piece, current_x=current_x, current_y=current_y, new_x=square[
                            0
                        ], new_y=square[
                            1
                        ]: self.movePiece(
                            piece, current_x, current_y, new_x, new_y
                        )
                    )

    def calculateMaterialScore(self):
        score = 0
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None:
                    # Add or subtract the value of the piece from the score
                    if piece.colour == "white":
                        score += piece.weight
                    else:  # piece is black
                        score -= piece.weight
        return scor

    def areYouInCheck(self, player_colour):
        king_position = None
        # Find the king's position
        for x in range(8):
            for y in range(8):
                if (
                    isinstance(self.board[x][y], King)
                    and self.board[x][y].colour == player_colour
                ):
                    king_position = (x, y)

        # Check if any of the opponent's pieces can move to the king's position
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None and piece.colour != player_colour:
                    if king_position in piece.getValidMoves(self.board, x, y):
                        # The king is in check. Now check if there are no valid moves that would result in the king not being in check.
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                new_x, new_y = (
                                    king_position[0] + dx,
                                    king_position[1] + dy,
                                )
                                if 0 <= new_x < 8 and 0 <= new_y < 8:
                                    # Temporarily move the king
                                    temp = self.board[new_x][new_y]
                                    self.board[new_x][new_y] = self.board[
                                        king_position[0]
                                    ][king_position[1]]
                                    self.board[king_position[0]][
                                        king_position[1]
                                    ] = None
                                    # Check if the king is still in check
                                    if not self.areYouInCheck(player_colour):
                                        # The king is not in check, so it's not checkmate
                                        # Move the king back
                                        self.board[king_position[0]][
                                            king_position[1]
                                        ] = self.board[new_x][new_y]
                                        self.board[new_x][new_y] = temp
                                        return 1  # Return 1 for check
                                    # Move the king back
                                    self.board[king_position[0]][king_position[1]] = (
                                        self.board[new_x][new_y]
                                    )
                                    self.board[new_x][new_y] = temp
                        return 2  # Return 2 for checkmate
        return 0  # Return 0 for no check

    def movePiece(self, piece, current_x, current_y, new_x, new_y):
        if piece is not None:
            if piece.colour != self.playerTurn:
                print("not your turn")
                return
            # Prevent the player from moving the pawn two squares twice
            if piece.__class__.__name__ == "Pawn":
                piece.firstMove = False

            # Remove piece from previous pos & set new pos
            self.board[current_x][current_y] = None
            self.board[new_x][new_y] = piece

            self.drawPiece(self.buttons[f"{new_x},{new_y}"], piece)
            self.drawPiece(self.buttons[f"{current_x},{current_y}"], None)

            # checks if the pawn is moving to a promotion square
            if isinstance(self.board[new_x][new_y], Pawn) and (
                new_x == 0 or new_x == 7
            ):
                self.promotionWindow = PromotionWindow()
                self.promotionWindow.pieceSelected.connect(self.onPieceSelected)
                self.promotionWindow.show()
            else:
                logging.info(f"Pawn Cannot Promote on square, ({new_x}, {new_y}) ")

            # Switch player turn
            if self.playerTurn == "white":
                self.playerTurn = "black"
            else:
                self.playerTurn = "white"

        else:
            logging.warn("Piece is None")
            self.highlightSquares(None, [])

        #! fix promotion bug
        #! retrive promotion peice
        for x in range(8):
            if isinstance(self.board[7][x], Pawn):
                print(f"pawn, [8],[{x+1}] can promote")
                print("Waiting for user to select promotion piece...")
                self.promotionWindow = PromotionWindow()
                self.promotionWindow.pieceSelected.connect(self.onPieceSelected)
                self.promotionWindow.show()

            elif isinstance(self.board[0][x], Pawn):
                print(f"pawn, [1],[{x+1}] can promote")
                print("Waiting for user to select promotion piece...")
                self.promotionWindow = PromotionWindow()
                self.promotionWindow.pieceSelected.connect(self.onPieceSelected)
                self.promotionWindow.show()

        # deselect whole board
        for i in range(8):
            for j in range(8):
                self.buttons[f"{i},{j}"].setDown(False)
        if self.selectedButton is not None:
            self.selectedButton.setDown(False)

        # * find if in check
        check = self.areYouInCheck(self.playerTurn)
        logging.info(f"Check status: {check}")

        # * deselect the currently selected button
        self.buttons[f"{current_x},{current_y}"].setStyleSheet(
            "background-color: orange; border: None"
        )
        try:
            self.selectedButton.setStyleSheet(
                "background-color: purple; border: None"
            )  # original square
        except AttributeError:
            logging.error("No button selected")


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
