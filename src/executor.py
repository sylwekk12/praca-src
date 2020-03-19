import cv2
import numpy as np
from stopwatche import Stopwatch

class TestManager:
    def __init__(self, inputReader, algorithm):
        self.input = inputReader
        self.algorithm = algorithm
        self.stopwatch = Stopwatch()
    def run(self, calculateFnc, argListForFnc):
        while (self.input.isFrameAvaliable() and ord("q") != cv2.waitKey(1)):
            res = calculateFnc(self.input.getFrame(), *argListForFnc)
            cv2.imshow("", res)
