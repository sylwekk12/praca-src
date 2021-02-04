import cv2
import numpy as np



def disableChannelV(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    frame[:,:,2] = 255
    frame = cv2.cvtColor(frame,cv2.COLOR_HSV2BGR)
    # cv2.imshow("",frame)
    # cv2.waitKey(1)
    return frame


class backgroundModelMedianWithContainer:
    def __init__(self, frameContainer, noShadows=True):
        self.frameContainer = frameContainer
        self.containerCapacity = len(self.frameContainer)
        self.noShadows = noShadows
        if self.containerCapacity == 0:
            raise Exception("Empty frame container")
        if frameContainer[0].dtype.itemsize != 1:
            raise Exception("Unsupported bit depth")
        if self.noShadows:
            for i in range(len(self.frameContainer)):
                self.frameContainer[i] = disableChannelV(self.frameContainer[i])

    def calculate(self, frame, threshold=20):
        backgroundModel = self._prepareModel()
        cv2.imshow("background", cv2.convertScaleAbs(backgroundModel))

        if self.noShadows:
            frame = disableChannelV(frame)
        del self.frameContainer[0]
        self.frameContainer.append(frame)
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame, backgroundModel), threshold, 255,
                                             cv2.THRESH_BINARY)
        #differenceFrame = cv2.medianBlur(differenceFrame, 3)
        # kernel = np.ones((3,3), np.uint8)
        # differenceFrame = cv2.morphologyEx(differenceFrame, cv2.MORPH_OPEN, kernel)
        return cv2.convertScaleAbs(differenceFrame)

    def _prepareModel(self):
        modelFrame = np.median(self.frameContainer, axis=0).astype(dtype=np.uint8)
        return modelFrame
