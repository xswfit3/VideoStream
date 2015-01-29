import cv2
import threading
from cv2 import *
import os
i = -1
def showImg():
    dirPath = "/home/VideoStream/ImgsOut/"
    files = os.listdir(dirPath)
    if len(files) > 0:
        files.sort(key=lambda x:int(x[:-4]))
        print files[-1]
        imgPath = dirPath + files[-1]
        imgMat = cv2.imread(imgPath)
        cv2.imshow("result",imgMat)
        waitKey(1)
    t = threading.Timer(2, showImg)
    t.start()#Notice: use global variable!
t = threading.Timer(0, showImg)
t.start()

