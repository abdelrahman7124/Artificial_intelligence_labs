import GameBoard as gb
from collections import deque

def bfs(initial_state): 
    QUEUE = deque()
    states = set()
    VISITED = set()
    
    QUEUE.append((initial_state, None, None))
    states.add(initial_state)
    
    while QUEUE:
        node = QUEUE.popleft()
        state = node[0]
        states.remove(state)
        VISITED.add(state)
        
        if gb.is_goal(state):
            return gb.get_path_from_node(node)
        
        for move,neighbour in gb.get_neighbours(state).items():
            if  neighbour not in VISITED and neighbour not in states:
                QUEUE.append((neighbour, node, move))
                states.add(neighbour)
    return None