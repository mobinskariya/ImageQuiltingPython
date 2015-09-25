import cv2 as cv
import numpy as np


#this program depicts the use of opencv 
#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images
def getMinCost(i,j):
    minimum = 0;
    path[(i,j)] = [(i,j)] + path[(i,j)]
   
    list1 = path.get((i,j))
    if i > 0:
        if j < len(imgarr[0])-1 and j > 0:
            minimum = min(getMinCost(i-1,j-1), getMinCost(i-1,j), getMinCost(i-1,j+1))
            if minimum == getMinCost(i-1,j-1):
                list2 = path.get((i-1,j-1))
            if minimum == getMinCost(i-1,j+1):
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == 0:
            minimum = min(getMinCost(i-1,j), getMinCost(i-1,j+1))
            if minimum == getMinCost(i-1,j+1):
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == len(imgarr[0])-1:
            minimum = min(getMinCost(i-1,j-1), getMinCost(i-1,j))
            if minimum == getMinCost(i-1,j-1):
                list2 = path.get((i-1,j-1))
            else:
                list2 = path.get((i-1,j))
        list1 += list2
        path[(i,j)]=list1
        return imgarr[i,j] + minimum
    else:
        path[(i,j)] = [(i,j)] + path[(i,j)]
        return imgarr[i,j]

def minpath(imgarr):
    v=np.empty((sample_size,overlap_size), dtype=np.float64)
    #dist=np.empty((sample_size,overlap_size), dtype=np.float64)
    #dist.fill(float("inf"))
    imgarr=np.random.rand(sample_size,overlap_size)
    j=5
        
    for j in range(len(imgarr[0])):
        cost=0
        
        for i in range(len(imgarr)):
            lowest=float("inf")
            if i >= len(imgarr)-1:
                break
            if j > 1 and imgarr[i+1,j-1] < lowest:
                lowest = imgarr[i+1,j-1]
                index=0
            if imgarr[i+1,j] < lowest:
                lowest = imgarr[i+1,j]
                index=1
            if j < overlap_size - 1 and imgarr[i+1,j+1] < lowest:
                lowest = imgarr[i+1,j+1]
                index=2
            if index == 0:
                path.append((i+1,j-1))
                j=j-1
            elif index == 1:
                path.append((i+1,j))
            else:
                path.append((i+1,j+1))
                j=j+1
            cost += lowest
        print "cost"
        print cost
        print path   
    return imgarr

im=cv.imread('image.png',-1)


x_size=500
y_size=500

sample_size=40
overlap_size=10

path={}
cost=[]


l_img=np.zeros((x_size,y_size,4))

imgarr=np.random.randint(1,1000,size=(40,10))

for i in range(sample_size):
    for j in range(overlap_size):
        path[(i,j)]=[]

#minpath(imgarr)
print imgarr

for i in range(sample_size):
    for j in range(overlap_size):
        print i,j,"===>",path[(i,j)]

print getMinCost(39,5)

for i in range(sample_size-1):
    for j in range(overlap_size):
        print i,j,"===>",set(path[(i,j)])

mat = np.array(l_img)
cv.imwrite('testimg.png',mat)

