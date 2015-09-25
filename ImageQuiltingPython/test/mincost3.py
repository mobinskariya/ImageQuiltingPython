import cv2 as cv
import numpy as np
import time

#this program depicts the use of opencv 
#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images
def getMinCost(i,j):
    minimum = 0;
    path[(i,j)] = [(i,j)] + path[(i,j)]
    cost_jp1=0
    cost_j=0
    cost_jm1=0
    list1 = path.get((i,j))
    if i > 0:
        if j < len(imgarr[0])-1 and j > 0:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1)
            minimum = min(cost_jm1, cost_j, cost_jp1)
            if minimum == cost_jm1:
                list2 = path.get((i-1,j-1))
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == 0:
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1)
            minimum = min(cost_j, cost_jp1)
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == len(imgarr[0])-1:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j)
            minimum = min(cost_jm1, cost_j)
            if minimum == cost_jm1:
                list2 = path.get((i-1,j-1))
            else:
                list2 = path.get((i-1,j))
        list1 += list2
        path[(i,j)] = list1
        cost[(i,j)] = imgarr[i,j] + minimum
        return imgarr[i,j] + minimum
    else:
        path[(i,j)] = [(i,j)] + path[(i,j)]
        cost[(i,j)] = imgarr[i,j]
        return imgarr[i,j]

im=cv.imread('image.png',-1)


x_size=500
y_size=500

sample_size=40
overlap_size=10

path={}
cost={}


l_img=np.zeros((x_size,y_size,4))

imgarr=np.random.randint(1,1000,size=(sample_size,overlap_size))

for i in range(sample_size):
    for j in range(overlap_size):
        path[(i,j)]=[]
        cost[(i,j)]=0

print imgarr

mincosts=[]
paths={}
start = time.time()
for i in range(overlap_size):
    mincosts.append(getMinCost(39, i))
    paths[i]=sorted(set(path[(39,i)]))

minidx = mincosts.index(min(mincosts))
print paths[minidx]
print mincosts[minidx]
print time.time() - start

mat = np.array(l_img)
cv.imwrite('testimg.png',mat)