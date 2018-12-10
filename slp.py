import numpy as np
#import matplotlib.pylab as plt
import heapq

# agent wheel direction
c='center' # 0 degrees, straight ahead
l='left' # -45 degrees, angled left
r='right' # 45 degrees, angled right
angle = [c,l,r]
# agent heading/direction
# because of the way python accesses list of lists (choose row and then column),
# the x-axis is now along the N-S axis and the y-axis in now along the E-W axis
# we will stick to the normal cardinal directions to keep in straight in our
# heads - that means increasing x goes south and increasing y goes east
# (0,0) is at the northwest corner of the state space
#       N
#       |
#   W -   - E
#       |
#       S
n='north'
s='south'
e='east'
w='west'
heading = [n,s,e,w]
# in physical space, agent can only move to different (x,y) coordinate or
# remain at same (x,y) coordinate and change wheel direction - cannot do both
# at the same time
# when the agent moves to a different (x,y) location with turned wheels,
# their wheels will remain in the same turned position when they arrive
# so the agent will need to make an extra step to adjust the wheels if it
# wants to move straight after it makes a turn

# this function constructs the state lattice — a list of lists (multi
# dimensional array)
def build_state_lattice(nrows, ncols):
    state_lattice = []
    for i in range(nrows):
        list_row = []
        for j in range(ncols):
            # randomly choose a 0 or 1 for each location - define probability
            # distribution with p = [0.x, 0.x]
            list_row.append(np.random.choice([0,1], p = [0.9, 0.1]))
        state_lattice.append(list_row)
    # in the state lattice, a '0' means the (x,y) position is open and a '1'
    # means the (x,y) position is blocked

    print("State Lattice:")
    for i in range(nrows):
        print(state_lattice[i])

    return state_lattice

# this function initializes ONLY the nodes in the state graph
def build_state_graph(state_lattice):
    state_graph = {}
    # create all nodes
    for x in range(len(state_lattice[0])):
        for y in range(len(state_lattice)):
            for h in heading:
                for a in angle:
                    state_graph[(x,y,h,a)] = []
    print("# of nodes = ", len(state_graph))
    return state_graph

# this function creates the edges in the state graph
def assign_edges(state_lattice, state_graph):
    for node in state_graph:
        # upper left corner
        if (node[0] == 0 and node[1] == 0):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]+1, node[1]+1, w, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]+1, e, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]+1, n, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]+1, s, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
        # bottom left corner
        elif (node[0] == (len(state_lattice) - 1) and node[1] == 0):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]+1, e, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]-1, node[1]+1, w, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]+1, s, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]+1, n, l))
        # upper right corner
        elif (node[0] == 0 and node[1] == (len(state_lattice[0]) - 1)):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]+1, node[1]-1, e, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]-1, w, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]-1, s, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]-1, n, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
        # bottom right corner
        elif (node[0] == (len(state_lattice) - 1) and node[1] == (len(state_lattice[0]) - 1)):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]-1, w, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]-1, node[1]-1, e, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]-1, n, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]-1, s, l))
        # top edge
        elif node[0] == 0:
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]+1, node[1]+1, w, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]+1, node[1]-1, e, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]-1, w, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]+1, e, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]-1, s, l))
                state_graph[node].append((node[0]+1, node[1]+1, n, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]+1, s, r))
                state_graph[node].append((node[0]+1, node[1]-1, n, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
        # bottom edge
        elif node[0] == (len(state_lattice) - 1):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]+1, e, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]-1, w, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]-1, node[1]-1, e, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]-1, node[1]+1, w, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]-1, n, r))
                state_graph[node].append((node[0]-1, node[1]+1, s, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]+1, n, l))
                state_graph[node].append((node[0]-1, node[1]-1, s, l))
        # left edge
        elif node[1] == 0:
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]+1, e, r))
                state_graph[node].append((node[0]+1, node[1]+1, w, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]+1, e, l))
                state_graph[node].append((node[0]-1, node[1]+1, w, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]+1, s, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]+1, n, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]+1, s, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]+1, n, l))
        # right edge
        elif node[1] == (len(state_lattice[0]) - 1):
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]-1, w, l))
                state_graph[node].append((node[0]+1, node[1]-1, e, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]-1, w, r))
                state_graph[node].append((node[0]-1, node[1]-1, e, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]-1, n, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]-1, s, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]-1, n, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]-1, s, l))
        # everything else in the middle
        else:
            if node[2] == n and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]+1, e, r))
                state_graph[node].append((node[0]+1, node[1]+1, w, r))
            elif node[2] == n and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, l))
                state_graph[node].append((node[0], node[1], n, r))
                state_graph[node].append((node[0]-1, node[1], n, c))
                state_graph[node].append((node[0]+1, node[1], n, c))
            elif node[2] == n and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], n, c))
                state_graph[node].append((node[0]-1, node[1]-1, w, l))
                state_graph[node].append((node[0]+1, node[1]-1, e, l))
            elif node[2] == s and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]-1, w, r))
                state_graph[node].append((node[0]-1, node[1]-1, e, r))
            elif node[2] == s and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, l))
                state_graph[node].append((node[0], node[1], s, r))
                state_graph[node].append((node[0]+1, node[1], s, c))
                state_graph[node].append((node[0]-1, node[1], s, c))
            elif node[2] == s and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], s, c))
                state_graph[node].append((node[0]+1, node[1]+1, e, l))
                state_graph[node].append((node[0]-1, node[1]+1, w, l))
            elif node[2] == w and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]-1, node[1]-1, n, r))
                state_graph[node].append((node[0]-1, node[1]+1, s, r))
            elif node[2] == w and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, l))
                state_graph[node].append((node[0], node[1], w, r))
                state_graph[node].append((node[0], node[1]-1, w, c))
                state_graph[node].append((node[0], node[1]+1, w, c))
            elif node[2] == w and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], w, c))
                state_graph[node].append((node[0]+1, node[1]-1, s, l))
                state_graph[node].append((node[0]+1, node[1]+1, n, l))
            elif node[2] == e and node[3] == r:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]+1, node[1]+1, s, r))
                state_graph[node].append((node[0]+1, node[1]-1, n, r))
            elif node[2] == e and node[3] == c:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, l))
                state_graph[node].append((node[0], node[1], e, r))
                state_graph[node].append((node[0], node[1]+1, e, c))
                state_graph[node].append((node[0], node[1]-1, e, c))
            elif node[2] == e and node[3] == l:
                state_graph[node].append(node)
                state_graph[node].append((node[0], node[1], e, c))
                state_graph[node].append((node[0]-1, node[1]+1, n, l))
                state_graph[node].append((node[0]-1, node[1]-1, s, l))
    return state_graph

# this function constructs a path that the agent follows through the state space
def path(previous, s):
    '''
    'previous' is a dictionary chaining together the predecessor state that led
    to each state - 's' will be None for the initial state
    otherwise, start from the last state 's' and recursively trace 'previous'
    back to the initial state, constructing a list of states visited as we go
    '''
    if s is None:
        return []
    else:
        return path(previous, previous[s]) + [s]

# this function calculates the total cost of the path that the agent takes
def pathcost(path, step_costs):
    '''
    add up the step costs along a path, which is assumed to be a list output
    from the 'path' function above
    '''
    cost = 0
    for s in range(len(path) - 1):
        cost += step_costs[path[s]][path[s+1]]
    return cost

# this class provides methods to initialize and edit the priority queue
# that is used in A* search
class Frontier_PQ:
    def __init__(self, start, cost = 0):
        self.start = start
        # initialize dictionary - keys are states (x,y,h,a) and values are
        # minimum distances to those states from the start state
        self.states = dict({start : 0})
        self.q = [(0, start)] # initialize priority queue (cost, state)
    def add(self, state, cost): # add a (cost, state) tuple to the frontier
        heapq.heappush(self.q, (cost, state))
    def pop(self): # return the lowest cost (cost, state) tuple, and pop it off of the frontier
        return heapq.heappop(self.q)
    # if a lower path cost to a state already on the frontier is found, it should be replaced
    def replace(self, state, cost):
        self.states[state] = cost

def astar_search(start, goal, state_graph, state_lattice, heuristic, return_cost = False, return_nexp = False):
    my_frontier = Frontier_PQ(start) # create a priority queue
    visited = []
    prev = {start : None} # initialize prev dictionary (keys are successors, values are predecessors)
    while (my_frontier.q): # while the priority queue is not empty
        x = my_frontier.pop() # pop state off of queue (with heapq it will be the lowest cost tuple)
        if x[1] not in visited: # if we haven't visited the state yet
            visited.append(x[1])
            if x[1] == goal: # We found it!
                if return_nexp: # return number of nodes expanded
                    solution_path = path(prev, x[1])
                    nexp = len(visited) # number of nodes expanded is the number of nodes visited
                    if return_cost:
                        path_cost = pathcost(solution_path, state_graph)
                        return (solution_path, path_cost, nexp)
                    else:
                        return (solution_path, nexp)
                else:
                    if return_cost:
                        solution_path = path(prev, x[1])
                        path_cost = pathcost(solution_path, state_graph)
                        return (solution_path, path_cost)
                    else:
                        return path(prev, x[1])
            else: # we haven't found the goal yet...
                for neighbor in state_graph[x[1]]:
                    if neighbor not in visited:
                        if neighbor not in prev:
                            # add neighbor as key and current state as value
                            prev[neighbor] = x[1] # x[1] is predecessor to neighbor
                        current_cost = my_frontier.states[x[1]]
                        additional_cost = state_graph[x[1]][neighbor]
                        new_cost = current_cost + additional_cost
                        heuristic_score = heuristic(neighbor)
                        astar_score = new_cost + heuristic_score
                        my_frontier.add(neighbor, astar_score) # add neighbor and cost to priority queue
                        if neighbor not in my_frontier.states:
                            my_frontier.states[neighbor] = new_cost
                        if new_cost < my_frontier.states[neighbor]:
                            # update states dictionary if cheaper path is found
                            my_frontier.replace(neighbor, new_cost)
                            prev[neighbor] = x[1]


# main function
def main():
    # build a state lattice
    nrows = 10
    ncols = 10
    state_lattice = build_state_lattice(nrows, ncols)
    state_graph_init = build_state_graph(state_lattice)
    state_graph_complete = assign_edges(state_lattice, state_graph_init)
    #for node in state_graph_complete:
        #print(state_graph_complete[node])

if __name__ == '__main__':
    main()
