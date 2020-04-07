import cv2
import numpy as np


class backgroundModelMean:
    def __init__(self, frameContainer):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")

    def calculate(self, frame, treshold=20):
        backgroundModel = self._prepareModel()
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        isOk, diffrenceFrame = cv2.threshold(cv2.absdiff(frame*1.0, backgroundModel), treshold, 255,cv2.THRESH_BINARY)
        return cv2.convertScaleAbs(diffrenceFrame)

    def _prepareModel(self):
        self.modelFrame = self.frameContainer[0] * 0.0
        for i in range(self.containerCapacity):
            self.modelFrame += self.frameContainer[i]
        self.modelFrame /= self.containerCapacity + 1.0
        return self.modelFrame
