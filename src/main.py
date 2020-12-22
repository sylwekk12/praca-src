from algorithms.SimpleDifference import substracts
from algorithms.BackgroundModling import backgroundModeling
from utils.colorHelper import ColorRangeSelector
from algorithms.Trackers import colorTracker
from utils.executor import TestManager
from utils.reader import VideoReader
import TestScenarios as ts
import cv2

videoPath = 0#"../data/testVideo1/v2.avi"
maskPath = None #"../data/testVideo1/m.png"

tr = ts.TestScenario_Trackers()
tr.SimplyColorTracker(ts.wieczko)


########################################################################################################################
###init Input video streams
#camera1 = VideoReader(videoPath, frameToSkip=2)
#camera2 = VideoReader(videoPath, frameToSkip=0)
# camera3 = VideoReader(videoPath, frameToSkip=1)
# camera = VideoReader(videoPath,frameToSkip=0, greyscaleMode=False)
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
# initFrame = camera.getFrame()
# algorithm = backgroundModeling.backgroundModelMeanAccelerated(initFrame)
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
# manTest4 = TestManager(camera, algorithm, ([30]))
# manTest4.maskBasedDisplay()
#5
# manTest4 = TestManager(camera, colorSelectorAglorithm.calculate, ([]))
# manTest4.run()