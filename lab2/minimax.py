import math
import board as bd
from heuristics import evaluate, FOUR_WEIGHT


class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_expanded = 0

    def decision(self, board):
        self.nodes_expanded = 0
        return self.maximize(board,self.depth)

    def maximize(self, board, depth):
        # TERMINAL-TEST: full -> (None, exact score) | depth == 0 -> (None, evaluate)
        # nodes_expanded += 1
        # max_col, max_utility = None, -inf
        # for col in valid_moves:
        #     drop AI
        #     _, utility = self.minimize(board, depth - 1)
        #     undo
        #     if utility > max_utility: update both
        # return max_col, max_utility
        if board.is_full():
            return None, FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
        if depth == 0:
            return None,evaluate(board)

        moves = board.valid_moves()
        max_value = float("-inf")
        best_move = None
        for move in moves:
            board.drop(move,bd.AI)
            _,value = self.minimize(board,depth - 1)
            board.undo(move)
            if value > max_value:
                max_value = value
                best_move = move
        self.nodes_expanded += 1
            
        return best_move,max_value
            

    def minimize(self, board, depth):
        # mirror of maximize: drop HUMAN, start at +inf, call maximize, use <
        if board.is_full():
            return None, FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
        if depth == 0:
            return None,evaluate(board)
        
        moves = board.valid_moves()
        min_value = float("inf")
        best_move = None
        for move in moves:
            board.drop(move,bd.HUMAN)
            _,value = self.maximize(board,depth - 1)
            board.undo(move)
            if value < min_value:
                min_value = value
                best_move = move
        self.nodes_expanded += 1
        
        return best_move,min_value