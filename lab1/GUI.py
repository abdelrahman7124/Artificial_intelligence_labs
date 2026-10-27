from tkinter import *
from tkinter import messagebox
import random
import time

import GameBoard as gb
import BFS as bfs
import DFS as dfs
import IDS as ids
import A_STAR as a_star


TILE_SIZE = 100
SLOW_SPEED = 500
FAST_SPEED = 50

TILE_COLOR = "white"
NUMBER_COLOR = "gray20"
BLANK_COLOR = "gray74"
BACKGROUND_COLOR = "gray62"

game = {
    "boards": [],
    "moves": [],
    "step": 0,
    "playing": False,
    "speed": SLOW_SPEED
}



def is_solvable(state):
    tiles = []
    for tile in state:
        if tile != 0:
            tiles.append(tile)
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1,len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0


def get_initial_state():
    text = state_entry.get().replace(","," ")
    numbers = []
    for number in text.split():
        if not number.isdigit():
            return None
        numbers.append(int(number))
    if sorted(numbers) != [0,1,2,3,4,5,6,7,8]:
        return None
    return tuple(numbers)


def draw_board(state):
    canvas.delete("all")
    for i in range(9):
        x = (i % 3) * TILE_SIZE
        y = (i // 3) * TILE_SIZE
        if state[i] == 0:
            canvas.create_rectangle(x + 4,y + 4,x + TILE_SIZE - 4,y + TILE_SIZE - 4,fill=BLANK_COLOR,outline="")
        else:
            canvas.create_rectangle(x + 4,y + 4,x + TILE_SIZE - 4,y + TILE_SIZE - 4,fill=TILE_COLOR,outline="")
            canvas.create_text(x + TILE_SIZE / 2,y + TILE_SIZE / 2,text=str(state[i]),font=("Arial",32,"bold"),fill=NUMBER_COLOR)


def show_step(new_step):
    boards = game["boards"]
    moves = game["moves"]
    if len(boards) == 0:
        return
    if new_step < 0:
        new_step = 0
    if new_step > len(boards) - 1:
        new_step = len(boards) - 1
    game["step"] = new_step

    draw_board(boards[new_step])
    if new_step == 0:
        step_label.config(text="Step 0 / " + str(len(moves)) + "   (start)")
    else:
        step_label.config(text="Step " + str(new_step) + " / " + str(len(moves)) + "   (" + moves[new_step - 1] + ")")


def random_board():
    state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(state)
    while not is_solvable(state):
        random.shuffle(state)
    text = ""
    for tile in state:
        text += str(tile) + ","
    state_entry.delete(0,END)
    state_entry.insert(0,text[:-1])
    draw_board(state)


def solve():
    initial_state = get_initial_state()
    if initial_state is None:
        messagebox.showerror("Error","Write the numbers from 0 to 8, each one once.\nExample: 1,2,5,3,4,0,6,7,8")
        return
    if not is_solvable(initial_state):
        messagebox.showwarning("Unsolvable","This board can't reach the goal state.")
        return

    stop()
    draw_board(initial_state)
    choice = algorithm.get()
    result_label.config(text="Solving with " + choice + "...")
    root.update()

    start_time = time.time()
    if choice == "BFS":
        result = bfs.bfs(initial_state)
    elif choice == "DFS":
        result = dfs.dfs(initial_state)
    elif choice == "IDS":
        result = ids.ids(initial_state)
    elif choice == "A* Manhattan":
        result = a_star.a_star(initial_state,"manhattan")
    else:
        result = a_star.a_star(initial_state,"euclidean")
    running_time = time.time() - start_time

    if result is None:
        result_label.config(text="No path found to the goal state.")
        return

    path,cost,nodes_expanded,max_depth_reached = result
    boards = [initial_state]
    for move in path:
        boards.append(gb.get_neighbours(boards[-1])[move])
    game["boards"] = boards
    game["moves"] = path

    result_label.config(text=choice + "   |   Cost of path: " + str(cost) + "   |   Time: " + str(round(running_time,3)) + " s\n"
                        + "Nodes expanded: " + str(nodes_expanded) + "   |   Search depth: " + str(max_depth_reached))
    show_step(0)


def play_pause():
    if game["playing"]:
        stop()
    elif len(game["boards"]) > 0:
        if game["step"] == len(game["boards"]) - 1:
            show_step(0)
        game["playing"] = True
        play_button.config(text="Pause")
        next_frame()


def next_frame():
    if not game["playing"]:
        return
    if game["step"] == len(game["boards"]) - 1:
        stop()
        return
    show_step(game["step"] + 1)
    root.after(game["speed"],next_frame)


def stop():
    game["playing"] = False
    play_button.config(text="Play")


def change_speed():
    if game["speed"] == SLOW_SPEED:
        game["speed"] = FAST_SPEED
        speed_button.config(text="Speed: Fast")
    else:
        game["speed"] = SLOW_SPEED
        speed_button.config(text="Speed: Slow")


def go_first():
    show_step(0)

def go_back():
    show_step(game["step"] - 1)

def go_next():
    show_step(game["step"] + 1)

def go_last():
    show_step(len(game["boards"]) - 1)



root = Tk()
root.title("8-Puzzle Solver")

Label(root,text="Initial state:").grid(column=0,row=0)
state_entry = Entry(root,width=20)
state_entry.insert(0,"1,2,5,3,4,0,6,7,8")
state_entry.grid(column=1,row=0)
Button(root,text="Random",command=random_board).grid(column=2,row=0)
algorithm = StringVar(value="BFS")
OptionMenu(root,algorithm,"BFS","DFS","IDS","A* Manhattan","A* Euclidean").grid(column=3,row=0)
Button(root,text="Solve",command=solve).grid(column=4,row=0)

canvas = Canvas(root,width=3 * TILE_SIZE,height=3 * TILE_SIZE,bg=BACKGROUND_COLOR)
canvas.grid(column=0,row=1,columnspan=5,pady=10)

result_label = Label(root,text="Pick an algorithm and press Solve")
result_label.grid(column=0,row=2,columnspan=5)
step_label = Label(root,text="")
step_label.grid(column=0,row=3,columnspan=5)

Button(root,text="|<",width=5,command=go_first).grid(column=0,row=4)
Button(root,text="<",width=5,command=go_back).grid(column=1,row=4)
play_button = Button(root,text="Play",width=5,command=play_pause)
play_button.grid(column=2,row=4)
Button(root,text=">",width=5,command=go_next).grid(column=3,row=4)
Button(root,text=">|",width=5,command=go_last).grid(column=4,row=4)

speed_button = Button(root,text="Speed: Slow",command=change_speed)
speed_button.grid(column=0,row=5,columnspan=5,pady=10)

draw_board((1,2,5,3,4,0,6,7,8))
root.mainloop()
