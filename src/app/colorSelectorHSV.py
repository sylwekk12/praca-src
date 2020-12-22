import cv2
import numpy as np
import sys

sys.path.append("..")
from utils import colorHelper

# also image can be used

baseImg = None

##### alternatevely comment this and press image like 'baseImg = cv2.imread("path to file")'
#captureCameraVideo = cv2.VideoCapture("../../data/SimpleStreet.mp4")
captureCameraVideo = cv2.VideoCapture(0)

if not captureCameraVideo.isOpened():
    print("camera: capture init failed!")
    exit(0)

while True:
    _, img = captureCameraVideo.read()
    baseImg = img.copy()
    cv2.putText(img, "press 'c' to select frame", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    cv2.imshow('frame selector', img)
    keyCode = cv2.waitKey(10)
    if keyCode is ord("q"):
        print("I quit!")
        exit(0)
    if keyCode is ord("c"):
        print("Captured frame successful!")
        break
#####
cv2.destroyAllWindows()

baseImg = cv2.resize(baseImg,(640,490))
####################################
# end section image initialization #
####################################


LAST_USED_TB = None


def f_min(argMock=None):
    global LAST_USED_TB
    LAST_USED_TB = "MIN"


def f_max(argMock=None):
    global LAST_USED_TB
    LAST_USED_TB = "MAX"


def mock(argMock=None):
    pass

#init Trackbars
cv2.namedWindow("TestBars")
cv2.resizeWindow("TestBars", 680, 240)
cv2.createTrackbar("H min", "TestBars", 0, 179, mock)
cv2.createTrackbar("H max", "TestBars", 179, 179, mock)
cv2.createTrackbar("S min", "TestBars", 0, 255, f_min)
cv2.createTrackbar("S max", "TestBars", 255, 255, f_max)
cv2.createTrackbar("V min", "TestBars", 0, 255, f_min)
cv2.createTrackbar("V max", "TestBars", 255, 255, f_max)

#init values
HMin = None
HMax = None
SMin = None
SMax = None
VMin = None
VMax = None

#program loop
while cv2.waitKey(10) != ord("q"):
    HMin = cv2.getTrackbarPos("H min", "TestBars")
    HMax = cv2.getTrackbarPos("H max", "TestBars")
    SMin = cv2.getTrackbarPos("S min", "TestBars")
    SMax = cv2.getTrackbarPos("S max", "TestBars")
    VMin = cv2.getTrackbarPos("V min", "TestBars")
    VMax = cv2.getTrackbarPos("V max", "TestBars")

    if LAST_USED_TB == "MIN":
        if SMin > SMax:
            cv2.setTrackbarPos("S min", "TestBars", SMax)
        if VMin > VMax:
            cv2.setTrackbarPos("V min", "TestBars", VMax)

    if LAST_USED_TB == "MAX":
        if SMin > SMax:
            cv2.setTrackbarPos("S max", "TestBars", SMin)
        if VMin > VMax:
            cv2.setTrackbarPos("V max", "TestBars", VMin)

    print(LAST_USED_TB)

    cs = colorHelper.ColorRangeSelector(*(HMin, SMin, VMin), *(HMax, SMax, VMax))
    mask = cs.selectColorFromImage(baseImg)
    if mask is not None:
        img = np.hstack((baseImg, mask))
        cv2.imshow("selector", img)

resultString = "format: H min:{HMin} H max:{HMax} S min:{SMin} S max:{SMax} V min:{VMin} V max:{VMax}"
print(resultString.format(HMin=HMin, HMax=HMax, SMin=SMin, SMax=SMax, VMin=VMin, VMax=VMax))

#clear
captureCameraVideo.release()
cv2.destroyAllWindows()
