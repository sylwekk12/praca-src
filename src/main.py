from reader import VideoReader
from algorithms.SimpleDifference import substracts
from algorithms.BackgroundModling import backgroundModeling
from executor import TestManager
import cv2

videoPath = "../data/hard.mp4"
maskPath = None #"../data/testVideo1/m.png"

########################################################################################################################
###init Input video streams
# camera1 = VideoReader(videoPath, frameToSkip=10)
# camera2 = VideoReader(videoPath, frameToSkip=10)
# camera3 = VideoReader(videoPath, frameToSkip=1)
camera = VideoReader(videoPath,frameToSkip=1)
#myReadObject.setMask(maskPath) //if vido need special mask

########################################################################################################################
###Init algorithms
#     #1 Simply sybstr
# initFame = camera1.getFrame()
# algorithmSubstr1 = substracts.Substractor(initFame)
#
#     #2 Substr with n containter
# initFramesContainer1 = camera2.getFramesContainer(10)
# algorithmSubstrBuffer2 = substracts.SubstractorWithBufferDampingEuler(initFramesContainer1)
#
#     #3
# initFramesContainer2 = camera3.getFramesContainer(5)
# algorithmSubstrBuffer3 = substracts.SubstractorWithBufferDampingLinGeom(initFramesContainer2, 1)
#     #4
initFrame = camera.getFrame()
algorithm = backgroundModeling.backgroundModelMeanAccelerated(initFrame)
########################################################################################################################
# ###start Executors Section
#
# manTest1 = TestManager(camera1, algorithmSubstr1)
# manTest1.run(algorithmSubstr1.calculate, ([20]))
#
# manTest2 = TestManager(camera2, algorithmSubstrBuffer2)
# manTest2.run(algorithmSubstrBuffer2.calculate, ([30]))
#
# manTest3 = TestManager(camera3, algorithmSubstrBuffer3)
# manTest3.run(algorithmSubstrBuffer3.calculate, ([40]))
#
manTest4 = TestManager(camera, algorithm)
manTest4.run(algorithm.calculate, ([50]))