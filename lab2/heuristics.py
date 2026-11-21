import board as bd

FOUR_WEIGHT = 1000    
THREE_WEIGHT = 50     
TWO_WEIGHT = 5        
ONE_WEIGHT = 1        
PARITY_WEIGHT = 15    
CENTER_WEIGHT = 3     


def get_windows(board):
    #dawr 3ala kol el 4 cell windows elly mawgodein
    #kol window bterga3 ma3aha el rows bta3et el cells 3lshan ne3raf el cell el fadya fe anhy row
    b, rows, cols = board.board, board.rows, board.cols
    windows = []

    # horizontal  
    for r in range(rows):
        for c in range(cols - 3):
            windows.append(([b[r][c + k] for k in range(4)], [r] * 4))

    # vertical  
    for r in range(rows - 3):
        for c in range(cols):
            windows.append(([b[r + k][c] for k in range(4)], [r + k for k in range(4)]))

    # diagonal  /  
    for r in range(rows - 3):
        for c in range(cols - 3):
            windows.append(([b[r + k][c + k] for k in range(4)], [r + k for k in range(4)]))

    # diagonal  \  
    for r in range(rows - 3):
        for c in range(3, cols):
            windows.append(([b[r + k][c - k] for k in range(4)], [r + k for k in range(4)]))

    return windows


def score_window(window, window_rows, rows):

    ai = window.count(bd.AI)
    human = window.count(bd.HUMAN)

    if ai > 0 and human > 0:
        return 0

    if ai == 4:
        return FOUR_WEIGHT
    if ai == 3:

        empty_row = window_rows[window.index(bd.EMPTY)]
        if rows % 2 == 0 and empty_row % 2 == 1:
            return THREE_WEIGHT + PARITY_WEIGHT
        return THREE_WEIGHT
    if ai == 2:
        return TWO_WEIGHT
    if ai == 1:
        return ONE_WEIGHT

    if human == 4:
        return -FOUR_WEIGHT
    if human == 3:
        empty_row = window_rows[window.index(bd.EMPTY)]
        if rows % 2 == 0 and empty_row % 2 == 0:
            return -(THREE_WEIGHT + PARITY_WEIGHT)
        return -THREE_WEIGHT
    if human == 2:
        return -TWO_WEIGHT
    if human == 1:
        return -ONE_WEIGHT

    return 0   


def evaluate(board):
    score = 0

    for window, window_rows in get_windows(board):
        score += score_window(window, window_rows, board.rows)

    # el nos beyb2a 2ahsan haga law el board fadya 3lshan momken yeshark feh kaza wahda
    # law 3adad el columns zawgy fe 3amoodein fe el nos
    centers = [board.cols // 2]
    if board.cols % 2 == 0:
        centers.append(board.cols // 2 - 1)
    for center in centers:
        for r in range(board.rows):
            if board.board[r][center] == bd.AI:
                score += CENTER_WEIGHT
            elif board.board[r][center] == bd.HUMAN:
                score -= CENTER_WEIGHT

    return score