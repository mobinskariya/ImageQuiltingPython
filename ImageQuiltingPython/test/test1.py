import cv2 as cv
import numpy as np
import random as ran

#this program implements image quilting except the minimum error boundary

#objectv is to create a larger bgr image from small bgr tile by placing it pixel by pixel. this program finds the next image having
#minssd from a list of random images

#this method is used to convert color to greyscale
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

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
    randx = ran.randint(0,len(im)-sample_size)
    randy = ran.randint(0,len(im[0])-sample_size)
    img=im[randy:randy+sample_size, randx:randx+sample_size]
    #below while is used because the height & width is not consistent expected is sample_size
    while(len(img) & len(img[0]) != sample_size):
        randx = ran.randint(0,len(im)-sample_size)
        randy = ran.randint(0,len(im[0])-sample_size)
        img=im[randy:randy+sample_size, randx:randx+sample_size]
    return img

#this method creates a list containing 500 random images
def createRandImageList(randlist):
    for i in range(500):
        randImg=createRandImage()
        randlist.append(randImg)
    return randlist

#this method computes the SSD between the 2 images for the vertical overlapping region
def computeVerticalSSD(pre_img, randimg, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:len(randimg), 0:overlap_size], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    return ssd

#this method computes the SSD between the 2 images for the horizontal overlapping region
def computeHorizontalSSD(top_img, randimg, overlap_size):
    overlap1 = np.array(top_img[len(top_img)-overlap_size:len(top_img), 0:len(top_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:overlap_size, 0:len(top_img[0])], dtype=np.float64)
    ssd = np.sum((overlap1-overlap2)**2)
    return ssd

#this method computes the SSD between the 2 images for the vertical overlapping region
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
                    #print 'ha ha ha'
                    #print i
                    minidx = i;
    imglist=np.delete(imglist,minidx,0)
    #print
    #print 'minSSD'
    #print len(imglist)
    #print minidx
    #print minSSD
    #print minSSDImg
    return minSSDImg

#this method computes the minimum error boundary
def compMinErrBoun(img, randimg, overlap_size):
    overlap1 = np.array(img[0:len(img[0]), len(img)-overlap_size:len(img)], dtype=np.float64)
    overlap2 = np.array(randimg[0:len(randimg[0]), 0:overlap_size], dtype=np.float64)
    error=np.zeros((len(img[0]),overlap_size), dtype=np.float64)
    #print error.shape
    #print overlap_size
    #print len(overlap1)
    for i in range(len(overlap1)):
        for j in range(overlap_size):
            error[i,j]=overlap1[i,j]+overlap2[i,j]
im=cv.imread('image.png',0)

x_size=500
y_size=500

sample_size=40
overlap_size=10

l_img=np.zeros((x_size,y_size))

randlist=[]
imglist=[]
createImageList(imglist)
createRandImageList(randlist)
cur_img=np.empty((sample_size), dtype=np.float64)
pre_img=np.empty((sample_size), dtype=np.float64)
top_img=np.empty((sample_size), dtype=np.float64)


for i in range(x_size/sample_size):
    for j in range(y_size/sample_size):
        if j == 0:
            pre_img=createRandImage()
        else:
            #pre_img=cur_img
            pre_img=l_img[i*sample_size:i*sample_size+sample_size,(j-1)*sample_size:(j-1)*sample_size+sample_size]
        if i == 0:
            top_img=createRandImage()
        else:
            top_img=l_img[(i-1)*sample_size:i*sample_size+sample_size,j*sample_size:j*sample_size+sample_size]
        
        cur_img=getminSSDImg(pre_img, top_img)
        #write the code for minimum error boundary here
        #compMinErrBoun(pre_img,cur_img,overlap_size)
        

        l_img[i*sample_size:i*sample_size+sample_size,j*sample_size:j*sample_size+sample_size]=cur_img
        test_img=l_img[i*sample_size:i*sample_size+sample_size,j*sample_size:j*sample_size+sample_size]
        #mat = np.array(l_img)
        #cv.imwrite('test'+str(i)+':'+str(j)+'.png',mat)

mat = np.array(l_img)
cv.imwrite('testimg.png',mat)

#code to find the minimun SSD from the list of random images
#for i in range(len(randlist)):
#    mat = np.array(randlist[i])
#    filename = 'test'+str(i)+'.png'
#    cv.imwrite(filename, mat) # write an image