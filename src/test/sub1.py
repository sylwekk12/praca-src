import sys
sys.path.append("..")
import algorithms.substracts
import cv2
import logging

#2 arguments
  #arg1 path to vid/stream
  #arg2 mask - optional

#init arguments
try:
    dataPath = sys.argv[1]
except:
    logging.warning("First argunent (data file path) default path is data needed")
    exit()
try:
    mask = sys.argv[2]
except:
    logging.debug("Second Argument not given")

kamera = cv2.VideoCapture(dataPath)
if not kamera.isOpened():
    logging.error(f"Cannot init cv2.VideoCapture from file: {dataPath}")


while()
ret, frame = kamera.read()
