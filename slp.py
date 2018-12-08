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
# reflected over x-axis because state lattice (list of lists) access is
# reversed (we will stay consistent with coordinate system defined by
# state lattice)
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

# build state lattice
# determine parameters for lattice (can change based on preference)
nrows = 10
ncols = 10
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

# build state graph
state_graph = {}
# create all nodes
for x in range(len(state_lattice[0])):
    for y in range(len(state_lattice)):
        for h in heading:
            for a in angle:
                state_graph[(x,y,h,a)] = []

print("state_graph = \n", state_graph)
print("# of nodes = ", len(state_graph))
