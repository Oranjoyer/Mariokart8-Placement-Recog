import cv2
import numpy as np
import getAverageFrame
places = []
for i in range(12):
     places.append(getAverageFrame.grayscale(cv2.imread("PlaceTemplates/" + str(i+1) + "Place.jpg")))

def deriveAttributes(inputFrame):
    attributeString =""
    attributeString += trackDerive(inputFrame) + "."

def trackDerive(input):
    # TBD
    return "NoTrack"

def cropFrame(frame, x1, y1, x2, y2):
        frame_height, frame_width, _ = frame.shape
        spot1 = [int(frame_width*(x1*.01)), int(frame_height*(y1*0.01))]
        spot2 = [int(frame_width*x2*.01), int(frame_height*y2*.01)]

        return frame[spot1[1]:spot2[1], spot1[0]:spot2[0]]

def getPlace(frame):
    frame = getAverageFrame.highPass(cropFrame(frame, 85, 79, 94.5, 95))
    highestMatch = 0
    bestMatch = 0
    for i in range(12):
        place = places[i]
        # cv2.imshow("e",place)
        # cv2.waitKey(1)
        res = cv2.matchTemplate(frame,place,cv2.TM_CCOEFF_NORMED)
        loc = np.max(res)
        if((loc>highestMatch) & (loc > 0.2)):
             highestMatch = loc
             bestMatch = (i+1)
    return highestMatch, bestMatch


