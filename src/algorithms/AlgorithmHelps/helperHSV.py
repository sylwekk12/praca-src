import cv2
import numpy as np

class ColorRangeSelector:
    def __init__(self, hd, sd, vd, hu, su, vu):
        self.rangeDown = np.array([hd,sd,vd])
        self.rangeUp = np.array([hu,su,vu])

    def makeMaskFromRGB(self, imgRGB):
        imgHSV = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2HSV)
        imgRangeHSV = cv2.inRange(imgHSV, self.rangeDown, self.rangeUp)
        return imgRangeHSV #cv2.cvtColor(imgRangeHSV, cv2.COLOR_HSV2BGR)

    def selectColorFromImage(self, imgRGB):
        mask = self.makeMaskFromRGB(imgRGB)
        return imgRGB & mask