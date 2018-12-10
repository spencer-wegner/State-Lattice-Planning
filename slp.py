import numpy as np
#import matplotlib.pylab as plt
import heapq
import random

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
            list_row.append(0)
        state_lattice.append(list_row)
    # in the state lattice, a '0' means the (x,y) position is open and a '1'
    # means the (x,y) position is blocked

    # *** add functionality to randomly insert '1s' into state lattice

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

        elif node[0] == 0: # top edge
            pass

        elif node[0] == (len(state_lattice) - 1): # bottom edge
            pass

        elif node[1] == 0: # left edge
            pass

        elif node[1] == (len(state_lattice[0]) - 1): # right edge
            pass

        else: # everything else in the middle
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

# main function
def main():
    # build a state lattice
    nrows = 10
    ncols = 10
    state_lattice = build_state_lattice(nrows, ncols)
    state_graph_init = build_state_graph(state_lattice)
    state_graph_complete = assign_edges(state_lattice, state_graph_init)
    ctr = 0
    for node in state_graph_complete:
        if state_graph_complete[node] == []:
            ctr += 1
        print(state_graph_complete[node])
    print(ctr)

if __name__ == '__main__':
    main()
