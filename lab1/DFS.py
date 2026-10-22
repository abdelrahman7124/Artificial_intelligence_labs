import GameBoard as gb

def dfs(initial_state): 
    STACK = []
    VISITED = set()
    
    STACK.append((initial_state,[]))
    
    while STACK:
        state,path = STACK.pop()
        if state in VISITED:
            continue
        VISITED.add(state)
        
        if gb.is_goal(state):
            return path
        
        for move,neighbour in gb.get_neighbours(state).items():
            if  neighbour not in VISITED:
                STACK.append((neighbour, path + [move]))
    return None