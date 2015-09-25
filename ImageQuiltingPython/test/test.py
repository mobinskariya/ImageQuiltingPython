import cv2 as cv
import numpy as np
import random as ran
from minpath import getMinPath

#this program depicts the use of opencv 

#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images

def print_grid(grid):
    for row in grid:
        for e in row:
            print '\t',sum(e),
        print

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
    #print "overlap1",overlap1.shape
    #print_grid(overlap1)
    #print "overlap2",overlap2.shape
    #print_grid(overlap2)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    ssd3 = np.sum(((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5)
    #print "vertical ssd3 ",ssd3
    return ssd3

#this method computes the SSD between the 2 images for the horizontal overlapping region
def computeHorizontalSSD(top_img, randimg, overlap_size):
    overlap1 = np.array(top_img[len(top_img)-overlap_size:len(top_img), 0:len(top_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:overlap_size, 0:len(top_img[0])], dtype=np.float64)
    #print "overlap1",top_img.shape
    #print_grid(overlap1)
    #print "overlap2",randimg.shape
    #print_grid(overlap2)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    ssd3 = np.sum(((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5)
    #print "horizontal ssd3 ",ssd3
    return ssd3

#this method computes the SSD between the 2 images for the vertical & horizontal overlapping region
def computeSSD(pre_img, top_img, randimg, overlap_size):
    #print "printing", pre_img, top_img
    if pre_img is None and top_img is None:
        #print 'both are none'
        return 0
    if pre_img is None:
        #print 'prev img is none'
        return computeHorizontalSSD(top_img, randimg, overlap_size)
    if top_img is None:
        #print 'top img is none'
        return computeVerticalSSD(pre_img, randimg, overlap_size)
    #print 'both are not none'
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
    #imglist=np.delete(imglist,minidx,0)
    #print "minSSD ",minSSD
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


#this method computes the minimum error boundary
def compVertMinErrBoun(pre_img, cur_img, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(cur_img[0:len(cur_img), 0:overlap_size], dtype=np.float64)
    error = ((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5
    
    
    path = getMinPath(error)
    print pre_img.shape, cur_img.shape
    #print path
    for i in path:
        #print i
        for k in range(i[1]):
            cur_img[i[0]][k]=overlap1[i[0]][k]
    
    #print E
    
def compHorMinErrBoun(top_img, cur_img, overlap_size):
    imgT=np.transpose(top_img, axes=(1, 0, 2))
    randimgT=np.transpose(cur_img, axes=(1, 0, 2))
    compVertMinErrBoun(imgT, randimgT, overlap_size)
    
def compMinErrBoun(pre_img,top_img,cur_img,overlap_size):
    if pre_img is not None:
        #print "pre_img is not none"
        compVertMinErrBoun(pre_img,cur_img,overlap_size)
    if top_img is not None:
        compHorMinErrBoun(top_img,cur_img,overlap_size)
    
def getPrevImg(i,j):
    if j == 0:
        #print "returning prev none"
        return None
    else:
        #print "getPrevImg",i,j
        #print_grid(l_img)
        return l_img[(i*sample_size)-(overlap_size*i):((i+1)*sample_size)-(overlap_size*i),((j-1)*sample_size)-(j-1)*overlap_size:(j*sample_size)-(j-1)*overlap_size]

def getTopImg(i,j):
    if i == 0:
        #print "returning top none"
        return None
    else:
        #print "getTopImg",i,j
        #print_grid(l_img)
        return l_img[((i-1)*sample_size)-(i-1)*overlap_size:(i*sample_size)-(i-1)*overlap_size,(j*sample_size)-(overlap_size*j):((j+1)*sample_size)-(overlap_size*j)]

im=cv.imread('image1.png',-1)
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
#for i in range(len(imglist)):
#    print i,sum(sum(imglist[i]))
#createRandImageList(randlist)
cur_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
pre_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
top_img=np.empty((sample_size,sample_size,4), dtype=np.float64)

nx=x_size/(sample_size-overlap_size)
ny=y_size/(sample_size-overlap_size)

newx=nx# + (x_size-nx*overlap_size)/sample_size
newy=ny# + (y_size-ny*overlap_size)/sample_size

#print newx
#print newy

for i in range(newx):
    for j in range(newy):
        print "value:",i,j
        pre_img = getPrevImg(i, j)
        top_img = getTopImg(i, j)
        #if pre_img is not None:
            #print "pre"
            #print_grid(pre_img)
        #if top_img is not None:
        #    print "top"
        #    print_grid(top_img)
        cur_img=getminSSDImg(pre_img, top_img)
        #print "cur"
        #print_grid(cur_img)
        #write the code for minimum error boundary here
        #if pre_img is not None:
            #print_grid(pre_img)
            #print sum(sum(pre_img))
        
        #compMinErrBoun(pre_img,top_img,cur_img,overlap_size)
        
        x1 = (i*sample_size)-(overlap_size*i)
        x2 = ((i+1)*sample_size)-(overlap_size*i)
        y1 = (j*sample_size)-(overlap_size*j)
        y2 = ((j+1)*sample_size)-(overlap_size*j)
        
        if i == 0:
            x1 = (i*sample_size)
            x2 = ((i+1)*sample_size)
        if j == 0 :
            y1 = (j*sample_size)
            y2 = ((j+1)*sample_size)
        #print i,j
        #print l_img[x1:x2,y1:y2].shape, cur_img.shape
        l_img[x1:x2,y1:y2]=cur_img
        #print_grid(l_img)
        #mat = np.array(l_img)
        #cv.imwrite('/home/mobin/Misc/img/test'+str(i)+':'+str(j)+'.png',mat)
        mat = np.array(l_img)
        cv.imwrite('testimg.png',mat)


mat = np.array(l_img)
cv.imwrite('testimg.png',mat)

#code to find the minimun SSD from the list of random images
#for i in range(len(randlist)):
#    mat = np.array(randlist[i])
#    filename = 'test'+str(i)+'.png'
#    cv.imwrite(filename, mat) # write an image
