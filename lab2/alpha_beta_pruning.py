import math
import board as bd
from heuristics import evaluate, FOUR_WEIGHT
from TreePrinting import TreeNode


class Minimax_Alpha_Beta:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_expanded = 0
        self.root = None
        self.alpha = float("-inf")
        self.beta = float("inf")

    def decision(self, board):
        self.nodes_expanded = 0
        self.root = TreeNode("MAX")
        return self.maximize(board,self.depth,self.alpha,self.beta,self.root)

    def maximize(self, board, depth,alpha,beta,node):
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
        
        for i,move in enumerate(moves):
            child = TreeNode("MIN", move)
            node.children.append(child)
            
            board.drop(move,bd.AI)
            _,value = self.minimize(board,depth - 1,alpha,beta,child)
            board.undo(move)
            
            if value > max_value:
                max_value = value
                best_move = move
                
            if max_value >= beta:
                node.pruned = moves[i+1:]
                break
            
            if max_value > alpha:
                alpha = max_value
                
        self.nodes_expanded += 1
        node.value = max_value
            
        return best_move,max_value
            

    def minimize(self, board, depth,alpha,beta,node):
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
        
        for i,move in enumerate(moves):
            child = TreeNode("MAX", move)
            node.children.append(child)
            
            board.drop(move,bd.HUMAN)
            _,value = self.maximize(board,depth - 1,alpha,beta,child)
            board.undo(move)
            
            if value < min_value:
                min_value = value
                best_move = move
                
            if min_value <= alpha:
                node.pruned = moves[i+1:]
                break
            
            if min_value < beta:
                beta = min_value
                
        self.nodes_expanded += 1
        node.value = min_value
        
        return best_move,min_value