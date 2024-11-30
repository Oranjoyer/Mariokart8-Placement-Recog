import cv2
import numpy as np
import getAverageFrame

places = []
placesHalf = []
FINISH=getAverageFrame.grayscale(cv2.imread("Go&Finish/Finish.jpg"))
GO=getAverageFrame.grayscale(cv2.imread("Go&Finish/Go!.jpg"))
RANKINGS=getAverageFrame.grayscale(cv2.imread("RankTemplates/Rankings.jpg"))
FINISH_HALF=getAverageFrame.grayscale(cv2.imread("Go&Finish/Finish0.5.jpg"))
GO_HALF=getAverageFrame.grayscale(cv2.imread("Go&Finish/Go!0.5.jpg"))
RANKINGS_HALF=getAverageFrame.grayscale(cv2.imread("RankTemplates/Rankings0.5.jpg"))
# COMM_ERR=getAverageFrame.grayscale(cv2.imread("ErrorTemplates/Comm.jpg"))
for i in range(12):
     places.append(getAverageFrame.grayscale(cv2.imread("PlaceTemplates/" + str(i+1) + "Place.jpg")))
for i in range(12):
     placesHalf.append(getAverageFrame.grayscale(cv2.imread("PlaceTemplates/" + str(i+1) + "Place0.5.jpg")))

def deriveAttributes(inputFrame):
    attributeString =""
    attributeString += trackDerive(inputFrame) + "."

def trackDerive(input,scale):
    # TBD
    return "NoTrack"

def cropFrame(frame, x1, y1, x2, y2):
        if((x1==0)&(y1==0)&(x2==100)&(y2==100)):
            return frame
        if len(frame.shape)==3:
            frame_height, frame_width, _ = frame.shape
        else:
            frame_height, frame_width = frame.shape
        spot1 = [int(frame_width*(x1*.01)), int(frame_height*(y1*0.01))]
        spot2 = [int(frame_width*x2*.01), int(frame_height*y2*.01)]

        return frame[spot1[1]:spot2[1], spot1[0]:spot2[0]]

def getPlace(frame,scale):
    frame = getAverageFrame.highPass(cropFrame(frame, 85, 79, 94.5, 95))
    highestMatch = 0
    bestMatch = 0
    placesTemplate = places
    if(scale==0.5):
        placesTemplate=placesHalf
    for i in range(12):
        place = placesTemplate[i]
        # cv2.imshow("e",place)
        # cv2.waitKey(1)
        res = cv2.matchTemplate(frame,place,cv2.TM_CCOEFF_NORMED)
        loc = np.max(res)
        if((loc>highestMatch) & (loc > 0.15)):
             highestMatch = loc
             bestMatch = (i+1)
    return highestMatch, bestMatch
def getFinish(frame,scale):
    threshold = 0.15
    frame = getAverageFrame.grayscale(cropFrame(frame,24.1,33,76.1,53))
    if(np.mean(frame)<1):
        return False
    # print(np.mean(frame))
    # cv2.imshow("DebugFinish",frame)
    frame = getAverageFrame.highPass(frame)
    templateIm=FINISH
    if(scale==0.5):
        templateIm=FINISH_HALF
    # print(templateIm==FINISH_HALF)
    res = cv2.matchTemplate(frame,templateIm,cv2.TM_CCOEFF_NORMED)
    loc = np.max(res)
    return (loc > threshold)==True
def getGo(frame,scale):
    threshold = 0.1
    frame = getAverageFrame.grayscale(cropFrame(frame,36.875,32.625,63.195,54.195))
    if(np.mean(frame)<1):
        return False
    # print(np.mean(frame))
    # cv2.imshow("DebugGo",frame)
    frame = getAverageFrame.highPass(frame)
    templateIm = GO
    if(scale==0.5):
        templateIm=GO_HALF
    res = cv2.matchTemplate(frame,templateIm,cv2.TM_CCOEFF_NORMED)
    loc = np.max(res)
    # print(loc)
    return (loc > threshold)==True
def getRankings(frame,scale):
    threshold = 0.1
    frame = getAverageFrame.grayscale(cropFrame(frame,42.89,6.5,42.89+53.47,14))
    if(np.mean(frame)<1):
        return False
    # print(np.mean(frame))
    # cv2.imshow("DebugGo",frame)
    frame = getAverageFrame.highPass(frame)
    templateIm=RANKINGS
    if(scale==0.5):
        templateIm=RANKINGS_HALF
    res = cv2.matchTemplate(frame,templateIm,cv2.TM_CCOEFF_NORMED)
    loc = np.max(res)
    # print(loc)
    return (loc > threshold)==True
# def isCommErr(frame):
#     threshold = 0.1
#     frame = getAverageFrame.grayscale(cropFrame(frame,42.89,6.5,42.89+53.47,14))
#     if(np.mean(frame)<1):
#         return False
#     # print(np.mean(frame))
#     # cv2.imshow("DebugGo",frame)
#     frame = getAverageFrame.highPass(frame)
#     res = cv2.matchTemplate(frame,COMM_ERR,cv2.TM_CCOEFF_NORMED)
#     loc = np.max(res)
#     # print(loc)
#     return (loc > threshold)==True
     


