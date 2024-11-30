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
def createPlaces(scale):
    for i in range(12):
        iscale = scale
        if(scale==1):
            iscale=""
        frame=getAverageFrame.getAverageFrameColor(scaleImagesToAndBack(getAverageFrame.filesToImage(getAverageFrame.filterPlace(FILES,i+1)),scale))
        # cv2.imshow('Debug' + str(i+1),frame)
        cv2.imwrite("PlaceTemplates/" + str(i+1)+f"Place{iscale}.jpg",getAverageFrame.highPass(cropFrame(frame,85, 79, 94.5, 95)))
def createFinish(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Finish","Line"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,24.1,33,76.1,53)
    cv2.imwrite(f"Go&Finish/Finish{scale}.jpg",frame)
def createGo(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Go!"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,36.875,32.625,63.195,54.195)
    cv2.imwrite(f"Go&Finish/Go!{scale}.jpg",frame)
def createRankings(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Rankings"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,42.89,6.5,42.89+53.47,14)
    cv2.imwrite(f"RankTemplates/Rankings{scale}.jpg",frame)
def scaleImagesToAndBack(images,scale):
     imageList = []
     for image in images:
          imageList.append(scaleSingleToAndBack(image,scale))
     return imageList
def scaleSingleToAndBack(image,scale):
    if(scale==1):
        return image
    return cv2.resize(cv2.resize(image,(int(1280*scale),int(720*scale))),(1280,720))
def createTemplates(scale):
    createGo(scale)
    createPlaces(scale)
    createFinish(scale)
    createRankings(scale)
createTemplates(1)
createTemplates(0.5)

    
