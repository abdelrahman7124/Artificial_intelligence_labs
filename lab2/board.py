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
        2ebd2 beh el nos 3lshan heya feh el 2a8lb hateb2a 3andaha 2ahsn haga 
        fah el pruning momken yeshel branches 2aktar
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
        # rag3 el row 3lshan te3raf tersem feh el gui
        row = self.heights[col]
        self.board[row][col] = player
        self.heights[col] += 1
        self.disc_counter += 1
        return row

    def undo(self, col):
        #2e3ks el tarteb
        row = self.heights[col] - 1
        self.board[row][col] = EMPTY
        self.heights[col] -= 1
        self.disc_counter -= 1

    def is_full(self):
        return self.disc_counter == self.rows * self.cols

    def count_fours(self, player):
        fours = 0
        
        # horizontal
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
            
        # vertical
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
        # check diagonal /  
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

        # check diagonal \ 
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
    
    def drop_distribution(self, col):
        left = self.is_valid(col - 1)
        right = self.is_valid(col + 1)

        if left and right:
            return [(col,0.6),(col - 1,0.2),(col + 1,0.2)]
        if left:
            return [(col,0.6),(col - 1,0.4)]
        if right:
            return [(col,0.6),(col + 1,0.4)]
        return [(col,1.0)]


    def print_board(self):
        symbols = {EMPTY: '.', HUMAN: 'H', AI: 'A'}
        for row in reversed(self.board):
            print(*[symbols[cell] for cell in row])
