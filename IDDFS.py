import time

def get_path(state, predecessor):
    """
    Given a path specified by  @predecessor dictionary, and a @state
    returns the list of spaces along the path that goes from the state whose predecessor is None to @state
    :param state: state
    :param predecessor: path
    :return:
    """
    current = state
    path = []
    
    while current != None:
        path.append(current)
        current = predecessor[current]
    return path

def move(state):
    """
    move(state):
    generator that returns all states that are reached from
    state, in one move.

    :param state:
    :return: next_state
    """
    by, bx, rows = state
    
    if bx < len(rows[0])-1: #Blank space not on right
        #Move Right
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx+1] = temp_rows[by][bx+1], 0
        next_state = [by, bx+1, temp_rows]
        yield next_state
    if bx > 0: #Blank space not on left
        #Move Left
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by][bx-1] = temp_rows[by][bx-1], 0
        next_state = [by, bx-1, temp_rows]
        yield next_state
    if by < len(rows)-1: #Blank space not at bottom
        #Move Down
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by+1][bx] = temp_rows[by+1][bx], 0
        next_state = [by+1, bx, temp_rows]
        yield next_state
    if by > 0: #Blank space not at top
        #Move Up
        temp_rows = [list(row) for row in rows]
        temp_rows[by][bx], temp_rows[by-1][bx]  = temp_rows[by-1][bx], 0
        next_state = [by-1, bx, temp_rows]
        yield next_state
    
    return None


def iddfs(state, goal):
    """
    NON-RECURSIVE version of the depth first search of a cyclic search space.
    uses a stack of states, @state, and a dictionary @predecessor to store the predecessor of each state along the
    search path.

    calls @get_path
    calls @is_goal

    Note: the dictionary is initialized by the statement:  predecessor = {state : None}. "None" is a marker
    to identify the starting state when reconstruction a path by @get_path
    :param state: state from which the search starts
    :return: path to the goal state
    """
    
    maxMoves = (len(state[2])*len(state[2][0]) * (len(state[2])-1 + len(state[2][0])-1))+1
    
    accesses = 0
    
    for search_depth in range(maxMoves + maxMoves):
        predecessor = {(state[0], state[1], tuple(tuple(row) for row in state[2])) : None}
        stack = [[0,state]]
        while stack:
            
            depth, current = stack.pop()
            key = current[0], current[1], tuple(tuple(row) for row in current[2])
                
            if current == goal:
                return get_path(key, predecessor), accesses

            if depth <= search_depth:
                for next_state in move(current):
                    accesses += 1
                    nextKey = next_state[0], next_state[1], tuple(tuple(row) for row in next_state[2])
                    if nextKey not in predecessor:
                        stack.append([depth + 1, next_state])
                        predecessor[nextKey] = key
                    
    print("No solution found")
    return [], accesses

def main(cases, goal, ind = 0):
    for i in range(len(cases)):
        print(f"Case {i + 1 + ind}")
        start = time.time()
        path, accesses = iddfs(cases[i], goal)
        compTime = time.time() - start
        print(f"States accessed: {accesses}")
        print(f"Path Length: {len(path)}")
        print(f"Computation Time: {compTime * 1000}ms \n\n")
        
cases1 = [[0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
[0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
[2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
[1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
[2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]]

goal1 = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]] 

main(cases1, goal1)

cases2 = [[0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
[2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
[0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
[0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
[2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]]

goal2 = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

main(cases2, goal2, 5)