import cv2
import numpy as np

#Default True, can be changed if needed
DEBUG_MODE = True

class substractor:
    def __init__(self, frame, treshold):
        self.frameOld = frame
        self.treshold =
        pass
    def calculate(self, frame):
        diffrenceFrame = cv2.absdiff(frame, self.frameOld)
        self.frameOld = frame
        self.tresholdAbsoluteValue = 2 ** (8 * diffrenceFrame.dtype.itemsize) * tresholdDetectionPercent / 100
        return np.greater(diffrenceFrame, self.tresholdAbsoluteValue).any()
        pass


#params
#frame1,frame2  - frames to compare in algorithm
#mask           - optional argument useful for videos with HUD
#blur           - optional blur filter, correct values: 0,1,3,5; default: 1
# def frameDiffDetectionRGB(frame1,frame2,tresholdDetectionPercent, mask = np.array([]), blur=1):#TODO: mask=None????
#     diffrenceFrame = cv2.absdiff(frame1,frame2)
#
#     #check mask eistance by any
#     if mask.any():
#         diffrenceFrame = diffrenceFrame & mask
#
#     #median filter
#     diffrenceFrame = cv2.medianBlur(diffrenceFrame, blur)
#
#     if DEBUG_MODE:
#         cv2.imshow("",diffrenceFrame)
#         cv2.waitKey(1)
#         print("Max value in deffrence frame:"+str(np.max(diffrenceFrame)))
#
#     tresholdAbsoluteValue = 2**(8*diffrenceFrame.dtype.itemsize) * tresholdDetectionPercent / 100
#         #tresholdAbsoluteValue = maxValueOfPixel * tresholdDetectionPercent / 100
#     return np.greater(diffrenceFrame, tresholdAbsoluteValue).any()

def frameDiffDetectionRGB(frame1, frame2, tresholdDetectionPercent):
    diffrenceFrame = cv2.absdiff(frame1, frame2)

    # check mask eistance by any
    if mask.any():
        diffrenceFrame = diffrenceFrame & mask

    # median filter
    diffrenceFrame = cv2.medianBlur(diffrenceFrame, blur)

    if DEBUG_MODE:
        cv2.imshow("", diffrenceFrame)
        cv2.waitKey(1)
        print("Max value in deffrence frame:" + str(np.max(diffrenceFrame)))

    tresholdAbsoluteValue = 2 ** (8 * diffrenceFrame.dtype.itemsize) * tresholdDetectionPercent / 100
    # tresholdAbsoluteValue = maxValueOfPixel * tresholdDetectionPercent / 100
    return np.greater(diffrenceFrame, tresholdAbsoluteValue).any()

def frameDiffDetectionHSV(frame1,frame2,tresholdDetectionPercent, mask = np.array([])):
    diffrenceFrame = cv2.absdiff(frame1,frame2)

    #check mask eistance by any
    if mask.any():
        diffrenceFrame = diffrenceFrame & mask
    
    #median filter
    diffrenceFrame = cv2.medianBlur(diffrenceFrame, 5)
    

    if DEBUG_MODE:
        cv2.imshow("",diffrenceFrame)
        cv2.waitKey(1)
        print("Max value in deffrence frame:"+str(np.max(diffrenceFrame)))

    tresholdAbsoluteValue = 2**(8*diffrenceFrame.dtype.itemsize) * tresholdDetectionPercent / 100
        #tresholdAbsoluteValue = maxValueOfPixel * tresholdDetectionPercent / 100
    return np.greater(diffrenceFrame, tresholdAbsoluteValue).any()

def frameDiffDetectionRH(frame1, frame2, tresholdDetectionPercent, mask=np.array([])):
    diffrenceFrame = cv2.absdiff(frame1, frame2)

    # check mask eistance by any
    if mask.any():
        diffrenceFrame = diffrenceFrame & mask

    #median filter
    diffrenceFrame = cv2.medianBlur(diffrenceFrame, 3)
    

    if DEBUG_MODE == True:
        cv2.imshow("",diffrenceFrame)
        cv2.waitKey(1)
        print("Max value in deffrence frame:"+str(np.max(diffrenceFrame)))

    tresholdAbsoluteValue = 2**(8*diffrenceFrame.dtype.itemsize) * tresholdDetectionPercent / 100
        #tresholdAbsoluteValue = maxValueOfPixel * tresholdDetectionPercent / 100
    return np.greater(diffrenceFrame, tresholdAbsoluteValue).any()


class CameraManager:
    def __init__(self, camera, mask=None):
        ret1, self.frameOld = camera.read()
        ret2, self.frameNew = camera.read()
        self.camera = camera
        self.mask = mask
    #return False if Frame not readed, True if readed correctly
    def updateFrameForDynamicAlg(self):
        self.old = self.New
        ret, self.New = camera.read()
        return ret
    #return False if Frame not readed, True if readed correctly
    def updateFrameForStaticAlg(self):
        ret, self.New = camera.read()
        return ret
    def calculateOutput(self,algorithm, treshold, blur=):
        algorithm(self.frameOld,self.frameNew, treshold, self.mask, blur)
        frameDiffDetectionRGB(frame1, frame2, tresholdDetectionPercent, mask=np.array([]), blur=1)