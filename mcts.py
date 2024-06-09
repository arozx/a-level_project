import math
from multiprocessing import Pool, cpu_count

import chess
import numpy as np


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

    def expand(self):
        board = chess.Board(self.board_fen)  # Initialize board with FEN
        print(f"Expanding node with board FEN: {self.board_fen}")  # Debug print
        for move in board.legal_moves:
            board.push(move)
            child_fen = board.fen()  # Get FEN of the new board state
            self.children.append(Node(child_fen, move, self))
            print(
                f"Generated child move: {move.uci()} with FEN: {child_fen}"
            )  # Debug print
            board.pop()
        print(
            f"Number of children after expansion: {len(self.children)}"
        )  # Debug print

    def update(self, value):
        self.visits += 1
        self.value += value

    def best_child(self, exploration_weight):
        # Use a large negative number as the default value
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
    def __init__(self, model, ai_color, iterations):
        self.model = model
        self.ai_color = ai_color
        self.root = None
        self.iterations = iterations

    def __call__(self, human_move):
        max_workers = cpu_count()
        with Pool(processes=max_workers) as pool:
            pool.map(self.run_iteration, range(self.iterations))

        if not self.root.children:
            print("No children were created during MCTS.")  # Debug print
            return None

        best_move_node = sorted(self.root.children, key=lambda c: c.visits)[-1]
        best_move = best_move_node.move
        return best_move

    def get_best_move(self, game):
        self.root = Node(game.get_board_state())

        # Expand root node to initialize children
        self.root.expand()
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
            node.expand()

        reward = self.simulate(board)
        while node is not None:
            node.update(reward)
            node = node.parent

    def simulate(self, board):
        while not board.is_game_over():
            move = np.random.choice(list(board.legal_moves))
            board.push(move)
        result = board.result()
        if result == "1-0":
            return 1 if self.ai_color == chess.WHITE else -1
        elif result == "0-1":
            return 1 if self.ai_color == chess.BLACK else -1
        else:
            return 0
