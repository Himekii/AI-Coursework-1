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

def manhattan(state, state1):
    by, bx, rows = state
    by1, bx1, rows1 = state1
    
    result = 0
    indices = {}
    
    
    # Finds the x and y index of each value
    for row in range(len(rows)): 
        for val in range(len(rows[row])):
            indices[rows[row][val]] = [row,val]

    # Calculates the distance between the x and y index of each values
    # from the corresponding value in the previous state and then adds
    # the value to @result.
    for row in range(len(rows1)):
        for val in range(len(rows1[row])):
            result += abs(indices[rows1[row][val]][0] - row) + abs(indices[rows1[row][val]][1] - val)
   
    return result


def IDAstar(state, goal):
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
    
    
    # Each number multiplied by maximum manhatten (across and up/down) for each number
    maxMoves = (len(state[2])*len(state[2][0]) * (len(state[2])-1 + len(state[2][0])-1))
    
    # Initial threshold of the hueristic of @state
    thresh = manhattan(state, goal)
    
    accesses = 0
    
    # Loops as long as thresh is below the maximum moves (g) + maxmimum depth (h)
    while thresh <= maxMoves + maxMoves:
        predecessor = {(state[0], state[1], tuple(tuple(row) for row in state[2])) : None} # Initialises predecessors with hashable state.
        stack = [[0,state]] # Initialises stack with initial state with depth 0.
        minmanhattan = maxMoves
        while stack:  # While new states still available to search
            
            depth, current = stack.pop() # Destack most recent unseen element
            key = current[0], current[1], tuple(tuple(row) for row in current[2]) # Hashable copy of current
            
            if current == goal: #Checks if current is the target state
                return get_path(key, predecessor), accesses # Returns path from inital state to target state and the number of accesses.
    
            # Heuristic of the node using depth + manhattan distance to goal
            h = depth + manhattan(current, goal) 
    
            if h <= thresh: #If heuristic of node is below threshold
                for next_state in move(current):
                    accesses += 1
                    nextKey = next_state[0], next_state[1], tuple(tuple(row) for row in next_state[2])
                    if nextKey not in predecessor:
                        stack.append([depth + 1, next_state])
                        predecessor[nextKey] = key
            elif h < minmanhattan:
                minmanhattan = h
        
        if minmanhattan != maxMoves: #If minmanhatten has been updated
            thresh = minmanhattan #Update threshold to minmanhatten
        else: #If minmanhatten has not been updated
            thresh += 1 #Increment threshold
    print("No solution found")
    return [], accesses


def main(cases, goal, ind = 0):
    for i in range(len(cases)):
        print(f"Case {i + 1 + ind}")
        start = time.time()
        path, accesses = IDAstar(cases[i], goal)
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
