import time
from board import Board, HUMAN, AI
from minimax import Minimax
from alpha_beta_pruning import Minimax_Alpha_Beta
from TreePrinting import print_tree


def ask_int(prompt, default, low=None, high=None):
    while True:
        text = input(f"{prompt} [{default}]: ").strip()
        if text == "":
            return default
        if text.lstrip("-").isdigit():
            value = int(text)
            if (low is None or value >= low) and (high is None or value <= high):
                return value
        print("  invalid value, try again")


def show(board):
    # Board + column numbers + current score
    print()
    board.print_board()
    print(*[c % 10 for c in range(board.cols)])
    print(f"Score  ->  Human (H): {board.count_fours(HUMAN)}   AI (A): {board.count_fours(AI)}")


def main():
    print("=== Connect 4 - terminal test ===")
    algo = ask_int("Algorithm: 1 = Minimax, 2 = Alpha-Beta", 2, 1, 2)
    k = ask_int("Depth K", 3, 1)
    rows = ask_int("Rows", 6, 6)
    cols = ask_int("Columns", 7, 7)
    human_first = ask_int("Who starts: 1 = Human, 2 = AI", 1, 1, 2) == 1
    show_tree = input("Print the tree each AI turn? (y/n) [y]: ").strip().lower() != "n"

    board = Board(rows, cols)
    ai = Minimax(k) if algo == 1 else Minimax_Alpha_Beta(k)
    name = "Minimax" if algo == 1 else "Alpha-Beta"
    turn = HUMAN if human_first else AI

    show(board)
    while not board.is_full():
        if turn == HUMAN:
            col = ask_int(f"Your move (0-{cols - 1})", board.valid_moves()[0], 0, cols - 1)
            if not board.is_valid(col):
                print("  column is full, choose another one")
                continue
            board.drop(col, HUMAN)
            print(f"You played column {col}")
        else:
            print(f"\nAI thinking ({name}, K={k}) ...")
            start = time.perf_counter()
            col, value = ai.decision(board)
            elapsed = time.perf_counter() - start

            if show_tree:
                print("\n----- search tree -----")
                print_tree(ai.root)
                print("-----------------------")
            board.drop(col, AI)
            print(f"AI played column {col}  |  value = {value}  |  "
                  f"nodes expanded = {ai.nodes_expanded}  |  time = {elapsed * 1000:.1f} ms")

        show(board)
        turn = AI if turn == HUMAN else HUMAN

    h, a = board.count_fours(HUMAN), board.count_fours(AI)
    print("\n=== Game over ===")
    print(f"Final score  ->  Human: {h}   AI: {a}")
    print("You win!" if h > a else "AI wins!" if a > h else "Draw!")


if __name__ == "__main__":
    main()
