import cv2
import getAverageFrame
import os
TEMPLATE_DIR = "MKImageData"
FILES = os.listdir(TEMPLATE_DIR)

def cropFrame(frame, x1, y1, x2, y2):
        if len(frame.shape)==3:
            frame_height, frame_width, _ = frame.shape
        else:
            frame_height, frame_width = frame.shape
        spot1 = [int(frame_width*(x1*.01)), int(frame_height*(y1*0.01))]
        spot2 = [int(frame_width*x2*.01), int(frame_height*y2*.01)]

        return frame[spot1[1]:spot2[1], spot1[0]:spot2[0]]
def createPlaces():
    for i in range(12):
        frame=getAverageFrame.getAverageFrameColor(getAverageFrame.filesToImage(getAverageFrame.filterPlace(FILES,i+1)))
        # cv2.imshow('Debug' + str(i+1),frame)
        cv2.imwrite("PlaceTemplates/" + str(i+1)+"Place.jpg",getAverageFrame.highPass(cropFrame(frame,85, 79, 94.5, 95)))
def createFinish():
    frame = getAverageFrame.getAverageFrame(getAverageFrame.imagesFromFilter(FILES,["Finish","Line"]))
    frame = cropFrame(frame,24.1,33,76.1,53)
    cv2.imwrite("Go&Finish/Finish.jpg",frame)
def createGo():
    frame = getAverageFrame.getAverageFrame(getAverageFrame.imagesFromFilter(FILES,["Go!"]))
    frame = cropFrame(frame,36.875,32.625,63.195,54.195)
    cv2.imwrite("Go&Finish/Go!.jpg",frame)
def createRankings():
    frame = getAverageFrame.getAverageFrame(getAverageFrame.imagesFromFilter(FILES,["Rankings"]))
    frame = cropFrame(frame,42.89,6.5,42.89+53.47,14)
    cv2.imwrite("RankTemplates/Rankings.jpg",frame)
createGo()
createPlaces()
createFinish()
createRankings()

    
