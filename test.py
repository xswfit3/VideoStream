#coding:utf-8
import cv2
from cv2 import *
def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
def peopleDetect(x):  #x  (path,Mat)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    found, w = hog.detectMultiScale(x[1], winStride=(8,8), padding=(32,32), scale=1.05)
    
    xnew = draw_detections(x[1], found)
    #print '%d (%d) found' % (len(found_filtered), len(found))
    return x[0],x[1]
def Read(x):
    return x,imread(x)   #filePath ,Mat 
def Write(x):
    imwrite(x[0],x[1])

x1 = Read("/home/xunw/x/scalaWS/VideoStream/Imgs/0.jpg")
x11 = peopleDetect(x1)
x2 = Read("/home/xunw/x/scalaWS/VideoStream/Imgs/1.jpg")
x22 = peopleDetect(x2)
a = []
a.append(x11)
a.append(x22)
map(lambda x : imwrite(x[0],x[1]),a)


