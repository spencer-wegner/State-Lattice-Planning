import numpy as np
#import matplotlib.pylab as plt
import heapq
from scipy.spatial import distance

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
# the cost to move along any edge is 1 (uniform across all actions)
# the agent can also stay in its current state with a cost of 0

# this function constructs the state lattice — a list of lists (multi
# dimensional array)
def build_state_lattice(nrows, ncols):
    state_lattice = []
    for i in range(nrows):
        list_row = []
        for j in range(ncols):
            # randomly choose a 0 or 1 for each location - define probability
            # distribution with p = [0.x, 0.x]
            list_row.append(np.random.choice([0,1], p = [0.5, 0.5]))
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
                    state_graph[(x,y,h,a)] = {}
    print("# of nodes = ", len(state_graph))
    return state_graph

# this function creates the edges in the state graph
def assign_edges(state_lattice, state_graph):
    for node in state_graph:
        # upper left corner
        if (node[0] == 0 and node[1] == 0):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, w, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, e, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, n, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, s, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
        # bottom left corner
        elif (node[0] == (len(state_lattice) - 1) and node[1] == 0):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, e, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, w, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, s, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, n, l)] = 1
        # upper right corner
        elif (node[0] == 0 and node[1] == (len(state_lattice[0]) - 1)):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, e, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, w, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, s, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, n, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
        # bottom right corner
        elif (node[0] == (len(state_lattice) - 1) and node[1] == (len(state_lattice[0]) - 1)):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, w, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, e, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, n, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, s, l)] = 1
        # top edge
        elif node[0] == 0:
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, w, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, e, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, w, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, e, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, s, l)] = 1
                state_graph[node][(node[0]+1, node[1]+1, n, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, s, r)] = 1
                state_graph[node][(node[0]+1, node[1]-1, n, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
        # bottom edge
        elif node[0] == (len(state_lattice) - 1):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, e, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, w, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, e, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, w, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, n, r)] = 1
                state_graph[node][(node[0]-1, node[1]+1, s, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, n, l)] = 1
                state_graph[node][(node[0]-1, node[1]-1, s, l)] = 1
        # left edge
        elif node[1] == 0:
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, e, r)] = 1
                state_graph[node][(node[0]+1, node[1]+1, w, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, e, l)] = 1
                state_graph[node][(node[0]-1, node[1]+1, w, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, s, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, n, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, s, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, n, l)] = 1
        # right edge
        elif node[1] == (len(state_lattice[0]) - 1):
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, w, l)] = 1
                state_graph[node][(node[0]+1, node[1]-1, e, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, w, r)] = 1
                state_graph[node][(node[0]-1, node[1]-1, e, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, n, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, s, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, n, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, s, l)] = 1
        # everything else in the middle
        else:
            if node[2] == n and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, e, r)] = 1
                state_graph[node][(node[0]+1, node[1]+1, w, r)] = 1
            elif node[2] == n and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, l)] = 1
                state_graph[node][(node[0], node[1], n, r)] = 1
                state_graph[node][(node[0]-1, node[1], n, c)] = 1
                state_graph[node][(node[0]+1, node[1], n, c)] = 1
            elif node[2] == n and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], n, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, w, l)] = 1
                state_graph[node][(node[0]+1, node[1]-1, e, l)] = 1
            elif node[2] == s and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, w, r)] = 1
                state_graph[node][(node[0]-1, node[1]-1, e, r)] = 1
            elif node[2] == s and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, l)] = 1
                state_graph[node][(node[0], node[1], s, r)] = 1
                state_graph[node][(node[0]+1, node[1], s, c)] = 1
                state_graph[node][(node[0]-1, node[1], s, c)] = 1
            elif node[2] == s and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], s, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, e, l)] = 1
                state_graph[node][(node[0]-1, node[1]+1, w, l)] = 1
            elif node[2] == w and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]-1, node[1]-1, n, r)] = 1
                state_graph[node][(node[0]-1, node[1]+1, s, r)] = 1
            elif node[2] == w and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, l)] = 1
                state_graph[node][(node[0], node[1], w, r)] = 1
                state_graph[node][(node[0], node[1]-1, w, c)] = 1
                state_graph[node][(node[0], node[1]+1, w, c)] = 1
            elif node[2] == w and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], w, c)] = 1
                state_graph[node][(node[0]+1, node[1]-1, s, l)] = 1
                state_graph[node][(node[0]+1, node[1]+1, n, l)] = 1
            elif node[2] == e and node[3] == r:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]+1, node[1]+1, s, r)] = 1
                state_graph[node][(node[0]+1, node[1]-1, n, r)] = 1
            elif node[2] == e and node[3] == c:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, l)] = 1
                state_graph[node][(node[0], node[1], e, r)] = 1
                state_graph[node][(node[0], node[1]+1, e, c)] = 1
                state_graph[node][(node[0], node[1]-1, e, c)] = 1
            elif node[2] == e and node[3] == l:
                state_graph[node][node] = 0
                state_graph[node][(node[0], node[1], e, c)] = 1
                state_graph[node][(node[0]-1, node[1]+1, n, l)] = 1
                state_graph[node][(node[0]-1, node[1]-1, s, l)] = 1
    return state_graph

# this function is a helper functin to update_knowledge
# it breaks all ties (neighbors) with nodes that are blocked
def extract_node(x, y, state_graph):
    # remove nodes with position (x,y)
    to_delete = []
    for node in state_graph:
        if node[0] == x and node[1] == y:
            to_delete.append(node)
    for item in to_delete:
        del state_graph[item]

    # look for connections (neighbors) to a node (x,y) in other nodes
    to_delete = []
    for node in state_graph:
        for neighbor in state_graph[node]:
            if neighbor[0] == x and neighbor[1] == y:
                to_delete.append((node, neighbor))
    for (node, neighbor) in to_delete:
        del state_graph[node][neighbor]
    return state_graph

# this function updates the agent's state graph (agent's knowledge) about
# obstacles in the state lattice - the agent can see adjacent (x,y) positions
def update_knowledge(current_state, current_state_graph, state_lattice, vision):
    new_state_graph = current_state_graph
    x = current_state[0]
    y = current_state[1]
    for i in range(vision):
        # search south
        if (x + (i + 1) < len(state_lattice)):
            if state_lattice[x + (i + 1)][y] == 1:
                new_state_graph = extract_node(x + (i + 1), y, new_state_graph)
        # search north
        if (x - (i + 1)) >= 0:
            if state_lattice[x - (i + 1)][y] == 1:
                new_state_graph = extract_node(x - (i + 1), y, new_state_graph)
        # search east
        if (y + (i + 1)) < len(state_lattice[0]):
            if state_lattice[x][y + (i + 1)] == 1:
                new_state_graph = extract_node(x, y + (i + 1), new_state_graph)
        # search west
        if (y - (i + 1)) >= 0:
            if state_lattice[x][y - (i + 1)] == 1:
                new_state_graph = extract_node(x, y - (i + 1), new_state_graph)
        # search northwest
        if ((x - (i + 1)) >= 0) and ((y - (i + 1)) >= 0):
            if state_lattice[x - (i + 1)][y - (i + 1)] == 1:
                new_state_graph = extract_node(x - (i + 1), y - (i + 1), new_state_graph)
        # search northeast
        if ((x - (i + 1)) >= 0) and ((y + (i + 1)) < len(state_lattice[0])):
            if state_lattice[x - (i + 1)][y + (i + 1)] == 1:
                new_state_graph = extract_node(x - (i + 1), y + (i + 1), new_state_graph)
        # search southwest
        if ((x + (i + 1)) < len(state_lattice)) and ((y - (i + 1)) >= 0):
            if state_lattice[x + (i + 1)][y - (i + 1)] == 1:
                new_state_graph = extract_node(x + (i + 1), y - (i + 1), new_state_graph)
        # search southeast
        if ((x + (i + 1)) < len(state_lattice)) and ((y + (i + 1)) < len(state_lattice[0])):
            if state_lattice[x + (i + 1)][y + (i + 1)] == 1:
                new_state_graph = extract_node(x + (i + 1), y + (i + 1), new_state_graph)
    return new_state_graph

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

# this function calculates the heuristic for the A* search algorithm
def euclidean_distance(current_state, goal):
    # here we use the Euclidean distance
    start_pos = (current_state[0], current_state[1])
    end_pos = (goal[0], goal[1])
    return distance.euclidean(start_pos, end_pos)

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
                        heuristic_score = heuristic(neighbor, goal)
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
    # adjust nrows and ncolumns to your liking
    nrows = 10
    ncols = 10
    state_lattice = build_state_lattice(nrows, ncols)
    state_graph_init = build_state_graph(state_lattice)
    state_graph_complete = assign_edges(state_lattice, state_graph_init)
    agent_state_graph = state_graph_complete # agent starts by thinking entire state space is free

    '''
    possible_locations = []
    for i in range(len(state_lattice)):
        for j in range(len(state_lattice[0])):
            if state_lattice[i][j] == 0:
                possible_locations.append((i,j))
    print(possible_locations)
    start = np.random.choice(possible_locations)
    goal = np.random.choice(possible_locations)
    print("start location: ", start)
    print("goal location: ", goal)
    print("agent vision: ", agent_vision)
    # adjust start and goal states and agent vision to your liking
    '''
    start = (0,0,s,c)
    goal = (8,8,n,l)
    if(state_lattice[start[0]][start[1]]==1):
        state_lattice[start[0]][start[1]]=0
    if(state_lattice[goal[0]][goal[1]]==1):
        state_lattice[goal[0]][goal[1]]=0

    agent_vision = 1

    agent_location = start # variable to keep track of agent's location

    agent_path = []
    total_cost = 0
    total_nodes_expanded = 0
    astar_plans = 0
    while True:
        if agent_location == goal:
            print("Agent reached goal state ", goal)
            agent_path.append(agent_location)
            break
        # update agent's knowledge based on current location
        print("agent updating its knowledge of state graph")
        agent_state_graph = update_knowledge(agent_location, agent_state_graph, state_lattice, agent_vision)
        # make new A* plan
        path, cost, nodes_expanded = astar_search(agent_location, goal, agent_state_graph, state_lattice, euclidean_distance, return_cost = True, return_nexp = True)
        astar_plans += 1
        total_cost += cost
        total_nodes_expanded += nodes_expanded
        '''print("A* planning summary:")
        print("Path: ", path)
        print("Cost: ", cost)
        print("# of nodes expanded: ", nodes_expanded)'''
        for state in path:
            if state_lattice[state[0]][state[1]] == 1: # can't go there!
                break
            else:
                agent_location = state
                agent_path.append(agent_location)
                print(agent_location)
    print('Agent Summary: ')
    print('Number of A* plans = ', astar_plans)
    print('Agent Path = ', agent_path)
    print('Total Path Cost = ', total_cost)
    print('Total Number of Nodes Expanded = ', total_nodes_expanded)

if __name__ == '__main__':
    main()
