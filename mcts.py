# mcts.py

import math
from multiprocessing import Pool, cpu_count

import chess


class Node:
    def __init__(self, board_fen, move=None, parent=None):
        self.board_fen = board_fen  # Store FEN string
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_leaf(self):
        return len(self.children) == 0

    def expand(self, all_valid_moves):
        for move_uci in all_valid_moves:
            move = chess.Move.from_uci(move_uci)
            new_board = chess.Board(self.board_fen)
            new_board.push(move)
            child = Node(new_board.fen(), move, self)
            self.children.append(child)

    def update(self, value):
        self.visits += 1
        self.value += value

    def best_child(self, exploration_weight):
        best_value = float("-inf")
        best_child = None

        for child in self.children:
            if child.visits == 0:
                value = float("inf")  # Encourage exploration of this child
            else:
                value = child.value / child.visits + exploration_weight * math.sqrt(
                    2 * math.log(self.visits) / child.visits
                )

            if value > best_value:
                best_value = value
                best_child = child

        return best_child


class MCTS:
    def __init__(self, model, ai_color, iterations, all_valid_moves):
        self.model = model
        self.ai_color = ai_color
        self.root = None
        self.iterations = iterations
        self.all_valid_moves = all_valid_moves

    def __call__(self, human_move):
        max_workers = cpu_count()
        with Pool(processes=max_workers) as pool:
            pool.map(self.run_iteration, range(self.iterations))

        if not self.root.children:  # no legal moves
            return None

        best_move_node = sorted(self.root.children, key=lambda c: c.visits)[-1]
        best_move = best_move_node.move
        return best_move

    def get_best_move(self, game, all_valid_moves):
        self.root = Node(
            game.get_board_state()
        )  # returns the FEN string of the current board state

        print("self.all_valid_moves: ", all_valid_moves)  # Debug print
        self.root.expand(all_valid_moves)  # Expand root node with valid moves
        print(
            f"Root node has {len(self.root.children)} children after expansion."
        )  # Debug print

        best_move = self.__call__(None)

        if best_move is not None:
            return best_move.uci()  # Return the move in UCI format
        else:
            return None

    def run_iteration(self, _):
        node = self.root
        while not node.is_leaf():
            node = node.best_child(exploration_weight=1.4)
            if node is None:
                print("Node is None during iteration.")  # Debug print
                return

        board = chess.Board(node.board_fen)  # Initialize board with FEN
        if not board.is_game_over():
            node.expand(self.all_valid_moves)

        reward = self.negamax(board, depth=3, color=1)
        while node is not None:
            node.update(reward)
            node = node.parent

    def negamax(self, board, depth, color):
        if depth == 0 or board.is_game_over():
            return color * self.evaluate(board)

        max_value = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            value = -self.negamax(board, depth - 1, -color)
            board.pop()
            max_value = max(max_value, value)

        return max_value

    def evaluate(self, board):
        # Simplified evaluation: material count
        material = sum(
            piece_value[piece.piece_type] for piece in board.piece_map().values()
        )
        return material if board.turn == chess.WHITE else -material


piece_value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,  # The king's value is arbitrarily set to 0 since it cannot be captured
}
