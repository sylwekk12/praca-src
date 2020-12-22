import cv2
import numpy as np

#Substractor works correctly with 8 bits depth

class Substractor:
    def __init__(self, frame):
        self.frameStored = frame
        if frame.dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")
    def calculate(self, frame, threshold):
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameStored), threshold, 255,cv2.THRESH_BINARY)
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
        resultFrame = self.frameContainer[0]*0.0 #init Zero matrix
        for frameI in self.frameContainer:
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, frameI), threshold, 255, cv2.THRESH_BINARY)
            resultFrame += differenceFrame/self.containerCapacity
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)

class SubstractorWithBufferDampingEuler:
    def __init__(self, frameContainer):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")
        resultFrame = self.frameContainer[0]*0.0 #init Zero matrix
    def calculate(self, frame, threshold):
        resultFrame = self.frameContainer[0]*0.0 #init Zero matrix
        for i in range(self.containerCapacity, 0, -1):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[-i]), threshold, 255, cv2.THRESH_BINARY)
            resultFrame += differenceFrame*np.exp(-i+1)
        scalar = (self.containerCapacity*((1-1/(np.exp(self.containerCapacity)))/(1-1/np.exp(1))))
        resultFrame /= scalar/10
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        #resultFrame = cv2.Laplacian(resultFrame, cv2.CV_64F)
        return cv2.convertScaleAbs(resultFrame)

class SubstractorWithBufferArrth:
    def __init__(self, frameContainer, a=1):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception(f"Unsupported bit depth: {frameContainer[0].dtype.itemsize*8}")
        self.a = a
    def calculate(self, frame, threshold):
        resultFrame = self.frameContainer[0]*0.0 #init Zero matrix
        for i in range(self.containerCapacity):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[i]), threshold, 255, cv2.THRESH_BINARY)
            scaling = self.a*(i-1+1)+1.0
            resultFrame += (differenceFrame*scaling)
        max = self.a*(self.containerCapacity-1)+1.0 #max value ciagu
        Sa_n = (self.containerCapacity*(max+1)/2)*1.0
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
            raise Exception(f"Unsupported bit depth: {frameContainer[0].dtype.itemsize*8}")
        self.a = a
    def calculate(self, frame, threshold):
        resultFrame = self.frameContainer[0]*0.0 #init Zero matrix
        for i in range(self.containerCapacity):
            isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, self.frameContainer[i]), threshold, 255, cv2.THRESH_BINARY)
            scaling = self.a**i*1.0
            resultFrame += (differenceFrame*scaling)
        if self.a == 1:
            Sa_n = 1.0
        else:
            Sa_n = (1-self.a**(self.containerCapacity))/(1-self.a)*1.0
        resultFrame /= Sa_n
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        return cv2.convertScaleAbs(resultFrame)

