import GameBoard as gb

def dfs(initial_state): 
    STACK = []
    states = set()
    VISITED = set()
    
    STACK.append((initial_state, None, None))
    states.add(initial_state)
    
    while STACK:
        node = STACK.pop()
        state = node[0]
        states.remove(state)
        VISITED.add(state)
        
        if gb.is_goal(state):
            return gb.get_path_from_node(node)
        
        for move,neighbour in gb.get_neighbours(state).items():
            if  neighbour not in VISITED and neighbour not in states:
                STACK.append((neighbour, node, move))
                states.add(neighbour)
    return None