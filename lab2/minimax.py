import board as bd
from heuristics import evaluate, FOUR_WEIGHT
from TreePrinting import TreeNode


class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_expanded = 0
        self.root = None
        self.seen = {}

    def decision(self, board):
        self.nodes_expanded = 0
        self.seen = {}
        self.root = TreeNode("MAX")
        return self.maximize(board,self.depth,self.root)

    def reuse(self, key, node):
        old = self.seen.get(key)
        if old is None:
            return False
        node.kind = old.kind
        node.value = old.value
        node.children = old.children
        return True

    def maximize(self, board, depth, node):
        key = "MAX" + str(depth) + str(board.board)
        if self.reuse(key, node):
            return None, node.value
        if board.is_full():
            node.kind = "LEAF"
            node.value = FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
            self.seen[key] = node
            return None, node.value
        if depth == 0:
            node.kind = "LEAF"
            node.value = evaluate(board)
            self.seen[key] = node
            return None,node.value

        moves = board.valid_moves()
        max_value = float("-inf")
        best_move = None
        for move in moves:
            child = TreeNode("MIN", move)
            node.children.append(child)
            board.drop(move,bd.AI)
            _,value = self.minimize(board,depth - 1,child)
            board.undo(move)
            if value > max_value:
                max_value = value
                best_move = move
        self.nodes_expanded += 1
        node.value = max_value
        self.seen[key] = node
        return best_move,max_value
            

    def minimize(self, board, depth, node):
        key = "MIN" + str(depth) + str(board.board)
        if self.reuse(key, node):
            return None, node.value
        if board.is_full():
            node.kind = "LEAF"
            node.value = FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
            self.seen[key] = node
            return None, node.value
        if depth == 0:
            node.kind = "LEAF"
            node.value = evaluate(board)
            self.seen[key] = node
            return None,node.value

        moves = board.valid_moves()
        min_value = float("inf")
        best_move = None
        for move in moves:
            child = TreeNode("MAX", move)
            node.children.append(child)
            board.drop(move,bd.HUMAN)
            _,value = self.maximize(board,depth - 1,child)
            board.undo(move)
            if value < min_value:
                min_value = value
                best_move = move
        self.nodes_expanded += 1
        node.value = min_value
        self.seen[key] = node
        return best_move,min_value