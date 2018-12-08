import numpy as np
#import matplotlib.pylab as plt
import heapq

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
state_lattice = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
for i in range(10):
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
