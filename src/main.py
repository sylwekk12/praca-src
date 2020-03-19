from reader import VideoReader
from algorithms.substracts import Substractor
from executor import TestManager
import cv2

videoPath = "../data/testVideo1/v1.avi"
maskPath = "../data/testVideo1/m.png"

##init Input video stream
myReadObject = VideoReader(0)
myReadObject.setMask(maskPath)

#Init algorithm
frameStart = myReadObject.getFrame()
s1 = Substractor(frameStart)

#start Executor
manTest = TestManager(myReadObject,s1)
manTest.run(s1.calculateWithBuffer, ([100, 8]))

# while(myReadObject.isFrameAvaliable() and ord("q") != cv2.waitKey(1)):
#
#    res = s1.calculate(myReadObject.getFrame())
#    #myReadObject.skipFrame(1)
#    cv2.imshow("",res)