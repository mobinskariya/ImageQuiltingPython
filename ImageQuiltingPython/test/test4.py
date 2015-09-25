import cv2 as cv
import numpy as np
import random as ran
import datetime

#this program depicts the use of opencv 

#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images

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
    return imglist[ran.randint(0,len(imglist) - 1)]

#this method computes the SSD between the 2 images for the vertical overlapping region
def computeVerticalSSD(pre_img, randimg, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:len(randimg), 0:overlap_size], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)-rgb2gray(overlap2))**2)
    return ssd2

#this method computes the SSD between the 2 images for the horizontal overlapping region
def computeHorizontalSSD(top_img, randimg, overlap_size):
    overlap1 = np.array(top_img[len(top_img)-overlap_size:len(top_img), 0:len(top_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:overlap_size, 0:len(top_img[0])], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)-rgb2gray(overlap2))**2)
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

def findVertError(i,j,error):
    #print i,j
    if i == 1:
        if j == 0:
            return getMin2(error[0,j], error[0,j+1])
        elif j == overlap_size-1:
            return getMin2(error[0,j-1], error[0,j])
        else:
            return getMin3(error[0,j-1], error[0,j], error[0,j+1])
    else:
        if j == 0:
            return error[i,j] + getMin2(error[i-1,j], error[i-1,j+1])
        elif j == overlap_size-1:
            return error[i,j] + getMin2(error[i-1,j-1], error[i-1,j])
        else:
            return error[i,j] + getMin3(findVertError(i-1,j-1,error), findVertError(i-1,j,error), findVertError(i-1,j+1,error))

#this method computes the minimum error boundary
def compVertMinErrBoun(pre_img, cur_img, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(cur_img[0:len(cur_img), 0:overlap_size], dtype=np.float64)
    #print error.shape
    #print overlap_size
    #print len(overlap1)
    E = np.zeros(overlap_size)
    error = (rgb2gray(overlap1)-rgb2gray(overlap2))**2
    #for i in range(overlap_size):
        #E[i] = findVertError(sample_size-1,i,error)
    print findVertError(sample_size-1,4,error)
    #print E
im=cv.imread('image.png',-1)
print im.shape

start=datetime.datetime.now()
print start

x_size=500
y_size=500

sample_size=40
overlap_size=10

l_img=np.zeros((x_size,y_size,4))

#randlist=[]
imglist=[]
createImageList(imglist)
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
        cur_img=getminSSDImg(pre_img, top_img)
        #write the code for minimum error boundary here
        #compVertMinErrBoun(pre_img,cur_img,overlap_size)
        
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

stop=datetime.datetime.now()

delta=stop-start
print stop

print 'time taken'

print delta

mat = np.array(l_img)
cv.imwrite('testimg.png',mat)

#code to find the minimun SSD from the list of random images
#for i in range(len(randlist)):
#    mat = np.array(randlist[i])
#    filename = 'test'+str(i)+'.png'
#    cv.imwrite(filename, mat) # write an image
