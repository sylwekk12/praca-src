import numpy as np
import cv2
import logging

#mask defines which bits should be deleted (set to 0)
#for 0 in mask value means that respondent Video frame pixel value is set to 0
#in other case video pixels are unchanged

class CameraConfiguration:
    def __init__(self, camera):
        self.readCameraConfiguration(camera)
    def readCameraConfiguration(self, cam):
        self.fps = cam.get(cv2.CAP_PROP_FPS)
        self.width = cam.get(cv2.CV_CAP_PROP_FRAME_WIDTH)
        self.height = cam.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)

class VideoReader:
    def __init__(self, filePath, greyScale=False,frameToSkip=0):
        self.camera = cv2.VideoCapture(filePath)
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
        self.greyScaleFlag = greyScale

    def setMask(self, maskPath):
        self.mask = cv2.imread(maskPath)
        if self.mask is None:
            logging.warning("Failed: read mask")

    def getFrame(self):
        if not self.status:
            logging.error(f"Cannot read frame")
            raise Exception("frame was not avaliable, to avoid this error check frame avability before getFrame call")
        logging.debug(f"frame readed correctly")
        retFrame = self.containedFrame
        self.skipFrame(self.frameToSkip)
        if self.isFrameAvaliable():
            self.status, self.containedFrame = self.camera.read()
        if(self.greyScaleFlag == True):
            retFrame = cv2.cvtColor(retFrame, cv2.COLOR_BGR2GRAY, dstCn=1)
        if self.mask is not None:
            return retFrame&self.mask
        else:
            return retFrame

    def greyScaleSet(self, status):
        self.greyScaleFlag = status

    def isFrameAvaliable(self):
        if self.status:
            return True
        else:
            return False

    def skipFrame(self, numberoFFramesToSkip = 1):
        counter = 0
        while counter < (numberoFFramesToSkip - 1):
            self.camera.read()
            counter+=1
        self.status, self.containedFrame = self.camera.read()

    def getFramesContainer(self, n):
        framesList = []
        for i in range(n):
            #self.status, self.containedFrame = self.camera.read()
            recivedFrame = self.getFrame()
            if self.status == False:
                raise Exception(f"Read frame container [{i}] of [{n}] failed")
            framesList.append(recivedFrame)
        return framesList