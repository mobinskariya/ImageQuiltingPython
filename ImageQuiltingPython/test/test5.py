import cv2 as cv
import numpy as np
import random as ran
import datetime

#this program depicts the use of opencv 

#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images

def getMinCost(i,j,error):
    minimum = 0;
    path[(i,j)] = [(i,j)] + path[(i,j)]
    cost_jp1=0
    cost_j=0
    cost_jm1=0
    list1 = path.get((i,j))
    if i > 0:
        if j < len(error[0])-1 and j > 0:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1,error)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,error)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1,error)
            minimum = min(cost_jm1, cost_j, cost_jp1)
            if minimum == cost_jm1:
                list2 = path.get((i-1,j-1))
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == 0:
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,error)
            cost_jp1 = cost[(i-1,j+1)] if cost[(i-1,j+1)] > 0 else getMinCost(i-1,j+1,error)
            minimum = min(cost_j, cost_jp1)
            if minimum == cost_jp1:
                list2 = path.get((i-1,j+1))
            else:
                list2 = path.get((i-1,j))
        elif j == len(error[0])-1:
            cost_jm1 = cost[(i-1,j-1)] if cost[(i-1,j-1)] > 0 else getMinCost(i-1,j-1,error)
            cost_j = cost[(i-1,j)] if cost[(i-1,j)] > 0 else getMinCost(i-1,j,error)
            minimum = min(cost_jm1, cost_j)
            if minimum == cost_jm1:
                list2 = path.get((i-1,j-1))
            else:
                list2 = path.get((i-1,j))
        list1 += list2
        path[(i,j)] = list1
        cost[(i,j)] = error[i,j] + minimum
        return error[i,j] + minimum
    else:
        path[(i,j)] = [(i,j)] + path[(i,j)]
        cost[(i,j)] = error[i,j]
        return error[i,j]



def minpath(imgarr):
    v=np.empty((overlap_size,sample_size), dtype=np.float64)
    
    return imgarr

#this method is used to convert color to greyscale
def rgb2gray(rgb):
    return np.dot(rgb[...,:4], [0.299, 0.587, 0.144, 0])

def createImageList(imglist):
    for i in range(len(im)-sample_size):
        for j in range(len(im[0])-sample_size):
            imglist.append(im[i:i+sample_size, j:j+sample_size])
            #print i,i+sample_size,j,j+sample_size,im[i:i+sample_size, j:j+sample_size].shape
    #print 'final'
    #print i,j
    #print im.shape
    #print len(imglist)

#this method creates a random image of sample size from the given sample image
def createRandImage():
    r=ran.randint(0,len(imglist) - 1)
    return imglist[r]

#this method computes the SSD between the 2 images for the vertical overlapping region
def computeVerticalSSD(pre_img, randimg, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:len(randimg), 0:overlap_size], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    return ssd2

#this method computes the SSD between the 2 images for the horizontal overlapping region
def computeHorizontalSSD(top_img, randimg, overlap_size):
    overlap1 = np.array(top_img[len(top_img)-overlap_size:len(top_img), 0:len(top_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:overlap_size, 0:len(top_img[0])], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    return ssd2

#this method computes the SSD between the 2 images for the vertical & horizontal overlapping region
def computeSSD(pre_img, top_img, randimg, overlap_size):
    return computeVerticalSSD(pre_img, randimg, overlap_size) + computeHorizontalSSD(top_img, randimg, overlap_size)

#this method returns an image from random list which has the minimum ssd error with the image provided
def getminSSDImg(pre_img, top_img):
    minSSDImg = []
    global imglist
    minSSD = 0
    minidx = 0
    for i in range(len(imglist)):
        if i==0:
            minSSD = computeSSD(pre_img, top_img, imglist[i],overlap_size)
            minSSDImg=imglist[i]
            minidx = i
        else:
            if not (np.array_equal(pre_img,imglist[i]) or np.array_equal(top_img,imglist[i])):
                ssd = computeSSD(pre_img, top_img, imglist[i],overlap_size)
                #print ssd,
                if minSSD > ssd:
                    minSSD = ssd
                    minSSDImg = imglist[i]
                    minidx = i;
    imglist=np.delete(imglist,minidx,0)
    return minSSDImg

def getMin2(v1, v2):
    if v1 < v2:
        return v1
    else:
        return v2

def getMin3(v1, v2, v3):
    if v1 < v2:
        if v1 < v3:
            return v1
        else:
            return v3
    else:
        if v2 < v3:
            return v2
        else:
            return v3

def findVertError(error):
    for i in range(sample_size):
        for j in range(overlap_size):
            path[(i,j)]=[]
            cost[(i,j)]=0
    mincosts=[]
    for i in range(overlap_size):
        mincosts.append(getMinCost(39, i, error))
        paths[i]=sorted(set(path[(39,i)]))

    minidx = mincosts.index(min(mincosts))
    #print paths[minidx]

#this method computes the minimum error boundary
def compVertMinErrBoun(pre_img, cur_img, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(cur_img[0:len(cur_img), 0:overlap_size], dtype=np.float64)
    error = abs(rgb2gray(overlap1)**2-rgb2gray(overlap2)**2)**0.5
    findVertError(error)
    #print E
im=cv.imread('image.png',-1)
#print im.shape

path={}
cost={}

mincosts=[]
paths={}

x_size=500
y_size=500

sample_size=40
overlap_size=10

l_img=np.zeros((x_size,y_size,4))

#randlist=[]
imglist=[]
createImageList(imglist)
for i in range(len(imglist)):
    print i,sum(sum(imglist[i]))
#createRandImageList(randlist)
cur_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
pre_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
top_img=np.empty((sample_size,sample_size,4), dtype=np.float64)


for i in range(x_size/sample_size):
    for j in range(y_size/sample_size):
        if j == 0:
            pre_img=createRandImage()
        else:
            if i == 0:
                if j == 1:
                    pre_img=l_img[(i*sample_size):(i*sample_size+sample_size),((j-1)*sample_size):((j-1)*sample_size+sample_size)]
                else :
                    pre_img=l_img[(i*sample_size):(i*sample_size+sample_size),((j-1)*sample_size)-overlap_size:((j-1)*sample_size+sample_size)-overlap_size]
            else:
                if j == 1:
                    pre_img=l_img[(i*sample_size)-overlap_size:(i*sample_size+sample_size)-overlap_size,((j-1)*sample_size):((j-1)*sample_size+sample_size)]
                else:
                    pre_img=l_img[(i*sample_size)-overlap_size:(i*sample_size+sample_size)-overlap_size,((j-1)*sample_size)-overlap_size:((j-1)*sample_size+sample_size)-overlap_size]
            
        if i == 0:
            top_img=createRandImage()
        else:
            if j == 0:
                if i == 1:
                    top_img=l_img[((i-1)*sample_size):(i*sample_size+sample_size),(j*sample_size):(j*sample_size+sample_size)]
                else:
                    top_img=l_img[((i-1)*sample_size)-overlap_size:(i*sample_size+sample_size)-overlap_size,(j*sample_size):(j*sample_size+sample_size)]
            else:
                if i == 1:
                    top_img=l_img[((i-1)*sample_size):(i*sample_size+sample_size),(j*sample_size)-overlap_size:(j*sample_size+sample_size)-overlap_size]
                else:
                    top_img=l_img[((i-1)*sample_size)-overlap_size:(i*sample_size+sample_size)-overlap_size,(j*sample_size)-overlap_size:(j*sample_size+sample_size)-overlap_size]
        print pre_img.shape
        print sum(sum(pre_img))
        #cur_img=getminSSDImg(createRandImage(), createRandImage())
        cur_img=getminSSDImg(pre_img, top_img)
        #write the code for minimum error boundary here
        print "value:",i,j
        compVertMinErrBoun(pre_img,cur_img,overlap_size)
        
        x1 = (i*sample_size)-overlap_size
        x2 = ((i+1)*sample_size)-overlap_size
        y1 = (j*sample_size)-overlap_size
        y2 = ((j+1)*sample_size)-overlap_size
        
        if i == 0:
            x1 = (i*sample_size)
            x2 = ((i+1)*sample_size)
        if j ==0 :
            y1 = (j*sample_size)
            y2 = ((j+1)*sample_size)
        l_img[x1:x2,y1:y2]=cur_img
        #mat = np.array(l_img)
        #cv.imwrite('test'+str(i)+':'+str(j)+'.png',mat)


mat = np.array(l_img)
cv.imwrite('testimg.png',mat)

#code to find the minimun SSD from the list of random images
#for i in range(len(randlist)):
#    mat = np.array(randlist[i])
#    filename = 'test'+str(i)+'.png'
#    cv.imwrite(filename, mat) # write an image
