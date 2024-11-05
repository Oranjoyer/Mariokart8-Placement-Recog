import cv2
import numpy as np
import sys
import statistics as stats
import getAverageFrame
from threading import Thread
from time import sleep
video = cv2.VideoCapture("mkVidT.mkv")
frameLine = []
averageAverage = []
totalSize = 0
sixPlace = cv2.imread("6th.png")
SizeOfList = 3
run = True
averageSpan = SizeOfList-1
p=0
placeAtlas = cv2.imread("PlaceAtlasB.png")
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(str(frame_width) + ":" + str(frame_height))
def addFrames():
     while run:
          ret, vid = video.read()
          frameLine.append()
def cropFrame(frame, x1, y1, x2, y2):
        spot1 = [int(frame_width*(x1*.01)), int(frame_height*(y1*0.01))]
        spot2 = [int(frame_width*x2*.01), int(frame_height*y2*.01)]

        return frame[spot1[1]:spot2[1], spot1[0]:spot2[0]]
def getPlaceNumber(num):
     assert num > 0 & num <=12, "Num is " + str(num) + ". It should be in between 1-12"
     return placeAtlas[64:128, 180*(num-1):180*num]
def main():
    while True:
        video.read()
        video.read()
        video.read()
        video.read()
        video.read()
        # video.read()
        # video.read()
        # video.read()
        # ret, frame = video.read()
        
        placeFrame= cropFrame(getAverageFrame(), 85, 79, 94.5, 95) 
        # print(type(frameLine[0]))
        # cv2.imshow('hmm',getAverageAverage())
        # placeFrame = getAverageFrame()
        # cv2.imshow('Atlas', highPass(getPlaceNumber(5)))
        cv2.imshow('Camera', placeFrame)
        # while cv2.waitKey(1) != ord('o'):
        #     print("e")
        findPlace(placeFrame)
        if cv2.waitKey(1) == ord('q'):
            break
def findPlace(frame):
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    res = cv2.matchTemplate(frame,)

    

     
main()

# int(frame_width*(0))
# int(frame_height*(0))