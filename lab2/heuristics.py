"""
heuristic.py - evaluates a board for the AI.

Returns a number: positive = good for the AI, negative = good for the human.
It looks at every 4-cell window (every place a four can be made) and scores
how close each window is to becoming a four, plus a bonus for center control.
"""

from board import EMPTY, HUMAN, AI

# ---- weights ----
FOUR_WEIGHT = 1000    # a completed four (a real point)
THREE_WEIGHT = 50     # 3 discs + 1 empty  -> a threat / candidate point
TWO_WEIGHT = 5        # 2 discs + 2 empty  -> building toward a threat
CENTER_WEIGHT = 3     # per disc in the center column


def get_windows(board):
    """Return every 4-cell window on the board as a list of 4 cell values."""
    b, rows, cols = board.board, board.rows, board.cols
    windows = []

    # horizontal  
    for r in range(rows):
        for c in range(cols - 3):
            windows.append([b[r][c + k] for k in range(4)])

    # vertical  
    for r in range(rows - 3):
        for c in range(cols):
            windows.append([b[r + k][c] for k in range(4)])

    # diagonal  /  (up-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            windows.append([b[r + k][c + k] for k in range(4)])

    # diagonal  \  (up-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            windows.append([b[r + k][c - k] for k in range(4)])

    return windows


def score_window(window):
    """Points for one window: positive for AI, negative for human."""
    ai = window.count(AI)
    human = window.count(HUMAN)

    # both players inside -> nobody can ever make a four here
    if ai > 0 and human > 0:
        return 0

    if ai == 4:
        return FOUR_WEIGHT
    if ai == 3:
        return THREE_WEIGHT
    if ai == 2:
        return TWO_WEIGHT

    if human == 4:
        return -FOUR_WEIGHT
    if human == 3:
        return -THREE_WEIGHT
    if human == 2:
        return -TWO_WEIGHT

    return 0   # empty window or a single disc


def evaluate(board):
    """Heuristic value of the board from the AI's point of view."""
    score = 0

    # 1-3) fours, threats and twos from every window
    for window in get_windows(board):
        score += score_window(window)

    # 4) center control
    center = board.cols // 2
    for r in range(board.rows):
        if board.board[r][center] == AI:
            score += CENTER_WEIGHT
        elif board.board[r][center] == HUMAN:
            score -= CENTER_WEIGHT

    return score