# +------------------------------------------------------------
# Utility functions
def print_state(state):
    by, bx, rows = state
    print(bx, by)
    for row in rows:
        print(row, '\n', end = '')


def trans(state, state1):
    by, bx, rows = state
    by1, bx1, rows1 = state1
    if bx < bx1:
        print("moved blank left")
    elif bx > bx1:
        print("moved blank right")
    elif by < by1:
        print("moved blank up")
    elif by > by1:
        print("moved blank down")
    else:
        print("Error")
        raise("Error")

def print_path(path):
    print_state(path[0])
    for i in range(1, len(path)):
        trans(path[i - 1], path[i])
        print_state(path[i])

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
    
    
    if bx < 2: #Blank space not on right
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
    if by < 2: #Blank space not at bottom
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


def dfs_stack(state, goal):
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
    stack = [state]
    
    predecessor = {}
    prev_node = None
    
    while stack:
        current = stack[-1]
        
        key = current[0], current[1], tuple(tuple(row) for row in current[2])
        
        if key not in predecessor:
            predecessor[key] = prev_node
        else:
            stack.pop()
            continue
            
        if current == goal:
            return get_path(key, predecessor)

        offspring = move(current)

        for next_state in offspring:
            stack.append(next_state)
            
        prev_node = key
    print("No solution found")

def iddfs_stack(state, goal):
    return 0;

def ida_stack(state, goal):
    return 0;

print("\nDFS STACK:")
goal = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]] 
path = dfs_stack([0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]], goal)
print_path(path)