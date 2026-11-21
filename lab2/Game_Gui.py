import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from board import Board, EMPTY, HUMAN, AI
from minimax import Minimax
from alpha_beta_pruning import Minimax_Alpha_Beta
from TreePrinting import print_tree
from tree_gui import TreeGui

CELL = 80
COLORS = {EMPTY: "white", HUMAN: "red", AI: "yellow"}
ALGORITHMS = {
    "minimax without pruning": Minimax,
    "minimax with pruning": Minimax_Alpha_Beta,
    # "expectiminimax": Expectiminimax,      
}

def get_rows_columns():
    root = tk.Tk()
    root.title("Connect 4 - Setup")
    result = {}

    label = tk.Label(root, text="Please choose the desired rows and columns")
    label_row = tk.Label(root, text="Number of Rows")
    label_col = tk.Label(root, text="Number of Cols")
    label_k = tk.Label(root, text="Search Tree Depth Level")
    label_Algorithms = tk.Label(root, text="Choose the algorithm")
    
    entry_row = tk.Entry(root, width=30)
    entry_col = tk.Entry(root, width=30)
    entry_k = tk.Entry(root, width=30)
    
    algorithm_variable = tk.StringVar(value="minimax with pruning")          
    dropdown_Algorithms = ttk.Combobox(root, textvariable=algorithm_variable, values=list(ALGORITHMS),
                        state="readonly", width=27)
    
    entry_row.insert(0, "6")
    entry_col.insert(0, "7")
    entry_k.insert(0, "3")

    def submit():
        try:
            rows = int(entry_row.get())
            cols = int(entry_col.get())
            k = int(entry_k.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Rows , columns and K must be whole numbers.")
            return
        if rows < 6 or cols < 7 or k <=0 :
            messagebox.showerror("Invalid input", "Rows must be >= 6 and columns >= 7 and k > 0")
            return
        result["rows"] = rows
        result["cols"] = cols
        result["k"] = k
        result["algorithm"] = algorithm_variable.get()
        root.destroy()          

    button = tk.Button(root, text="Start", command=submit)

    label.grid(row=0, column=0, columnspan=2, pady=5)
    
    label_row.grid(row=1, column=0, padx=10)
    entry_row.grid(row=1, column=1, padx=10, pady=5)
    
    label_col.grid(row=2, column=0, padx=10)
    entry_col.grid(row=2, column=1, padx=10, pady=5)
    
    label_k.grid(row=3, column=0, padx=10)
    entry_k.grid(row=3, column=1, padx=10, pady=5)
    
    label_Algorithms.grid(row=4, column=0, padx=10)
    dropdown_Algorithms.grid(row=4, column=1, padx=10, pady=5)
    
    button.grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()
    return result


class Connect4GUI:
    def __init__(self, root, rows, cols,k,algorithm):
        self.k = k
        self.root = root
        self.board = Board(rows, cols)
        self.ai = ALGORITHMS[algorithm](k)    
        self.ai_thinking = False            
        
        self.canvas = tk.Canvas(root, width=cols * CELL, height=rows * CELL, bg="blue")
        self.canvas.pack()
        # button-1 dah el left click 3alael mouse
        self.canvas.bind("<Button-1>", self.on_click)

        
        self.status = tk.Label(root, text="Your turn")
        self.status.pack(pady=5)

        # 2erg3 3lshan te5tar el rows we el columns tany
        self.new_game_button = tk.Button(root, text="New game", command=self.new_game)
        self.new_game_button.pack(pady=5)
        
        self.tree_button = tk.Button(root, text="Draw Tree", command=self.draw_tree)
        self.tree_button.pack(pady=5)

        

        self.draw_board()
        
    def draw_tree(self):
        TreeGui(self.root, self.ai.root,self.k)
        
    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                #zawed x1 and y1 3lshan yeb2a feh masafa bein el cells we el walls
                x1 = j * CELL + 5            
                #2eks el y 3lshan bad2a mn fo2              
                y1 = ((self.board.rows - 1) * CELL) - (i * CELL) + 5
                #2all every x2 and y2 3lshan yeb2a feh masafa bein el cells
                x2 = x1 + CELL - 10                       
                y2 = y1 + CELL - 10
                self.canvas.create_oval(x1, y1, x2, y2, fill=COLORS[self.board.board[i][j]])

    def on_click(self, event):
        if self.ai_thinking:
            return
        column = event.x // CELL
        if not self.board.is_valid(column):
            return
        
        self.board.drop(column,HUMAN)
        self.draw_board()
        if self.check_game_over():
            return

        
        self.ai_thinking = True
        self.root.after(50,self.ai_turn)
        
    def ai_turn(self):
        column,_ = self.ai.decision(self.board)
        row = self.board.drop(column,AI)
        print_tree(self.ai.root)
        
        self.draw_board()
        
        self.root.update()
        self.ai_thinking = False
        if self.check_game_over():
            return
        self.update_status(f"AI played column {column} row {row} | nodes expanded: {self.ai.nodes_expanded} | Your turn")
    
    def update_status(self, message):
        human_score = self.board.count_fours(HUMAN)
        ai_score = self.board.count_fours(AI)
        self.status.config(text=f"{message}   |   You (red): {human_score}   AI (yellow): {ai_score}")

    def check_game_over(self):
        if not self.board.is_full():
            return False

        human_score = self.board.count_fours(HUMAN)
        ai_score = self.board.count_fours(AI)
        if human_score > ai_score:
            result = "You win!"
        elif ai_score > human_score:
            result = "AI wins!"
        else:
            result = "Draw!"

        self.ai_thinking = True          
        self.update_status("Game over")
        messagebox.showinfo("Game over", f"{result}\n\nYou: {human_score}   AI: {ai_score}")
        return True

    def new_game(self):
        self.root.destroy()


def main():
    while True:
        settings = get_rows_columns()
        if not settings:            
            break
        root = tk.Tk()
        root.title("Connect 4")
        Connect4GUI(root, settings["rows"], settings["cols"],settings["k"],settings["algorithm"])
        root.mainloop()             


if __name__ == "__main__":
    main()