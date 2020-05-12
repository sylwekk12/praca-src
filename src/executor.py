import cv2
import time
import numpy as np
from stopwatch import Stopwatch
import threading

class TestManager:
    execId = 0
    def __init__(self, inputReader, algorithm, windowName=None):
        self.input = inputReader
        self.algorithm = algorithm
        self.stopwatch = Stopwatch()
        if windowName:
            self.windowName = windowName
        else:
            self.windowName = "executor:"+str(TestManager.execId)
        self.framesToBreak = None
        TestManager.execId += 1

    def setBreakOutFrameNumber(self, num):
        self.framesToBreak = num

    #expect method function to execute with given parameters-list
    def run(self, calculateFnc, argListForFnc):
        while (self.input.isFrameAvaliable() and ord("q") != cv2.waitKey(1)):
            self.stopwatch.start()
            res = calculateFnc(self.input.getFrame(), *argListForFnc)
            self.stopwatch.stop()
            print(f"stopwatch result: {self.stopwatch.hadleResult()}")
            self.stopwatch.reset()

            cv2.imshow(self.windowName, res)

            if(self.framesToBreak is not None and self.input.getcountedFrames() > self.framesToBreak):
                cv2.waitKey(0)
