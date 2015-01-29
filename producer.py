#!/usr/bin/env python
#coding:utf-8
'''
Created on 2015年1月5日
@author: xunw
'''
import cv2
from cv2 import *
import time
import sys
import os
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
def peopleDetect(img):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
      
    draw_detections(img, found, 3)
    #print '%d (%d) found' % (len(found_filtered), len(found))
    if len(found) > 0 :
        return found[0]
    return found
    #return img
def peopleDetect2(img):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)  
    draw_detections(img, found, 3)
    print found,w
    return img
        
def testImg():
    imgPath = "/home/xunw/x2/pyWs/people.jpg" 
    imgPaths = []
    imgPaths.append(imgPath)
    imgPaths = imgPaths* 10 
    try:
        img = cv2.imread(imgPath)
    except:
        print 'loading error'   
    imgDetect = peopleDetect2(img)
    imwrite("test.jpg",imgDetect);
    imshow("detected",imgDetect)
    waitKey(0)
def testVideo():
    vc = VideoCapture('/home/xunw/x2/pyWs/track.avi')
    sucess,frame = vc.read()
    seq = 0;

    while seq < 5 :
        imshow("img",frame)
        imgOutPath = "/home/xunw/x2/pyWs/imgsIn/" + str(seq) + ".jpg" 
        imwrite(imgOutPath,frame)
        seq += 1 
        sucess,frame = vc.read()
        waitKey(0)
    return
def produceImgs(videoPath):
    vc = VideoCapture(videoPath)
    txtSeq = 0
    lineSeq = 0
    num = 1000
    imgsDir = "./Imgs"
    txtsDir = "./Txts"
    if os.path.exists(txtsDir):
        txtList = os.listdir(txtsDir)
        for t in txtList:
            os.remove(txtsDir + '/'+ t)  #清空文件夹
    else:
        print "create Imgs dir and Txts dir  in current path "
        exit(-1)
    txtPath = txtsDir+ '/'+ str(txtSeq) + ".txt"
    print txtPath
    sucess,frame = vc.read()
    print sucess
    fileOut = open(txtPath,'w')
    while sucess and lineSeq < 1000:
        imshow("img",frame)
        if lineSeq !=0 and lineSeq % num == 0 :
            fileOut.close() 
            print lineSeq #evry 10 line create a txt
            txtSeq += 1
            txtPath = txtsDir+ '/' + str(txtSeq) + ".txt"
            fileOut = open(txtPath,'w')
        #imgOutPath = imgsDir+ '/' + str(lineSeq) + ".jpg" 
        imgOutPath = '/home/VideoStream/Imgs/' + str(lineSeq) + '.jpg'
        imwrite(imgOutPath,frame)
        fileOut.write(imgOutPath +"\n")
        lineSeq += 1 
        sucess,frame = vc.read()
        waitKey(100)
        print sucess
    return
if __name__ =="__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: producer.py "\
                             "track.avi"
        exit(-1)
    videoPath = sys.argv[1]
    produceImgs(videoPath)
    #testImg()
     
