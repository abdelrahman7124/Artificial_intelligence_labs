GOAL_STATE = ( 0, 1, 2, 3, 4, 5, 6, 7, 8)
MOVES = {"UP":    (-1, 0),
         "DOWN":  ( 1, 0), 
         "LEFT":  ( 0,-1),
         "RIGHT": ( 0, 1)
        }

def is_goal(state):
    return state == GOAL_STATE

def get_neighbours(state):
    zero_idx = state.index(0)
    neighbours = {}
    row = zero_idx // 3
    col = zero_idx % 3
    for move,(r,c) in MOVES.items():
        new_row = row + r
        new_col = col + c
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_zero_idx] = new_state[new_zero_idx], new_state[zero_idx]
            neighbours[move] = tuple(new_state)
            
    return neighbours


def get_path_from_node(node):
    path = []
    cost = 0
    while node[1] is not None:
        path.append(node[2])
        node = node[1]
        cost += 1
    return path[::-1],cost