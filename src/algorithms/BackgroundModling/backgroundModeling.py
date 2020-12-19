import cv2
import numpy as np


class backgroundModelMeanWithContainer:
    def __init__(self, frameContainer):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")

    def calculate(self, frame, threshold=20):
        backgroundModel = self._prepareModel()
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame * 1.0, backgroundModel), threshold, 255,
                                             cv2.THRESH_BINARY)
        return cv2.convertScaleAbs(differenceFrame)

    def _prepareModel(self):
        self.modelFrame = self.frameContainer[0] * 0.0
        for i in range(self.containerCapacity):
            self.modelFrame += self.frameContainer[i]
        self.modelFrame /= self.containerCapacity
        return self.modelFrame


# @frameWeight - frame Weight when is beeing added to background model
class backgroundModelMeanAccelerated:
    def __init__(self, initFrame,
                 frameWeight=0.01):  # wniosek: im wolniejszy obiekt chcemy wykryć tym niższy współczynnik należy dobrać
        self.modelFrame = initFrame * 1.0
        self.frameWeight = frameWeight

    def calculate(self, frame, threshold=20):
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame * 1.0, self.modelFrame), threshold, 255,
                                             cv2.THRESH_BINARY)
        self.modelFrame = self._prepareModel(frame)
        return cv2.convertScaleAbs(differenceFrame)

    def _prepareModel(self, newFrame):
        self.modelFrame = self.modelFrame * (1 - self.frameWeight) + newFrame * self.frameWeight
        return self.modelFrame
