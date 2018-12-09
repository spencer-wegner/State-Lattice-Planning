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
# reflected over normal x-axis because state lattice (list of lists) access is
# reversed (we will stay consistent with coordinate system defined by
# state lattice)
# because of the way python accesses list of lists (choose row and then column),
# the x-axis is now along the S-N axis and the y-axis in now along the W-E axis
#       S
#       |
#   W -   - E
#       |
#       N
n='north'
s='south'
e='east'
w='west'
heading = [n,s,e,w]
# in physical space, agent can only move to different (x,y) coordinate or
# remain at same (x,y) coordinate and change wheel direction - cannot do both
# at the same time

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

# this function constructs the state graph
def build_state_graph(state_lattice):
    state_graph = {}
    # create all nodes
    for x in range(len(state_lattice[0])):
        for y in range(len(state_lattice)):
            for h in heading:
                for a in angle:
                    state_graph[(x,y,h,a)] = []

    print("# of nodes = ", len(state_graph))

    # create edges between nodes
    for node in state_graph:
        assign_edges(node, state_lattice)

    return state_graph

# this function creates the edges in the state graph
def assign_edges(node, state_lattice):
    if (node[0] == 0 and node[1] == 0): # upper left corner
        pass
    elif (node[0] == (len(state_lattice) - 1) and node[1] == 0): # bottom left corner
        pass
    elif (node[0] == 0 and node[1] == (len(state_lattice[0]) - 1)): # upper right corner
        pass
    elif (node[0] == (len(state_lattice) - 1) and node[1] == (len(state_lattice[0]) - 1)): # bottom right corner
        pass
    elif node[0] == 0: # top edge
        pass
    elif node[0] == (len(state_lattice) - 1): # bottom edge
        pass
    elif node[1] == 0: # left edge
        pass
    elif node[1] = (len(state_lattice[0]) - 1): # right edge
        pass
    else: # everything else in the middle
        pass
        
# main function
def main():
    # build a state lattice
    nrows = 10
    ncols = 10
    state_lattice = build_state_lattice(nrows, ncols)
    print(len(state_lattice[0]))
    #state_graph = build_state_graph(state_lattice)

if __name__ == '__main__':
    main()
