import numpy as np
import cv2
import logging


class ColorModel:
    RGB = 1
    HSV = 2


# mask defines which bits should be deleted (set to 0)
# for 0 in mask value means that respondent Video frame pixel value is set to 0
# in other case video pixels are unchanged

class Camera:
    def __init__(self, cv2Camera, maskPath=None, greyscaleMode=False,
                 colorModel=ColorModel.RGB):  # TODO: extract parameters to configuration
        self.cv2Cam = cv2Camera
        self.colorModel = colorModel
        self.greyscaleMode = greyscaleMode
        if maskPath is not None:
            self.mask = cv2.imread(maskPath)
        else:
            self.mask = None
        self.framesCounter = 0

    def UpdateConfig(self, greyscale=None, colorModel=None, maskPath=None):
        if greyscale is not None:
            self.greyscaleMode = greyscale
        if colorModel is not None:
            self.colorModel = colorModel
        if maskPath is not None:
            self.mask = cv2.imread(maskPath)

    def read(self):
        isOk, frame = self.cv2Cam.read()
        if not isOk:
            return isOk, frame

        self.framesCounter += 1

        if self.colorModel == ColorModel.RGB:
            pass  # frame = cv2.cvtColor(frame, cv2._)
        if self.colorModel == ColorModel.HSV:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s ,v = cv2.split(hsv)
            v.fill(255)
            frame = cv2.cvtColor(cv2.merge([h,s,v]), cv2.COLOR_HSV2BGR)

            cv2.imshow("w",frame)
            cv2.waitKey(1)

        if self.greyscaleMode:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # , dstCn=1)
        if self.mask is not None:
            frame = frame & self.mask

        #frame = cv2.blur(frame, (5,5))
        #frame = cv2.bilateralFilter(frame, 9, 75, 75)

        return isOk, frame

    def isOpened(self):
        return self.cv2Cam.isOpened()

    # def readCameraInfo(self, cam):
    #     pass
        # self.fps = cam.get(cv2.CAP_PROP_FPS)
        # self.width = cam.get(cv2.CV_CAP_PROP_FRAME_WIDTH)
        # self.height = cam.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)


class VideoReader:
    def __init__(self, filePath, frameToSkip=0):
        cv2Cam = cv2.VideoCapture(filePath)
        self.camera = Camera(cv2Cam)
        if not self.camera.isOpened():
            logging.error(f"Cannot open file: {filePath}")
            raise Exception("Video reader cannot be init")
        logging.info(f"File open: {filePath}")
        self.status, self.containedFrame = self.camera.read()
        # print(f"frame: {bytes(self.camera.get(cv2.CAP_PROP_FOURCC))}")
        if not self.status:
            raise Exception("Failed: read init Frame")
        self.mask = None
        self.frameToSkip = frameToSkip

    # def setMask(self, maskPath):
    #     self.mask = cv2.imread(maskPath)
    #     if self.mask is None:
    #         logging.warning("Failed: read mask")

    # def greyScaleSet(self, status):
    #     self.greyScaleFlag = status
    def updateCameraConfiguration(self, greyscale=None, colorModel=None, maskPath=None):
        self.camera.UpdateConfig(greyscale=greyscale, colorModel=colorModel, maskPath=maskPath)

    def isFrameAvaliable(self):
        return self.status

    def getcountedFrames(self):
        return self.camera.framesCounter

    def skipFrame(self, numberoFFramesToSkip=1):
        counter = 0
        while counter < (numberoFFramesToSkip - 1):
            self.camera.read()
            counter += 1
        self.status, self.containedFrame = self.camera.read()

    def getFramesContainer(self, n):
        framesList = []
        for i in range(n):
            # self.status, self.containedFrame = self.camera.read()
            receivedFrame = self.getFrame()
            if not self.status:
                raise Exception(f"Read frame container [{i}] of [{n}] failed")
            framesList.append(receivedFrame)
        return framesList

    def getFrame(self):
        if not self.status:
            logging.error(f"Cannot read frame")
            raise Exception("frame was not avaliable, to avoid this error check frame avability before getFrame call")
        logging.debug(f"frame readed correctly")
        retFrame = self.containedFrame
        self.skipFrame(self.frameToSkip)
        if self.isFrameAvaliable():
            self.status, self.containedFrame = self.camera.read()
        return retFrame
