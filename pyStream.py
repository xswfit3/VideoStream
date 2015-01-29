#!/usr/bin/env python
#coding:utf-8

'''
Created on 2015年1月4日

@author: xunw
'''

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import os
import sys
import numpy as np
import cv2
from cv2 import *
from pyspark import SparkContext
import shutil
import myUtil
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
def Read(x):
    out = x.replace("Imgs","ImgsOut")
    return out,imread(x)   #(outImgPath ,Mat) 
def Encode(x):
    return x[0].encode('utf-8'),x[1]
def Write(x): 
    imwrite(x[0],x[1])
    
def peopleDetect(img):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
    #draw_detections(img, found, 3)
    #print '%d (%d) found' % (len(found_filtered), len(found))
    if len(found) > 0 :
        return found[0]
    #print found
    return found

def peopleDetectNew(x):  #x  (path,Mat)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    found, w = hog.detectMultiScale(x[1], winStride=(8,8), padding=(32,32), scale=1.05)
    
    draw_detections(x[1], found)
    #print '%d (%d) found' % (len(found_filtered), len(found))
    return x[0],x[1]


def createContext(txtsDir ,outputPath):
    # If you do not see this printed, that means the StreamingContext has been loaded
    # from the new checkpoint
    
    if os.path.exists(txtsDir):
        txtList = os.listdir(txtsDir)
        for t in txtList:
            os.remove(txtsDir + '/'+ t)  #清空文件夹
    else:
        print "create Imgs dir and Txts dir  in current path "
        exit(-1)
    Index = txtsDir.find("Txts")
    imgOutDir =txtsDir[:Index] + "ImgsOut" 
    if not os.path.exists(imgOutDir):
        os.makedirs(imgOutDir)
    else:
        myUtil.delete_all_file(imgOutDir)
        os.makedirs(imgOutDir)
        print "creste out dir : ",imgOutDir
    print "Creating new context"
    if os.path.exists(outputPath):
        os.remove(outputPath)
    sc = SparkContext("local[4]","PythonStreaming")
    ssc = StreamingContext(sc, 2) # 2 s

    # Create a socket stream on target ip:port and count the
    # words in input stream of \n delimited text (eg. generated by 'nc')
    dataDir = txtsDir
    lines = ssc.textFileStream(dataDir)  # every line is a img path
#     imgRdds = lines.map(lambda x :cv2.imread(x))  # (outpath,Mat)
#     detectedRdds = imgRdds.map(lambda x : peopleDetect(x))
#     def echo(time, rdd):
#         rects = "detected at time %s %s" % (time, rdd.collect())
#         print rects
#         print "Appending to " + os.path.abspath(outputPath)
#         with open(outputPath, 'a') as f:
#             f.write(rects + "\n")   

    imgRdds = lines.map(lambda x :Read(x))  # (outpath,Mat)
    detectedRdds = imgRdds.map(lambda x : peopleDetectNew(x))
    def echo(rdd):
        pyMatList  =  rdd.collect()
        print pyMatList
        map(Write,pyMatList)   
    detectedRdds.foreachRDD(echo)
    return ssc

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: pyStream.py "\
                             "txtsDir <output-file>"
        exit(-1)
  

    txtsDir, output = sys.argv[1:]
    #ssc = StreamingContext.getOrCreate(checkpoint,lambda: createContext(output))
    ssc =  createContext(txtsDir ,output)
    ssc.start()
    ssc.awaitTermination()

