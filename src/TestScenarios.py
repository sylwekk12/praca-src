from utils.VideoReader import VideoReader
from algorithms.SimpleDifference import Substracts
from algorithms.BackgroundModling import MeanModel
from algorithms.BackgroundModling import MedianModel
from utils.ColorHelper import ColorRangeSelector
from algorithms.Trackers import ColorTracker
from utils.Executor import TestManager
import cv2
import matplotlib.pyplot as plt

blueDownLimit = ([100, 150, 10])
blueUpLimit = ([120, 255, 255])
greenDownLimit = ([40, 150, 150])
greenUpLimit = ([70, 255, 255])


###helpers
# selectors
# BlueSelectorTest = colorHelper.ColorRangeSelector(*([100,150,10]),*([120,255,255])) #150 with blur or 120 normal
# #RedSelectorTest = colorHelper.ColorRangeSelector(*([0,200,200]),*([20,255,255]))
# GreenSelectorTest = colorHelper.ColorRangeSelector(*([40,150,150]),*([70,255,255]))


# test parameters
###
# video
class testVideo:
    liveAutodetectedCamera = 0
    staticCameraSimpleStreet = "../data/Street/S2.mp4"
    ColorTrackerTest = 0  # TODO: prepare viddo


frameBreakpointSubstr = 230  # 230
frameBreakpointBackgroundModeling = 420  # 420


# default test cases
class TestScenarios_Substractors:
    def __init__(self, video, framesToSkip=5, greyscale=False):
        self.video = video
        self.greyscale = greyscale
        self.framesToSkip = framesToSkip

    def simplySubstr(self):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        initFame = camera.getFrame()
        algorithmSubstr1 = Substracts.Substractor(initFame)
        manTest1 = TestManager(camera, algorithmSubstr1, ([10]), framesToBreak=frameBreakpointSubstr)
        manTest1.maskBaseDisplay()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Simply frame difference')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def substrWithBufferGeom(self, q=9):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=True)
        initFrames = camera.getFramesContainer(4)
        algorithmSubstr = Substracts.SubstractorWithBufferLinGeom(initFrames, q)
        manTest1 = TestManager(camera, algorithmSubstr, ([20]), framesToBreak=frameBreakpointSubstr)
        manTest1.simplyRun()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Simply frame difference scaled by geometric series based 4 frames')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def substrWithBufferArith(self, a=1, r=1):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=True)
        initFrames = camera.getFramesContainer(4)
        algorithmSubstr = Substracts.SubstractorWithBufferArith(initFrames, a1=a, r=r)
        manTest1 = TestManager(camera, algorithmSubstr, ([20]), framesToBreak=frameBreakpointSubstr)
        manTest1.simplyRun()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Simply frame difference scaled by arithmetic series based 4 frames')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def substrWithBufferEuler(self):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=True)
        initFrames = camera.getFramesContainer(4)
        algorithmSubstr = Substracts.SubstractorWithBufferEuler(initFrames)
        manTest1 = TestManager(camera, algorithmSubstr, ([20]), framesToBreak=frameBreakpointSubstr)
        manTest1.simplyRun()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Simply frame difference scaled by e^x series based 4 framess')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def backgroundMeanWithBuffer(self):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        initFrames = camera.getFramesContainer(50)
        algorithmSubstr = MeanModel.backgroundModelMeanWithContainer(initFrames)
        manTest1 = TestManager(camera, algorithmSubstr, ([20]), framesToBreak=frameBreakpointBackgroundModeling)
        manTest1.maskBaseDisplay()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Mean background modeling based 50 frames')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def backgroundMeanAccelerated(self, frameWeight=0.05):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        initFrame = camera.getFrame()
        algorithmSubstr = MeanModel.backgroundModelMeanAccelerated(initFrame, frameWeight)
        manTest1 = TestManager(camera, algorithmSubstr, ([20]), framesToBreak=frameBreakpointBackgroundModeling)
        manTest1.maskBaseDisplay()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Mean background modeling based average mean')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def backgroundMedianWithBuffer(self):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        initFrames = camera.getFramesContainer(20)
        algorithmSubstr1 = MedianModel.backgroundModelMedianWithContainer(initFrames, noShadows=True)
        manTest1 = TestManager(camera, algorithmSubstr1, ([20]),
                               framesToBreak=frameBreakpointBackgroundModeling)  # framesToBreak=frameBreakpointBackgroundModeling)
        manTest1.maskBaseDisplay()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('Median background modeling based 20 frames')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()

    def backgroundMOG2(self):
        camera = VideoReader(self.video, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        MOG2 = cv2.createBackgroundSubtractorMOG2(varThreshold=20, detectShadows=False)
        manTest1 = TestManager(camera, MOG2, None, framesToBreak=frameBreakpointBackgroundModeling)
        manTest1.cvAlgo()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('OpenCV MOG2 background modeling based 20 frames')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()


# format: H min:28 H max:41 S min:114 S max:248 V min:72 V max:255
Yellow = ColorRangeSelector(*(28, 114, 72), *(41, 248, 255))


class TestScenario_Trackers:
    def __init__(self, videoPath, framesToSkip=0, greyscale=False):
        self.videoPath = videoPath
        self.greyscale = greyscale
        self.framesToSkip = framesToSkip

    def SimplyColorTracker(self, selectedColorHSV):
        camera = VideoReader(self.videoPath, frameToSkip=self.framesToSkip, greyscaleMode=self.greyscale)
        initFame = camera.getFrame()
        colorSelectorAglorithm = ColorTracker.ColorTracker(initFame, selectedColorHSV)
        manTest1 = TestManager(camera, colorSelectorAglorithm, ([]))
        manTest1.simplyRun()
        print(f"avg measurementTime: {manTest1.getAverageMeasurementTime()}")
        mes = manTest1.getStopwatchMeasurements()
        plt.hist(mes, bins='auto', alpha=0.3, rwidth=0.2)
        plt.title('SimplyColorTracker')
        plt.ylabel('Counts')
        plt.xlabel('Measured iteration time')
        plt.grid()
        plt.show()
