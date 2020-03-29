from reader import VideoReader
from algorithms.SimpleDifference import substracts
from executor import TestManager
import cv2

videoPath = "../data/hard.mp4"
maskPath = None #"../data/testVideo1/m.png"

########################################################################################################################
###init Input video streams
camera1 = VideoReader(videoPath,10)
camera2 = VideoReader(videoPath,10)
#myReadObject.setMask(maskPath) //if vido need special mask

########################################################################################################################
###Init algorithms
    #1 Simply sybstr
initFame = camera1.getFrame()
algorithmSubstr1 = substracts.Substractor(initFame)

    #2 Substr with n containter
initFramesContainer1 = camera2.getFramesContainer(10)
algorithmSubstrBuffer2 = substracts.SubstractorWithBufferDampingEuler(initFramesContainer1)

########################################################################################################################
# ###start Executors Section

manTest1 = TestManager(camera1, algorithmSubstr1)
manTest1.run(algorithmSubstr1.calculate, ([20]))

manTest2 = TestManager(camera2, algorithmSubstrBuffer2)
manTest2.run(algorithmSubstrBuffer2.calculate, ([20]))