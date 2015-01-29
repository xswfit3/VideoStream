#coding:utf-8
'''
Created on 2014年9月25日

@author: xunw
'''
#!/usr/bin/env python

#!/usr/bin/env python

import numpy as np
import cv2
from cv2 import *
from pyspark import SparkContext, SparkConf
import os
import myUtil
import sys
help_message = '''
USAGE: peopledetect.py <image_names> ...

Press any key to continue, ESC to stop.
'''
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
    
    draw_detections(x[1], found)
    #print '%d (%d) found' % (len(found_filtered), len(found))
    return x[0],x[1]
def Read(x):
    out = x.replace("Imgs","ImgsOut")
    return out,imread(x)   #(outImgPath ,Mat) 

def Encode(x):
    return x[0].encode('utf-8'),x[1]
def Write(x): 
    imwrite(x[0],x[1])
def testMap(imgPaths):
    sparkConf = SparkConf()
   # sparkConf.setExecutorEnv(key=None, value=None, pairs=None)
    sc = SparkContext("spark://master:7077","pyStream")
    #imgPaths = 'file:///home/VideoStream/Txts2/100.txt'
    Index = imgPaths.find("Txts")
    imgOutDir =imgPaths[:Index] + "ImgsOut" 
    if not os.path.exists(imgOutDir):
        os.makedirs(imgOutDir)
    else:
        myUtil.delete_all_file(imgOutDir)
        os.makedirs(imgOutDir)
        
    print "creste out dir : ",imgOutDir
    imgPathRdd = sc.textFile(imgPaths,8)
    #imgRdd = imgPathRdd.map(lambda x :Read(x))
    imgList = imgPathRdd.collect()
    print imgList
    imgPathList = map(Read,imgList)
    imgRdd = sc.parallelize(imgPathList)
    detectedRddu = imgRdd.map(lambda x : peopleDetect(x))
    detectedRdd =detectedRddu.map(lambda x:Encode(x))
    detectedRdd.map(lambda x:Write(x))
        #detectedRdd.saveAsTextFile('/home/xunw/x2/pyWs/imgDetected')
    pRdd =  detectedRdd.collect()
    #print pRdd
    map(lambda x:Write(x),pRdd)

if __name__ =="__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: peepleDetect.py "\
                             "file:///home/VideoStream/Txts2/100.txt"
        exit(-1)
    imgPaths = sys.argv[1]
    testMap(imgPaths)
