import math
import time

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

# def move_blank(i,j,n):
#     if i+1 < n:
#         yield (i+1,j)   
#     if i-1 >= 0:
#         yield (i-1,j)
#     if j+1 < n:
#         yield (i,j+1)
#     if j-1 >= 0:
#         yield (i,j-1)

# def move(state):
#     [i,j,grid]=state
#     n = len(grid)
#     for pos in move_blank(i,j,n):
#         i1,j1 = pos
#         grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
#         yield [i1,j1,grid]
#         grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]


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
        
        if prev_node == key:
            prev_node = predecessor[prev_node]
        
        if key not in predecessor: #If node is unexplored
            predecessor[key] = prev_node #Add the node to predecessor with its parent node
        else:
            stack.pop()
            continue
            
        if current == goal:
            return get_path(key, predecessor)

        for next_state in move(current):
            stack.append(next_state)
        
        
        prev_node = key
    print("No solution found")
    return [state]

def iddfs_stack(state, goal):
    return 0;

def manhattan(state, state1):
    by, bx, rows = state
    by1, bx1, rows1 = state1
    
    result = 0
    indices = {}
    
    
    for row in range(len(rows)):
        for val in range(len(rows[row])):
            indices[rows[row][val]] = [row,val]

    for row in range(len(rows1)):
        for val in range(len(rows1[row])):
            result += abs(indices[rows1[row][val]][0] - row) + abs(indices[rows1[row][val]][1] - val)
   
    return result

def ida(state, goal):
    """
    How to apply Iterative Deepening to A*?
    1. A pass consists in expanding all nodes that have an value less
        than or equal to a bound (threshold).
    2. The initial bound is the value of the start state.
    3. Expand all nodes that have an value less than or equal to the
        actual bound (threshold).
    4. If the goal is not found, update the bound,
        the next bound is the smallest value of the states generated in
        the search but not expanded.
    5. Repeat (do another pass) until the goal is reached.
    6. When the bound is updated, the search restarts from the start
        state (ID).
    """
    
    
    #Each number multiplied by maximum manhatten (across and up/down) for each number
    maxmanhattan = (len(state[2])*len(state[2][0]) * (len(state[2])-1 + len(state[2][0])-1))
    thresh = manhattan(state, goal)
    
    accesses = 0
    
    while thresh <= maxmanhattan:
        minmanhattan = maxmanhattan
        predecessor = {(state[0], state[1], tuple(tuple(row) for row in state[2])) : None}
        stack = [[0,state]]
        while stack:
            
            depth, current = stack.pop() #Destack most recent unseen element
            key = current[0], current[1], tuple(tuple(row) for row in current[2])
            
            if current == goal:
                return get_path(key, predecessor), accesses
    
            h = depth + manhattan(current, goal)
    
            if h <= thresh:
                for next_state in move(current):
                    accesses += 1
                    nextKey = next_state[0], next_state[1], tuple(tuple(row) for row in next_state[2])
                    if nextKey not in predecessor:
                        predecessor[nextKey] = key
                        stack.append([depth + 1, next_state])
            elif h < minmanhattan:
                minmanhattan = h
                
        thresh = minmanhattan
    print("No solution found")
    return [state]

"""
(1) Case number.
(2) The number of moves to solve the case (i.e. the number of states – 1 in the
shortest path from the initial state to the goal).
(3) The number of nodes opened, that is, the number of yield made by the move
method during the search for a solution.
(4) The computing time the search took"""

def main(cases, goal, ind = 0):
    for i in range(len(cases)):
        print(f"Case {i + 1 + ind}")
        start = time.time()
        path, accesses = ida(cases[i], goal)
        compTime = time.time() - start
        print(f"States expanded: {accesses}")
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



