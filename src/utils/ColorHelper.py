import cv2
import numpy as np
import logging


class State:
    OK = "OK"
    ERROR = "ERROR"


# if HUp is less than HDown then selected range will be inverted
class ColorRangeSelector:
    def __init__(self, hd, sd, vd, hu, su, vu):
        self.state = State.OK
        self.rangeDown = np.array([hd, sd, vd])
        self.rangeUp = np.array([hu, su, vu])
        self._valid()
        if self.rangeDown[0] > self.rangeUp[0]:
            self.inverted = True
        else:
            self.inverted = False

    def makeMaskFromRGB(self, imgRGB):
        imgHSV = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2HSV)
        if not self.inverted:
            imgRangeHSV = cv2.inRange(imgHSV, self.rangeDown, self.rangeUp)
            return imgRangeHSV
        else:
            HDown = np.array((self.rangeUp[0], 255, 255))
            HUp = np.array((self.rangeDown[0], 0, 0))
            tmpDown = self.rangeDown.copy()
            tmpUp = self.rangeUp.copy()
            tmpDown[0] = 0
            tmpUp[0] = 179
            imgRangeSV = cv2.inRange(imgHSV, tmpDown, tmpUp)
            imgRangeH_partDown = cv2.inRange(imgHSV, np.array([(0, 0, 0)]), HDown)
            imgRangeH_partUp = cv2.inRange(imgHSV, HUp, np.array([(179, 255, 255)]))

            cv2.imshow("d", imgRangeH_partDown)
            cv2.waitKey(1)
            cv2.imshow("u", imgRangeH_partUp)
            cv2.waitKey(1)


            imgRangeHSV = cv2.bitwise_or(imgRangeH_partDown, imgRangeH_partUp)
            imgRangeHSV = cv2.bitwise_and(imgRangeHSV, imgRangeSV)
            return imgRangeHSV

    def selectColorFromImage(self, imgRGB):
        if self.state is not State.OK:
            return None
        mask = self.makeMaskFromRGB(imgRGB)
        return cv2.bitwise_and(imgRGB, imgRGB, None, mask)

    def _valid(self):
        self.state = State.OK
        if self.rangeDown[0] >= 180 or self.rangeUp[0] >= 180:
            logging.error("CloolrSelector:OUT_OF_RANGE_UP H")
            self.state = State.ERROR
        if self.rangeUp[1] > 255 or self.rangeUp[2] > 255 or self.rangeDown[1] > 255 or self.rangeDown[2] > 255:
            logging.error("CloolrSelector:OUT_OF_RANGE_UP S/V")
            self.state = State.ERROR
        if self.rangeUp.any() < 0 or self.rangeDown.any() < 0:
            logging.error("CloolrSelector:OUT_OF_RANGE_DONW: less than 0")
            self.state = State.ERROR
        if self.rangeDown[1] > self.rangeUp[1]:
            logging.error("CloolrSelector:INVALID_IMPUT: S up less than down")
            self.state = State.ERROR
        if self.rangeDown[2] > self.rangeUp[2]:
            logging.error("CloolrSelector:INVALID_IMPUT: V up less than down")
            self.state = State.ERROR


channels = ["H", "S", "V"]


class chanelDisabler():
    def __init(self, channel):
        if channel not in channels:
            Exception(f"Unsupported channel\nChannels supported:{channels}")

    def disableChannel(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame[:, :, 2] = 255
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        cv2.imshow("", frame)
        cv2.waitKey(1)
        return frame
