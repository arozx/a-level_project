# define the default parent piece class
class Piece:
    def __init__(self, colour):
        self.colour = colour
        self.x = int
        self.y = int
        self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.weight = 5
        self.fen_symbol = "R" if colour == "white" else "r"

    def getValidMoves(self, board, x, y):
        valid_moves = []
        valid_moves.append((x, y))

        # check if the square in front of the rook is empty
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
        self.weight = 3
        self.fen_symbol = "N" if colour == "white" else "n"

    def getValidMoves(self, board, x, y):
        valid_moves = []
        # calculate all L shaped moves
        moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None or board[nx][ny].colour != self.colour:
                    valid_moves.append((nx, ny))
        return valid_moves


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.weight = 3
        self.fen_symbol = "B" if colour == "white" else "b"

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
        self.weight = 9
        self.fen_symbol = "Q" if colour == "white" else "q"

    def getValidMoves(self, board, x, y):
        valid_moves = []
        # define movement directions
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        # itterate thorugh all directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    valid_moves.append((nx, ny))
                elif board[nx][ny].colour != self.colour:
                    valid_moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return valid_moves


class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.weight = 0
        self.fen_symbol = "K" if colour == "white" else "k"

    def getValidMoves(self, board, x, y):
        valid_moves = []
        # define movement directions
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        # itterate thorugh all directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None or board[nx][ny].colour != self.colour:
                    valid_moves.append((nx, ny))
        return valid_moves


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.first_move = True
        self.weight = 1
        self.fen_symbol = "P" if colour == "white" else "p"

    def getValidMoves(self, board, x, y):
        valid_moves = []

        # Determine the direction of movement based on the color of the pawn
        direction = 1 if self.colour == "white" else -1

        # Check if the square directly in front of the pawn is empty
        if board[x + direction][y] is None:
            valid_moves.append((x + direction, y))

            # If it's the pawn's first move, check if the square two steps ahead is also empty
            if self.first_move and board[x + 2 * direction][y] is None:
                valid_moves.append((x + 2 * direction, y))

        # Check for capturing moves diagonally
        if 0 <= x + direction < 8:
            if (
                0 <= y - 1 < 8
                and board[x + direction][y - 1] is not None
                and board[x + direction][y - 1].colour != self.colour
            ):
                valid_moves.append((x + direction, y - 1))
            if (
                0 <= y + 1 < 8
                and board[x + direction][y + 1] is not None
                and board[x + direction][y + 1].colour != self.colour
            ):
                valid_moves.append((x + direction, y + 1))

        return valid_moves
