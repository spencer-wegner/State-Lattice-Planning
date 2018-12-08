import numpy as np
#import matplotlib.pylab as plt
import heapq

c='c'
l='l'
r='r'
n='n'
s='s'
e='e'
w='w'

state_lattice = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
for i in range(10):
    print(state_lattice[i])

graph={(0,0,c,n):[(1,0,c,n),(0,0,c,n),(0,0,r,n)]}

#god damnit why is this so confusing, I feel like it shouldn't be, ya know?
