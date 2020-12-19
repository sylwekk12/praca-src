from algorithms.SimpleDifference import substracts
from algorithms.BackgroundModling import backgroundModeling
from utils.colorHelper import colorHelper
from algorithms.Trackers import colorTracker
from utils.executor import TestManager
from utils.reader import VideoReader
import cv2

videoPath = "../data/simpleStreet.mp4"
maskPath = None #"../data/testVideo1/m.png"


BlueSelectorTest = colorHelper.ColorRangeSelector(*blueDownLimit,*blueUpLimit) #150 with blur or 120 normal
#RedSelectorTest = colorHelper.ColorRangeSelector(*([0,200,200]),*([20,255,255]))
GreenSelectorTest = colorHelper.ColorRangeSelector(*greenDownLimit,*greenUpLimit)


########################################################################################################################
###init Input video streams
#camera1 = VideoReader(videoPath, frameToSkip=2)
#camera2 = VideoReader(videoPath, frameToSkip=0)
# camera3 = VideoReader(videoPath, frameToSkip=1)
camera = VideoReader(videoPath,frameToSkip=0)
#myReadObject.setMask(maskPath) //if vido need special mask

########################################################################################################################
###Init algorithms
#     #1 Simply sybstr
# initFame = camera1.getFrame()
# algorithmSubstr1 = substracts.Substractor(initFame)
#
#     #2 Substr with n containter
#initFramesContainer1 = camera2.getFramesContainer(10)
#algorithmSubstrBuffer2 = substracts.SubstractorWithBufferDampingEuler(initFramesContainer1)
#
#     #3
# initFramesContainer2 = camera3.getFramesContainer(5)
# algorithmSubstrBuffer3 = substracts.SubstractorWithBufferDampingLinGeom(initFramesContainer2, 1)
#     #4
initFrame = camera.getFrame()
algorithm = backgroundModeling.backgroundModelMeanAccelerated(initFrame)
#     #5 Color Selector
# initFame = camera.getFrame()
# colorSelectorAglorithm = colorTracker.ColorTracker2(initFame, BlueSelectorTest)

########################################################################################################################
# ###start Executors Section
#1
# manTest1 = TestManager(camera1, algorithmSubstr1, ([20]))
# manTest1.run()
#2
#manTest2 = TestManager(camera2, algorithmSubstrBuffer2, ([30]))
#manTest2.run()
#3
# manTest3 = TestManager(camera3, algorithmSubstrBuffer3, ([40]))
# manTest3.run()
#4
manTest4 = TestManager(camera, algorithm, ([50]))
manTest4.maskBasedDisplay()
#5
# manTest4 = TestManager(camera, colorSelectorAglorithm.calculate, ([]))
# manTest4.run()