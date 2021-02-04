import cv2
import numpy as np


# Substractor works correctly with 8 bits depth

class Substractor:
    def __init__(self, frame):
        self.frameStored = frame
        if frame.dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")

    def calculate(self, frame, threshold):
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameStored), threshold, 255, cv2.THRESH_BINARY)
        self.frameStored = frame
        return cv2.convertScaleAbs(differenceFrame)


class SubstractorWithBuffer:
    def __init__(self, frameContainer):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")

    def calculate(self, frame, threshold):
        resultFrame = np.ndarray(shape=frame.shape, dtype=np.float32)  # init Zero matrix
        for frameI in self.frameContainer:
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, frameI), threshold, 255, cv2.THRESH_BINARY)
            resultFrame += differenceFrame / self.containerCapacity
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)


class SubstractorWithBufferEuler:
    def __init__(self, frameContainer):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")

    def calculate(self, frame, threshold):
        resultFrame = np.ndarray(shape=frame.shape, dtype=np.float32)  # init Zero matrix
        for i in range(self.containerCapacity, 0, -1):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[-i]), threshold, 255,
                                                  cv2.THRESH_BINARY)
            resultFrame += differenceFrame * np.exp(-i + 1)
        scalar = (self.containerCapacity * ((1 - 1 / (np.exp(self.containerCapacity))) / (1 - 1 / np.exp(1))))
        resultFrame /= scalar / 10
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)


class SubstractorWithBufferArith:
    def __init__(self, frameContainer, a1=1, r=2): #
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception(f"Unsupported bit depth: {frameContainer[0].dtype.itemsize * 8}")
        self.a1 = a1
        self.r = r

    def calculate(self, frame, threshold):
        resultFrame = np.ndarray(shape=frame.shape, dtype=np.float32)  # init Zero matrix
        for i in range(self.containerCapacity):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[i]), threshold, 255,
                                                  cv2.THRESH_BINARY)
            scaling = self.r * (i - 1 + 1) + self.a1
            resultFrame = cv2.add(resultFrame, (cv2.multiply(differenceFrame.astype(dtype=np.float32), scaling)))
        max = self.r * (self.containerCapacity - 1) + self.a1  # max value
        Sa_n = np.float32((self.containerCapacity * (max + self.a1) / 2))
        resultFrame /= Sa_n
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)


class SubstractorWithBufferLinGeom:
    def __init__(self, frameContainer, a=1):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception(f"Unsupported bit depth: {frameContainer[0].dtype.itemsize * 8}")
        self.a = a

    def calculate(self, frame, threshold):
        resultFrame = np.ndarray(shape=frame.shape, dtype=np.float32) # init Zero matrix
        for i in range(self.containerCapacity):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[i]), threshold, 255,
                                                  cv2.THRESH_BINARY)
            scaling = np.float32(self.a ** i)
            resultFrame += (differenceFrame * scaling)
        if self.a == 1:
            Sa_n = 1.0
        else:
            Sa_n = np.float32((1 - self.a ** self.containerCapacity) / (1 - self.a))
        resultFrame /= Sa_n
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)
