import numpy as np

#this program returns the minimum cost path from last row to first row


def print_grid(grid):
    for row in grid:
        for e in row:
            print '\t\t',e,
        print

def mergeTile(tile1, tile2, path):
    for i in path:
        x=i[0]
        for k in range(i[1]):
            tile1[x][k]=tile2[x][k]


print 'tile1'
tile1=np.random.randint(1,1000,size=(5,5))
print tile1.shape
print_grid(tile1)

print 'tile2'
tile2=np.random.randint(1,1000,size=(5,5))
print tile2.shape
print_grid(tile2)

path=[(0,0),(1,1),(2,2),(3,3),(4,4)]
mergeTile(tile1, tile2, path)

print 'merged'
print_grid(tile1)