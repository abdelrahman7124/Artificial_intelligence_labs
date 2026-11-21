import board as bd

FOUR_WEIGHT = 1000    
THREE_WEIGHT = 50     
TWO_WEIGHT = 5        
CENTER_WEIGHT = 3     


def get_windows(board):
    #dawr 3ala kol el 4 cell windows elly mawgodein
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

    # diagonal  /  
    for r in range(rows - 3):
        for c in range(cols - 3):
            windows.append([b[r + k][c + k] for k in range(4)])

    # diagonal  \  
    for r in range(rows - 3):
        for c in range(3, cols):
            windows.append([b[r + k][c - k] for k in range(4)])

    return windows


def score_window(window):
    
    ai = window.count(bd.AI)
    human = window.count(bd.HUMAN)

    #law elly entnein mawgodein feh nafs el window 2estahala te3rf tegein point rag3 sefr
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

    return 0   


def evaluate(board):
    score = 0

    # egm3 el 3 we el 4 we el 2 
    for window in get_windows(board):
        score += score_window(window)

    # el nos beyb2a 2ahsan haga law el board fadya 3lshan momken yeshark feh kaza wahda 
    center = board.cols // 2
    for r in range(board.rows):
        if board.board[r][center] == bd.AI:
            score += CENTER_WEIGHT
        elif board.board[r][center] == bd.HUMAN:
            score -= CENTER_WEIGHT

    return score