import argparse
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget

from mcts import MCTS
from pieces import Bishop, King, Knight, Pawn, Queen, Rook
from promotion_window import PromotionWindow


def parse_rgb(value):
    try:
        # Split the input string by commas
        r, g, b = map(int, value.split(","))

        r, g, b = int(r), int(g), int(b)

        # Check if each value is within the 0-255 range
        if not all(0 <= val <= 255 for val in (r, g, b)):
            raise ValueError

        return (r, g, b)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "RGB values must be in the form 'R,G,B' and each between 0 and 255."
        )


class ChessBoard:
    def __init__(self, layout):
        self.move_count = 0
        self.player_turn = "white"

        try:
            # get the board colours from arguments
            parser = argparse.ArgumentParser(description="Store two RGB values.")

            # Add arguments for the two RGB values
            parser.add_argument(
                "rgb1",
                type=parse_rgb,
                help="First RGB value in the format 'R,G,B' where R, G, and B are integers between 0 and 255",
            )
            parser.add_argument(
                "rgb2",
                type=parse_rgb,
                help="Second RGB value in the format 'R,G,B' where R, G, and B are integers between 0 and 255",
            )

            # Parse the arguments
            args = parser.parse_args()

            # Print the RGB values
            print(f"White RGB value: {args.rgb1}")
            print(f"Black RGB value: {args.rgb2}")

            self.white_rgb = args.rgb1
            self.black_rgb = args.rgb2
        except argparse.ArgumentTypeError as e:
            print(f"Error: {e}")

        self.all_legal_moves = []

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.buttons = {}
        self.selected_button = None
        self.highlighted_squares = []

        # setup promotion window to be called as needed
        self.promotion_window = PromotionWindow()
        self.promotion_window.pieceSelected.connect(self.handle_piece_selected)
        self.promotion_window.close()

        # Create an instance of the MCTS class, passing all valid moves
        self.mcts = MCTS(
            model=None,
            ai_color="white",
            iterations=5000,
            all_valid_moves=self.get_all_valid_moves(),
        )

        # Create white pieces
        self.board[0][0] = Rook("white")
        self.board[0][1] = Knight("white")
        self.board[0][2] = Bishop("white")
        self.board[0][4] = Queen("white")
        self.board[0][3] = King("white")
        self.board[0][5] = Bishop("white")
        self.board[0][6] = Knight("white")
        self.board[0][7] = Rook("white")
        for i in range(8):
            self.board[1][i] = Pawn("white")

        # Create black pieces
        self.board[7][0] = Rook("black")
        self.board[7][1] = Knight("black")
        self.board[7][2] = Bishop("black")
        self.board[7][4] = Queen("black")
        self.board[7][3] = King("black")
        self.board[7][5] = Bishop("black")
        self.board[7][6] = Knight("black")
        self.board[7][7] = Rook("black")
        for i in range(8):
            self.board[6][i] = Pawn("black")

    # Get the current state of the board
    def get_board_state(self):
        # convert current board state to fen
        fen = ""
        for row in self.board:
            empty = 0
            for piece in row:
                if piece is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0

                    # use the piece to determine the fen symbol
                    match piece.__class__.__name__:
                        case "Pawn":
                            fen += "p"
                        case "Knight":
                            fen += "n"
                        case "Bishop":
                            fen += "b"
                        case "Rook":
                            fen += "r"
                        case "Queen":
                            fen += "q"
                        case "King":
                            fen += "k"

                    if piece.colour == "white":
                        fen = fen[:-1] + fen[-1].upper()

            if empty > 0:
                fen += str(empty)
            fen += "/"
        return fen[:-1]

    def promote_pawn(self, x, y):
        print(f"Promoting pawn at ({x}, {y})")

    def game_over(self):
        return (
            self.are_you_in_check("white") == 2 or self.are_you_in_check("black") == 2
        )

    def get_all_valid_moves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None and piece.colour == "black":
                    valid_moves = piece.get_valid_moves(self.board, x, y)
                    for move in valid_moves:
                        moves.append(((x, y), move))

        # convert from tuple to UCI format
        moves = [
            f"{chr(97 + start[1])}{8 - start[0]}{chr(97 + end[1])}{8 - end[0]}"
            for start, end in moves
        ]
        # remove all moves where the start and end squares are the same
        moves = [move for move in moves if move[0] != move[2] or move[1] != move[3]]

        # remove all moves where the king is in check
        for move in moves:
            old_x, old_y, new_x, new_y = self.uci_to_coords(move)
            temp = self.board[new_x][new_y]
            self.board[new_x][new_y] = self.board[old_x][old_y]
            self.board[old_x][old_y] = None
            if self.are_you_in_check("black"):
                moves.remove(move)
            self.board[old_x][old_y] = self.board[new_x][new_y]
            self.board[new_x][new_y] = temp

        self.all_legal_moves = moves
        print("chessboard all valid moves: ", moves)

        return moves

    def uci_to_coords(self, uci):
        # Convert UCI move (e.g., 'e2e4') to coordinates (e.g., (6, 4, 4, 4))
        col_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        start_col, start_row, end_col, end_row = (
            col_dict[uci[0]],
            int(uci[1]) - 1,
            col_dict[uci[2]],
            int(uci[3]) - 1,
        )
        return 7 - start_row, start_col, 7 - end_row, end_col

    def game_loop(self):
        print("Game loop called")
        if self.player_turn == "black":
            print("f {self.all_valid_moves()}")
            move_uci = self.mcts.get_best_move(
                self, all_valid_moves=self.get_all_valid_moves()
            )
            if move_uci:  # when b7b8n
                print(f"Best move found by MCTS: {move_uci}")  # Debug print
                move = self.uci_to_coords(move_uci)
                print(f"Converted move: {move}")
                self.execute_move(move)
            else:
                exit(1)
            self.player_turn = "white"
            self.move_count += 1

    # Ensure the execute_move method expects move in the format (old_x, old_y, new_x, new_y)
    def execute_move(self, move):
        old_x, old_y, new_x, new_y = move
        return self.move_piece(self.board[old_x][old_y], old_x, old_y, new_x, new_y)

    # called when a piece is selected & promotion window is open
    def handle_piece_selected(self, piece):
        logging.info(f"Piece selected: {piece}")
        self.promotion_window.close()
        print(f"Piece selected: {piece}")

    def find_piece_coordinates(self, piece):
        if piece is None:
            return None, None
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == piece:
                    return x, y

    # check if a piece & square have been clicked, then call move_piece
    def check_move(self, piece, square):
        print(f"CheckMove; Piece: {piece} : Square: {square}")
        if piece is not None and square is not None:
            x, y = [int(i) for i in square.split(",")]
            if self.selected_button is None:
                self.selected_button = self.buttons[square]
                # set the background colour of the selected button to yellow
                self.selected_button.setStyleSheet(
                    "background-color: yellow; border: None"
                )
                valid_moves = self.get_valid_moves(self.board, x, y)
                try:
                    valid_moves.insert(0, (x, y))
                    print(f"cur x = {valid_moves[0][0]} cur y = {valid_moves[0][1]}")
                except IndexError:
                    print("No valid moves")
                self.highlight_squares(piece, valid_moves)
            else:
                self.clearhighlighted_squares()
                current_x, current_y = self.find_piece_coordinates(piece)
                print(f"{current_x} : current x\n {current_y} : current y")
                if self.selected_button == self.buttons[square]:
                    self.selected_button.setStyleSheet("")
                    self.selected_button = None
                else:
                    if current_x is not None and current_y is not None:
                        self.draw_square(current_x, current_y)
                    self.selected_button = self.buttons[square]
                    self.selected_button.setStyleSheet(
                        "background-color: yellow; border: None"
                    )

    # draw the board
    def draw_square(self, x, y):
        button = QPushButton()
        button.setFixedSize(100, 100)

        if x is not None and y is not None:
            if (x + y) % 2 == 0:  # sets white squares
                if self.white_rgb:
                    button.setStyleSheet(
                        f"background-color: rgb{self.white_rgb}; border: None"
                    )
                else:
                    button.setProperty("class", "white")
                    button.setStyleSheet("background-color: white; border: None")
            else:  # sets black squares
                if self.black_rgb:
                    button.setStyleSheet(
                        f"background-color: rgb{self.black_rgb}; border: None"
                    )
                else:
                    button.setProperty("class", "black")
                    button.setStyleSheet("background-color: green; border: None")

        #! For development purposes / Debugging
        button.setText(f"{x},{y}")

        # set the objectName property to the coordinates of the square
        self.buttons[f"{x},{y}"] = button

        button.setObjectName(f"{x},{y}")

        # disconnect existing connections
        try:
            button.clicked.disconnect()
        except TypeError:
            pass  # ignore if no connections were present

        # connect the clicked signal to check if a piece and a square have been clicked
        button.clicked.connect(
            lambda _,
            piece=self.board[x][y],
            square=button.objectName(): self.check_move(piece, square)
        )
        return button

    # draw the chess board
    def draw_board(self, layout):
        for x in range(8):
            for y in range(8):
                button = self.draw_square(x, y)
                layout.addWidget(button, x, y)

        self._score_label = QLabel("White Score: 0")
        layout.addWidget(self._score_label, 8, 0, 1, 8)

        # check if there is a piece on the square and call draw_piece
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None:
                    self.draw_piece(self.buttons[f"{x},{y}"], self.board[x][y])

    # draw image / piece on a button
    def draw_piece(self, button, piece):
        if piece is not None and piece.__class__.__name__ != "None":
            icon = QIcon(f"media/{piece.colour}/{piece.__class__.__name__}.svg")
            button.setIcon(icon)
            button.setIconSize(button.size())
            button.setObjectName(f"{piece.x},{piece.y}")
        else:
            button.setIcon(QIcon())

    # getter for the valid moves of a piece
    def get_valid_moves(self, board, x, y):
        x = int(x)
        y = int(y)
        if self.board[x][y] is not None:
            return self.board[x][y].get_valid_moves(board, x, y)
        else:
            return []

    def highlight_squares(self, piece, squares):
        # get the coordinates of the previously selected button
        current_x = squares[0][0]
        current_y = squares[0][1]

        # remove the coordinates of the previously selected button
        squares.pop(0)

        print(f"Squares to be highlighted :{self.highlighted_squares}")
        for button in self.highlighted_squares:
            if button.property("class") == "white":
                button.setStyleSheet("background-color: white; border: None")
            elif button.property("class") == "black":
                button.setStyleSheet("background-color: green; border: None")

        # reset values
        self.highlighted_squares = []

        # iterate through the squares array, highlights the squares
        for square in squares:
            if isinstance(square, tuple) and len(square) == 2:
                if 0 <= square[0] < 8 and 0 <= square[1] < 8:
                    button = self.buttons[f"{square[0]},{square[1]}"]
                    self.highlighted_squares.append(button)
                    button.setStyleSheet("background-color: blue; border: None")

                    # connect to move_piece
                    button.clicked.connect(
                        lambda _,
                        piece=piece,
                        current_x=current_x,
                        current_y=current_y,
                        new_x=square[0],
                        new_y=square[1]: self.move_piece(
                            piece, current_x, current_y, new_x, new_y
                        )
                    )

    def clearhighlighted_squares(self):
        for button in self.highlighted_squares:
            if button.property("class") == "white":
                button.setStyleSheet("background-color: white; border: None")
            elif button.property("class") == "black":
                button.setStyleSheet("background-color: green; border: None")
        self.highlighted_squares = []

    def move_piece(self, piece, old_x, old_y, new_x, new_y):
        print(f"board state: {self.get_board_state()}")

        print(
            f"move_piece; old_x: {old_x}, old_y: {old_y}, new_x: {new_x}, new_y: {new_y}"
        )
        print(f"self.player_turn: {self.player_turn} piece: {piece}")

        if self.selected_button:
            self.selected_button.setStyleSheet("")
            self.selected_button = None
        else:
            print("No button was selected")

        self.clearhighlighted_squares()

        if self.board[old_x][old_y] is not None:
            if (
                self.board[new_x][new_y] is None
                or self.board[new_x][new_y].colour != self.board[old_x][old_y].colour
            ):
                # Clear old locations of all pieces
                for x in range(8):
                    for y in range(8):
                        if self.board[x][y] is not None:
                            self.buttons[f"{x},{y}"].setIcon(QIcon())  # Reset icon

                # Capture the opponent's piece if the destination square is occupied
                captured_piece = self.board[new_x][new_y]

                # Move the piece to the new location
                self.board[new_x][new_y] = self.board[old_x][old_y]
                self.board[old_x][old_y] = None

                # set first_move false if exists
                if isinstance(self.board[new_x][new_y], Pawn):
                    self.board[new_x][new_y].first_move = False

                # Set the icon for the piece at its new location
                new_piece = self.board[new_x][new_y]
                if new_piece is not None:
                    icon = QIcon(
                        f"media/{new_piece.colour}/{new_piece.__class__.__name__}.svg"
                    )
                    self.buttons[f"{new_x},{new_y}"].setIcon(icon)

                # Update player turn
                self.player_turn = "black" if self.player_turn == "white" else "white"

                # Handle pawn promotion
                if isinstance(new_piece, Pawn) and (new_x == 0 or new_x == 7):
                    print(
                        f"Promotion: {new_piece.colour} {new_piece.__class__.__name__}"
                    )
                    self.promote_pawn(new_x, new_y)

                # Regenerate the board
                self.regenerate_board()

                # Print a message indicating that a capture occurred
                if captured_piece:
                    print(
                        f"Captured {captured_piece.colour} {captured_piece.__class__.__name__}"
                    )

            else:
                print("Invalid move: Destination occupied by your own piece")
        else:
            print("Invalid move: No piece at the selected position")

        # always return the move as a tuple
        print(f"From: ({old_x}, {old_y}) To: ({new_x}, {new_y})")
        # call the game loop
        self.game_loop()
        return (old_x, old_y, new_x, new_y)

    def regenerate_board(self):
        layout = self.buttons["0,0"].parentWidget().layout()
        # Clear the layout
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.buttons = {}

        # Draw the board
        for x in range(8):
            for y in range(8):
                button = self.draw_square(x, y)
                layout.addWidget(button, x, y)

        self._score_label = QLabel("White Score: 0")
        layout.addWidget(self._score_label, 8, 0, 1, 8)

        # Redraw all pieces on the board
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None:
                    self.draw_piece(self.buttons[f"{x},{y}"], self.board[x][y])

        # Ensure last move is cleared
        self.last_move = None

    def calculate_material_score(self):
        score = 0
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None:
                    # add or subtract the value of the piece from the score
                    if piece.colour == "white":
                        score += piece.weight
                    else:  # piece is black
                        score -= piece.weight
        return score

    def _update_score(self):
        # Calculate the material score
        score = self.calculate_material_score()

        # Update the score label text
        self._score_label.setText(f"Score: {score}")

    def are_you_in_check(self, player_colour):
        king_position = None
        # find the king's position
        for x in range(8):
            for y in range(8):
                if (
                    isinstance(self.board[x][y], King)
                    and self.board[x][y].colour == player_colour
                ):
                    king_position = (x, y)

        # check if any of the opponent's pieces can move to the king's position
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece is not None and piece.colour != player_colour:
                    try:
                        if king_position in piece.get_valid_moves(self.board, x, y):
                            # check if there are no valid moves that would result in the king not being in check
                            for dx in range(-1, 2):
                                for dy in range(-1, 2):
                                    new_x, new_y = (
                                        king_position[0] + dx,
                                        king_position[1] + dy,
                                    )
                                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                                        # temporarily move the king
                                        temp = self.board[new_x][new_y]
                                        self.board[new_x][new_y] = self.board[
                                            king_position[0]
                                        ][king_position[1]]
                                        self.board[king_position[0]][
                                            king_position[1]
                                        ] = None
                                        # check if the king is still in check
                                        if not self.are_you_in_check(player_colour):
                                            # the king is not in check, so it's not checkmate
                                            # move the king back
                                            self.board[king_position[0]][
                                                king_position[1]
                                            ] = self.board[new_x][new_y]
                                            self.board[new_x][new_y] = temp
                                            return 1  # for check
                                        # move the king back
                                        self.board[king_position[0]][
                                            king_position[1]
                                        ] = self.board[new_x][new_y]
                                        self.board[new_x][new_y] = temp
                        return 2  # for checkmate
                    except ValueError:  # catch ValueError: Outside of board
                        print("ValueError: Outside of board")
        return 0  # for no check


# UI
class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.windowTitle = "Chess"

        # set layout
        layout = QGridLayout()
        self.setLayout(layout)

        # create instance of the chess board
        board = ChessBoard(layout)
        board.draw_board(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()
