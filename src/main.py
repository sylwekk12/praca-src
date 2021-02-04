from algorithms.SimpleDifference import Substracts
from algorithms.BackgroundModling import MeanModel
from utils.ColorHelper import ColorRangeSelector
from algorithms.Trackers import ColorTracker
from utils.Executor import TestManager
from utils.VideoReader import VideoReader
import TestScenarios as ts
import cv2

##### input data

# move detection
Street1 = "../data/Street/S1.mp4"
Street2 = "../data/Street/S2.mp4"

# move tracking
YellowPencilTrack = "../data/YellowTracker.mp4"

##### Initialize Scenarios
testScenarios_Substractors = ts.TestScenarios_Substractors(Street2)
testScenario_Trackers = ts.TestScenario_Trackers(Street2)

##### Execute

# Simply difference
# testScenarios_Substractors.simplySubstr()

# Difference container Arithmetic
# testScenarios_Substractors.substrWithBufferArith()


# Difference container Geometric
# testScenarios_Substractors.substrWithBufferGeom()

# Difference container Euler
# testScenarios_Substractors.substrWithBufferEuler()


##### background

# Mean background modeling with container
# testScenarios_Substractors.backgroundMeanWithBuffer()

# Mean background modeling accelerated
# testScenarios_Substractors.backgroundMeanAccelerated()

# Median background modeling
testScenarios_Substractors.backgroundMedianWithBuffer()

# MOG2
# testScenarios_Substractors.backgroundMOG2()


##### color Tracker

# ColorTracker
# testScenario_Trackers.SimplyColorTracker(ts.Yellow)
