import chess

from mcts import MCTS, Node
from pieces import Bishop, King, Knight, Pawn, Queen, Rook


class ChessBoard:
    def __init__(self):
        self.move_count = 0
        self.player_turn = "white"
        self.material = -1

        self.board = [[None for _ in range(8)] for _ in range(8)]

        self.board_cache = []

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

        # Initialize MCTS
        self.root_node = Node(self.board)
        self.mcts = MCTS(self.root_node)

    """
    Takes no arguments
    Returns an array of moves that are legal
    """

    def get_all_valid_moves(self):
        board = chess.Board(self.board_array_to_fen())
        return [move.uci() for move in board.legal_moves]

    """
    Takes no arguments
    Returns the board as a FEN string
    """

    def board_array_to_fen(self):
        board = chess.Board()
        board.clear_board()
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if piece is not None:
                    board.set_piece_at(
                        chess.square(file, 7 - rank),
                        chess.Piece.from_symbol(piece.symbol),
                    )
        return board.fen()

    """
    takes no arguments
    prints the board as text
    Returns N/A
    ! THIS IS A DEVELOPMENT FUNCTION
    """

    def display_board_as_text(self):
        self.board_cache = []
        for x in range(0, 8):
            for y in range(0, 8):
                if self.board[x][y] is None:
                    self.board_cache.append("|  |")
                else:
                    self.board_cache.append(
                        "|" + self.board[x][y].__class__.__name__[0:2] + "|"
                    )

        for i in range(0, 8):
            print(self.board_cache[i * 8 : i * 8 + 8])

    """
    takes no arguments
    Prints the colours of the pieces on the board
    Returns: N/A
    ! THIS IS A DEVELOPMENT FUNCTION
    """

    def display_board_as_colours(self):
        colours = []
        for x in range(0, 8):
            for y in range(0, 8):
                if self.board[x][y] is None:
                    colours.append("|  |")
                else:
                    colours.append("|" + self.board[x][y].colour[0:2] + "|")

        for i in range(0, 8):
            print(colours[i * 8 : i * 8 + 8])

    """
    takes no arguments
    Prints the coordinates of the board
    Returns: N/A
    ! INVERTED TO READ AS X, Y WHEN y then x
    """

    def display_board_as_coordinates(self):
        coordinates = []
        for x in range(0, 8):
            for y in range(0, 8):
                coordinates.append(f"|{x}{y}|")

        for i in range(0, 8):
            print(coordinates[i * 8 : i * 8 + 8])

    """
    take a x and y for starting take an x any y for end pos
    updates the board & board_cache
    updates the material & move_count if the move is valid
    ends early and reutrns false if the move causes check, there is no pice at the start or the end pos is not in the valid moves
    returns True if move is valid
    """

    def enpesaunt(self, x, y, endx, endy, colour):
        try:
            if isinstance(self.board[x][y], Pawn):
                if (
                    isinstance(self.board[endx][endy + 1], Pawn)
                    and colour != self.board[endx][endy + 1].colour
                ):
                    print("pawn on ", endx, endy + 1)
                    return True
                elif (
                    isinstance(self.board[endx][endy - 1], Pawn)
                    and colour != self.board[endx][endy - 1].colour
                ):
                    print("pawn on", endx, endy - 1)
                    return True
        except IndexError:
            # raised when enpseant is checked for outside the board
            return False
        return False

    """
    Take the board as an argument & player_colour
    returns False if castling is not possible
    returns "kingside" or "queenside"
    """

    def castling(self, board, player_colour):
        # check if the king has moved
        try:
            if player_colour == "white" and (board[0][3].first_move):
                # king can castle
                if board[0][0].first_move:
                    return "queenside"

                if board[0][7].first_move:
                    return "kingside"

            if player_colour == "black" and (board[7][3].first_move):
                # king can castle
                if board[7][0].first_move:
                    return "queenside"

                if board[7][7].first_move:
                    return "kingside"
        except Exception as e:
            print(e)
        return False

    """
    Take piece xy coords and end square xy coords
    Checks all legal moves as well as enpesaunt moves
    Returns True for a legal move
    Returns False for an illegal move
    """
    # TODO add castling support

    def move_piece(self, x, y, endx, endy):
        # where the is no peice return False
        if self.board[x][y] is None:
            print("No piece at this position")
            return False

        # enpesaunt rules
        is_enpesaunt = self.enpesaunt(x, y, endx, endy, self.board[x][y].colour)

        # castling rules
        is_castling = self.castling(self.board, self.board[x][y].colour)

        # if the end pos is not in the valid moves return False
        if (
            ((endx, endy) not in self.board[x][y].get_valid_moves(self.board, x, y))
            and not is_enpesaunt
            and is_castling  # returns False if no castling oppertunity
        ):
            #! DEBUG
            print("Invalid move, not legal")
            return False

        # check if the move caused the player to be in check
        if self.are_you_in_check(self.player_turn) == (1 or 2):
            print("Invalid move (check)")
            return False

        # remove enpesaunt pawn
        if is_enpesaunt:
            if isinstance(self.board[x][y], Pawn) and abs(x - endx) == 2:
                if isinstance(self.board[endx][endy + 1], Pawn):
                    self.board[endx][endy + 1] = None
                elif isinstance(self.board[endx][endy - 1], Pawn):
                    self.board[endx][endy - 1] = None

        # TODO check if the move is castling

        # move the piece
        self.board[endx][endy] = self.board[x][y]
        self.board[x][y] = None

        # generate the board
        self.board_cache[(x * 8 + y)] = "|  |"
        self.board_cache[(endx * 8 + endy)] = (
            "|" + self.board[endx][endy].__class__.__name__[0:2] + "|"
        )

        # update the material
        if self.board[endx][endy] is not None:
            self.material += self.board[endx][endy].weight

        # increment the move count
        self.move_count += 1
        return True

    """
    Takes No arguments and returns a number based on weather the player is in check
    """

    def game_over(self):
        return (
            self.are_you_in_check("white") == 2 or self.are_you_in_check("black") == 2
        )

    """
    Takes the colour of the player
    Returns the x and y of the king
    """

    def get_king_position(self, colour):
        for x in range(8):
            for y in range(8):
                if (
                    isinstance(self.board[x][y], King)
                    and self.board[x][y].colour == colour
                ):
                    return (x, y)

    """
    Takes no colour and returns
    2 for checkmate
    1 for check
    0 for no check
    """

    def are_you_in_check(self, player_colour):
        king_position = self.get_king_position(player_colour)

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

    """
    Takes no arguments
    calls other function
    """

    def main(self):
        while not self.game_over():
            #! DEBUG TEMP REMOVE THIS
            # self.display_board_as_coordinates()
            self.display_board_as_text()
            print("White to move")
            x, y, endx, endy = map(int, input("Enter move: ").split())
            if self.move_piece(x, y, endx, endy):
                self.player_turn = "black" if self.player_turn == "white" else "white"
            else:
                print("Invalid move")

            # Get the best move from the AI
            self.mcts.run()
            best_move = self.mcts.best_move()
            print(f"AI move: {best_move}")

            # Make the AI move
            # Take the array of move tuples and covert to x,y and endx, endy
            x, y, endx, endy = (
                best_move[0][0],
                best_move[0][1],
                best_move[1][0],
                best_move[1][1],
            )
            if self.move_piece(x, y, endx, endy):
                self.move_piece(x, y, endx, endy)

        print("Game over")


if __name__ == "__main__":
    board_instance = ChessBoard()
    board_instance.main()
