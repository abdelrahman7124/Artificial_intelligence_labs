import math
import board as bd
from heuristics import evaluate, FOUR_WEIGHT
from TreePrinting import TreeNode


class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_expanded = 0
        self.root = None

    def decision(self, board):
        self.nodes_expanded = 0
        self.root = TreeNode("MAX")
        return self.maximize(board,self.depth,self.root)

    def maximize(self, board, depth, node):
        if board.is_full():
            node.kind = "LEAF"
            node.value = FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
            return None, node.value
        if depth == 0:
            node.kind = "LEAF"
            node.value = evaluate(board)
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
            
        return best_move,max_value
            

    def minimize(self, board, depth, node):
        if board.is_full():
            node.kind = "LEAF"
            node.value = FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
            return None, node.value
        if depth == 0:
            node.kind = "LEAF"
            node.value = evaluate(board)
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
        
        return best_move,min_value