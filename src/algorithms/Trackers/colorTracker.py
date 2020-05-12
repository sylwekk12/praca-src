import cv2
import numpy as np
from algorithms.AlgorithmHelps import helperHSV
import statistics as stats
from functools import reduce

class ColorTracker:
    def __init__(self, frame, colorSelector):
        self.frameStored = frame
        self.colorSelector = colorSelector
        self.trackVector = np.array([], dtype=np.int32)
        self.maxTrackerPoints = 10

    def calculate(self, frame):
        selectedColorFrame = self.colorSelector.makeMaskFromRGB(frame)
        selectedColorFrame = cv2.medianBlur(selectedColorFrame, 13)
        conturs, h = cv2.findContours(selectedColorFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #CHAIN_APPROX_SIMPLE - przechowuje punkty oznaczające początki i końce łączących ich lini (opis konturu linią)

        listX = []
        listY = []
        for contour in conturs:
            if contour.size < 100:
                continue
            M = cv2.moments(contour)
            if M["m00"] != 0:
                listX.append(int(M["m10"] / M["m00"]))
                listY.append(int(M["m01"] / M["m00"]))
                frame = cv2.circle(frame, (listX[-1], listY[-1]), 2, (0,255,0))
            else: continue

            cv2.drawContours(selectedColorFrame, [contour], -1, 126, 2)
            if len(self.trackVector.reshape((-1,1,2))) > self.maxTrackerPoints:
                self.trackVector = np.delete(self.trackVector, [0,1])

        if len(listX) > 0:
            self.trackVector = np.append(self.trackVector, np.array([stats.mean(listX), stats.mean(listY)]))

        #for point in self.trackVector:
        self.trackVector = self.trackVector.reshape((-1,1,2))
        cv2.polylines(frame, np.int32([self.trackVector]), False, (0,0,255))

        self.frameStored = frame
        return frame

class ColorTracker2: #fork
    def __init__(self, frame, colorSelector):
        self.frameStored = frame
        self.colorSelector = colorSelector
        self.trackVector = np.array([], dtype=np.int32)
        self.maxTrackerPoints = 10

    def calculate(self, frame):
        selectedColorFrame = self.colorSelector.makeMaskFromRGB(frame)
        selectedColorFrame = cv2.medianBlur(selectedColorFrame, 13)
        conturs, h = cv2.findContours(selectedColorFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # CHAIN_APPROX_SIMPLE - przechowuje punkty oznaczające początki i końce łączących ich lini (opis konturu linią)
        # CHAIN_APPROX_NONE - should ave better performance

        cv2.imshow("mask",selectedColorFrame)
        cv2.waitKey(1)

        if len(conturs) <= 0:
            return frame

        conturs = sorted(conturs, key=lambda contour: contour.size, reverse=True)

        if conturs[0].size < 150:#TODO: treshold
            return frame

        M = cv2.moments(conturs[0])
        if M["m00"] != 0:
            X = int(M["m10"] / M["m00"])
            Y = int(M["m01"] / M["m00"])
            frame = cv2.circle(frame, (X,Y), 2, (0, 255, 0))
        else: return frame

        #cv2.drawContours(selectedColorFrame, [conturs[0]], -1, 126, 2)
        if len(self.trackVector.reshape((-1, 1, 2))) > self.maxTrackerPoints:
            self.trackVector = np.delete(self.trackVector, [0, 1])

        self.trackVector = np.append(self.trackVector, np.array([X, Y]))

        # for point in self.trackVector:
        self.trackVector = self.trackVector.reshape((-1, 1, 2))
        cv2.polylines(frame, np.int32([self.trackVector]), False, (0, 0, 255))

        self.frameStored = frame
        return frame


class ColorTracker3:  # fork
    def __init__(self, frame, colorSelector):
        self.frameStored = frame
        self.colorSelector = colorSelector
        self.trackVector = np.array([], dtype=np.int32)
        self.maxTrackerPoints = 10

    def calculate(self, frame):
        selectedColorFrame = self.colorSelector.makeMaskFromRGB(frame)
        selectedColorFrame = cv2.medianBlur(selectedColorFrame, 13)
        conturs, h = cv2.findContours(selectedColorFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # CHAIN_APPROX_SIMPLE - przechowuje punkty oznaczające początki i końce łączących ich lini (opis konturu linią)
        # CHAIN_APPROX_NONE - should ave better performance

        cv2.imshow("mask",selectedColorFrame)
        cv2.waitKey(1)

        if len(conturs) <= 0:
            return frame

        contoursWithArea = []
        for contour in conturs:
            contoursWithArea.append([contour, cv2.contourArea(contour)])

        contoursWithAreaSorted = sorted(contoursWithArea, key=lambda contourA: contourA[1], reverse=True)
        contur = contoursWithAreaSorted[0][0]
        area = contoursWithAreaSorted[0][1]

        if area < 150: #TODO: treshold
            return frame

        M = cv2.moments(contur)
        if M["m00"] != 0:
            X = int(M["m10"] / M["m00"])
            Y = int(M["m01"] / M["m00"])
            frame = cv2.circle(frame, (X, Y), 2, (0, 255, 0))
        else:
            return frame

        # cv2.drawContours(selectedColorFrame, [contours], -1, 126, 2)
        if len(self.trackVector.reshape((-1, 1, 2))) > self.maxTrackerPoints:
            self.trackVector = np.delete(self.trackVector, [0, 1])

        self.trackVector = np.append(self.trackVector, np.array([X, Y]))

        # for point in self.trackVector:
        self.trackVector = self.trackVector.reshape((-1, 1, 2))
        cv2.polylines(frame, np.int32([self.trackVector]), False, (0, 0, 255))

        self.frameStored = frame
        return frame