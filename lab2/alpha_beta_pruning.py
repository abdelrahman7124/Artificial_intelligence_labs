import math
import board as bd
from heuristics import evaluate, FOUR_WEIGHT


class Minimax_Alpha_Beta:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_expanded = 0
        self.alpha = float("-inf")
        self.beta = float("inf")

    def decision(self, board):
        self.nodes_expanded = 0
        return self.maximize(board,self.depth,self.alpha,self.beta)

    def maximize(self, board, depth,alpha,beta):
        if board.is_full():
            return None, FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
        if depth == 0:
            return None,evaluate(board)

        moves = board.valid_moves()
        max_value = float("-inf")
        best_move = None
        
        for i,move in enumerate(moves):
            
            board.drop(move,bd.AI)
            _,value = self.minimize(board,depth - 1,alpha,beta)
            board.undo(move)
            
            if value > max_value:
                max_value = value
                best_move = move
                
            if max_value >= beta:
                pruned = moves[i+1:]
                break
            
            if max_value > alpha:
                alpha = max_value
                
        self.nodes_expanded += 1
            
        return best_move,max_value
            

    def minimize(self, board, depth,alpha,beta):
        if board.is_full():
            return None, FOUR_WEIGHT * (board.count_fours(bd.AI) - board.count_fours(bd.HUMAN))
        if depth == 0:
            return None,evaluate(board)
        
        moves = board.valid_moves()
        min_value = float("inf")
        best_move = None
        
        for i,move in enumerate(moves):
            
            board.drop(move,bd.HUMAN)
            _,value = self.maximize(board,depth - 1,alpha,beta)
            board.undo(move)
            
            if value < min_value:
                min_value = value
                best_move = move
                
            if min_value <= alpha:
                pruned = moves[i+1:]
                break
            
            if min_value < beta:
                beta = min_value
                
        self.nodes_expanded += 1
        
        return best_move,min_value