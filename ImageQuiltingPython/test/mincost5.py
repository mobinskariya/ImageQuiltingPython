import cv2 as cv
import numpy as np
import time

#this program depicts the use of opencv 
#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images
def getMinCost(i,j,imgarr,path,cost):
    minimum = 0;
    path[(i,j)] = [(i,j)] + path[(i,j)]
    cost_jp1=0
    cost_j=0
    cost_jm1=0
    list1 = path.get((i,j))
    if i > 0:
        if j < len(imgarr[0])-1 and j > 0:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1,imgarr,path,cost)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,imgarr,path,cost)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1,imgarr,path,cost)
            minimum = min(cost_jm1, cost_j, cost_jp1)
            if minimum == cost_jm1:
                list2 = path.get((i-1,j-1))
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == 0:
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,imgarr,path,cost)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1,imgarr,path,cost)
            minimum = min(cost_j, cost_jp1)
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == len(imgarr[0])-1:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1,imgarr,path,cost)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,imgarr,path,cost)
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


def getMinPath(imgarr):
    path={}
    cost={}
    
    height=len(imgarr)
    width=len(imgarr[0])
    
    for i in range(height):
        for j in range(width):
            path[(i,j)]=[]
            cost[(i,j)]=0
    
    #print imgarr
    
    mincosts=[]
    paths={}
    start = time.time()
    for i in range(width):
        mincosts.append(getMinCost(height-1, i, imgarr, path, cost))
        #print path[(39 ,i)]
        paths[i]=sorted(set(path[(height-1 ,i)]))
    
    minidx = mincosts.index(min(mincosts))
    print paths[minidx]
    print mincosts[minidx]
    print time.time() - start

imgarr=np.random.randint(1,1000,size=(40,10))
getMinPath(imgarr)
