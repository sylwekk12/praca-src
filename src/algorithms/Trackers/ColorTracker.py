import cv2
import numpy as np
import statistics as stats
from functools import reduce


class ColorTracker:  # fork
    def __init__(self, frame, colorSelector, minDetectedContourAreaTh=300):
        self.frameStored = frame
        self.colorSelector = colorSelector
        self.trackVector = np.array([], dtype=np.int32)
        self.maxTrackerPoints = 10
        self.minDetectedContourAreaTh = minDetectedContourAreaTh

    def calculate(self, frame):
        selectedColorFrame = self.colorSelector.makeMaskFromRGB(frame)
        selectedColorFrame = cv2.medianBlur(selectedColorFrame, 13)
        contours, h = cv2.findContours(selectedColorFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # CHAIN_APPROX_SIMPLE - przechowuje punkty oznaczające początki i końce łączących ich lini (opis konturu linią)
        # CHAIN_APPROX_NONE - optional

        cv2.imshow("mask", selectedColorFrame)
        cv2.waitKey(1)

        if len(contours) <= 0:
            return frame

        approxContour = list()
        for cnt in contours:
            # approx
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approxContour.append(cv2.approxPolyDP(cnt, epsilon, True))

        sortedContours = sorted(approxContour, key=lambda contour: cv2.contourArea(contour), reverse=True)

        if cv2.contourArea(sortedContours[0]) < 300:  # TODO: threshold
            return frame

        M = cv2.moments(sortedContours[0])
        if M["m00"] != 0:
            X = int(M["m10"] / M["m00"])
            Y = int(M["m01"] / M["m00"])
            frame = cv2.circle(frame, (X, Y), 2, (0, 255, 0))
        else:
            return frame

        if len(self.trackVector.reshape((-1, 1, 2))) > self.maxTrackerPoints:
            self.trackVector = np.delete(self.trackVector, [0, 1])

        self.trackVector = np.append(self.trackVector, np.array([X, Y]))

        # for point in self.trackVector:
        self.trackVector = self.trackVector.reshape((-1, 1, 2))
        cv2.polylines(frame, np.int32([self.trackVector]), False, (0, 0, 255))

        self.frameStored = frame
        return frame
