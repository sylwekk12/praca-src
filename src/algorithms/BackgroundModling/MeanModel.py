import cv2
import numpy as np


# to slow, deprecated
# def WhiteBalancer(frame):
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
#     avgA = np.average(frame[:, :, 1])
#     avgB = np.average(frame[:, :, 2])
#
#     for x in range(frame.shape[0]):
#         for y in range(frame.shape[1]):
#             # https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html
#             L, a, b = frame[x, y, :]
#             L *= 100 / 255.0
#             frame[x, y, 1] = a - ((avgA - 128) * (L / 100.0) * 1.1)
#             frame[x, y, 2] = b - ((avgB - 128) * (L / 100.0) * 1.1)
#
#     frame = cv2.cvtColor(frame, cv2.COLOR_LAB2BGR)
#     return frame


def disableChannelV(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame[:, :, 2] = 255
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    return frame

# deprecated: too slow
class backgroundModelMeanWithContainer:
    def __init__(self, frameContainer, noShadows=False):
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
        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame.astype(dtype=np.float32), backgroundModel), threshold,
                                              255,
                                              cv2.THRESH_BINARY)
        return cv2.convertScaleAbs(differenceFrame)

    def _prepareModel(self):
        self.modelFrame = np.ndarray(shape=self.frameContainer[0].shape, dtype=np.float32)  # init Zero matrix
        for i in range(self.containerCapacity):
            self.modelFrame += self.frameContainer[i]
        self.modelFrame /= self.containerCapacity
        return self.modelFrame


class backgroundModelMeanWithContainer:
    def __init__(self, frameContainer, noShadows=False):
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

        self.modelFrame = np.ndarray(shape=self.frameContainer[0].shape, dtype=np.uint32)
        for i in range(self.containerCapacity):
            self.modelFrame += self.frameContainer[i]


    def calculate(self, frame, threshold=20):

        if self.noShadows:
            frame = disableChannelV(frame)
        # update model
        self.modelFrame = self.modelFrame - self.frameContainer[0]
        self.modelFrame = self.modelFrame + frame
        del self.frameContainer[0]
        self.frameContainer.append(frame)

        # diff
        backgroundModel = (self.modelFrame/self.containerCapacity).astype(dtype=np.uint8)

        diff = cv2.absdiff(frame, backgroundModel)
        isOk, differenceFrame = cv2.threshold(diff, threshold,
                                              255,
                                              cv2.THRESH_BINARY)
        return cv2.convertScaleAbs(differenceFrame)



# @frameWeight - frame Weight when is beeing added to background model
class backgroundModelMeanAccelerated:
    def __init__(self, initFrame,
                 frameWeight=0.01,
                 noShadows=False):  # wniosek: im wolniejszy obiekt chcemy wykryć tym niższy współczynnik należy dobrać
        self.noShadows = noShadows
        self.modelFrame = initFrame.astype(dtype=np.float32)
        if self.noShadows:
            self.modelFrame = disableChannelV(self.modelFrame).astype(dtype=np.float32)
        self.frameWeight = np.float32(frameWeight)

    def calculate(self, frame, threshold=20):
        if self.noShadows:
            frame = disableChannelV(frame)

        isOk, differenceFrame = cv2.threshold(cv2.absdiff(frame.astype(dtype=np.float32), self.modelFrame), threshold,
                                              255,
                                              cv2.THRESH_BINARY)
        self.modelFrame = self._prepareModel(frame)

        differenceFrame = cv2.convertScaleAbs(differenceFrame)
        differenceFrame = cv2.medianBlur(differenceFrame, 7)

        return cv2.convertScaleAbs(differenceFrame)

    def _prepareModel(self, newFrame):
        self.modelFrame = self.modelFrame * (1 - self.frameWeight) + newFrame * self.frameWeight
        return self.modelFrame
