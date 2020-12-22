import cv2
import time
import numpy as np
from utils.stopwatch import Stopwatch
import threading


class TestManager:
    execId = 0

    def __init__(self, inputReader, algorithm, argsForCalculate, windowName=None):
        self.input = inputReader
        self.algorithm = algorithm
        self.stopwatch = Stopwatch()
        self.argsForCalculate = argsForCalculate
        if windowName:
            self.windowName = windowName
        else:
            self.windowName = "executor:" + str(TestManager.execId)
        self.framesToBreak = None
        TestManager.execId += 1

    def setBreakOutFrameNumber(self, num):
        self.framesToBreak = num

    # expect method function to execute with given parameters-list
    def simplyRun(self):
        while self.input.isFrameAvaliable():

            key = cv2.waitKey(10)
            if key is ord("w"):
                cv2.waitKey(-1)
            if key is ord("q"):
                break

            self.stopwatch.start()
            actualFrame = self.input.getFrame()
            res = self.algorithm.calculate(actualFrame, *self.argsForCalculate)
            self.stopwatch.stop()
            print(f"stopwatch result: {self.stopwatch.hadleResult()}")
            self.stopwatch.reset()

            cv2.imshow(self.windowName, res)

            if self.framesToBreak is not None and self.input.getcountedFrames() > self.framesToBreak:
                cv2.waitKey(0)

    def maskBasedDisplay(self):
        while self.input.isFrameAvaliable():

            key = cv2.waitKey(10)
            if key is ord("w"):
                cv2.waitKey(-1)
            if key is ord("q"):
                break

            self.stopwatch.start()
            actualFrame = self.input.getFrame()
            res = self.algorithm.calculate(actualFrame, *self.argsForCalculate)
            self.stopwatch.stop()
            print(f"stopwatch result: {self.stopwatch.hadleResult()}")
            self.stopwatch.reset()

            self._presentImgWithMask(actualFrame, res)
            #cv2.imshow(self.windowName, res)

            if self.framesToBreak is not None and self.input.getcountedFrames() > self.framesToBreak:
                cv2.waitKey(0)

    def _presentImgWithMask(self, frame, mask):
        copyOfFrame = frame.copy()

        if len(mask.shape) > 2:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            if contour.size < 400:
                continue

            (a, b, ha, hb) = cv2.boundingRect(contour)
            cv2.rectangle(copyOfFrame, (a, b), (a+ha, b+hb), (255,0,0))


        #cv2.drawContours(copyOfFrame, conturs, -1, 126, 2)

        cv2.imshow(self.windowName, copyOfFrame)
