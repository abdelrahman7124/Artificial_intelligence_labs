EMPTY, HUMAN, AI = 0, 1, 2

class Board:
    def __init__(self, rows=6, cols=7):
        if rows < 6 or cols < 7:
            raise ValueError("Board must be 6x7 at least")
        self.rows = rows
        self.cols = cols
        self.board = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.disc_counter = 0 
        self.heights = [0 for _ in range(cols)]

        
        
    def is_valid(self, col):
        if col < self.cols and col >= 0:
            return not self.heights[col] == self.rows
        return False

    def valid_moves(self):
        '''
        We began with the center first as it is normally the best move
        so the alpha beta pruning will eventually prune alot of values
        '''
        middle = self.cols // 2 
        moves = []
        for i in range(middle + 1):
            if self.is_valid(middle + i):
                moves.append(middle + i)
                
            if self.is_valid(middle - i) and not i == 0:
                moves.append(middle - i)
        return moves

    def drop(self, col, player):
        '''
        We return the row for the gui to know where to draw the shape 
        '''
        row = self.heights[col]
        self.board[row][col] = player
        self.heights[col] += 1
        self.disc_counter += 1
        return row

    def undo(self, col):
        # reverse of drop
        row = self.heights[col] - 1
        self.board[row][col] = EMPTY
        self.heights[col] -= 1
        self.disc_counter -= 1

    def is_full(self):
        return self.disc_counter == self.rows * self.cols

    def count_fours(self, player):
        fours = 0
        # check horizontal
        
        for i in range(self.rows):
            count = 0
            for j in range(self.cols):
                if self.board[i][j] == player:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    fours += 1
                    count -= 1
            
        # check vertical
        for j in range(self.cols):
            count = 0
            for i in range(self.rows):
                if self.board[i][j] == player:
                    count += 1
                else:
                    count = 0                    
                if count == 4:
                    fours += 1
                    count -= 1
        # check diagonal /  (up-right)
        # every / diagonal starts on the bottom row or the left column
        starts = [(0, j) for j in range(self.cols)] + [(i, 0) for i in range(1, self.rows)]
        for i, j in starts:
            count = 0
            while i < self.rows and j < self.cols:
                if self.board[i][j] == player:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    fours += 1
                    count -= 1
                i += 1
                j += 1

        # check diagonal \  (up-left)
        # every \ diagonal starts on the bottom row or the right column
        starts = [(0, j) for j in range(self.cols)] + [(i, self.cols - 1) for i in range(1, self.rows)]
        for i, j in starts:
            count = 0
            while i < self.rows and j >= 0:
                if self.board[i][j] == player:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    fours += 1
                    count -= 1
                i += 1
                j -= 1

        return fours


    def print_board(self):
        symbols = {EMPTY: '.', HUMAN: 'H', AI: 'A'}
        for row in reversed(self.board):
            print(*[symbols[cell] for cell in row])

def main():
    #some test cases to see make sure the functions are correct
    sol = Board()
    for i in range(7):
        sol.drop(i,HUMAN)
    sol.drop(1,AI)
    sol.drop(2, HUMAN)
    
    sol.drop(2,AI)
    sol.drop(3,HUMAN)
    sol.drop(3,HUMAN)
    
    sol.drop(3,AI)
    sol.drop(4,HUMAN)
    sol.drop(4,HUMAN)
    sol.drop(4,HUMAN)
    sol.drop(4,AI)
    sol.print_board()
    human_score = sol.count_fours(HUMAN)
    Ai_score = sol.count_fours(AI)
    print(human_score)
    print(Ai_score)
    
if __name__ == "__main__":
    main()