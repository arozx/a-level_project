import chess
import numpy as np


class MCTS:
    def __init__(self, model, ai_color):
        self.model = model
        self.ai_color = ai_color
        self.root = None

    def __call__(self, human_move):
        if self.root is None:
            self.root = Node(chess.Board(), None)

        # Update the root node with the human move
        if human_move is not None:
            self.root = self._get_child_node(self.root, human_move)

        # Run MCTS iterations
        for _ in range(iterations):
            node = self.root
            board = chess.Board(node.board)

            # Selection
            while node.children:
                node = node.select_child()
                board.push(node.move)

            # Expansion
            if board.turn == self.ai_color:
                for move in board.legal_moves:
                    new_board = board.copy()
                    new_board.push(move)
                    node.add_child(new_board.fen())

            # Simulation
            while not board.is_game_over():
                if board.turn == self.ai_color:
                    move = np.random.choice(list(board.legal_moves))
                else:
                    # If it's the human's turn, wait for their move
                    move = get_human_move()  # You need to implement this function
                board.push(move)

            # Backpropagation
            result = self.model.evaluate(board)
            while node is not None:
                node.update(result)
                node = node.parent

        # Get the best move from the root node
        best_move = sorted(self.root.children, key=lambda c: c.visits)[-1].move
        return best_move if board.turn == self.ai_color else None

    def _get_child_node(self, parent_node, move):
        for child in parent_node.children:
            if child.move == move:
                return child
        return parent_node.add_child(move)


class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def select_child(self):
        s = sorted(
            self.children,
            key=lambda c: c.wins / c.visits
            + np.sqrt(2 * np.log(self.visits) / c.visits),
        )
        return s[-1]

    def add_child(self, move):
        child = Node(move, self)
        self.children.append(child)
        return child

    def update(self, score):
        self.visits += 1
        self.wins += score