import cv2
import numpy as np
import os
# import deriveAttributes

TEMPLATE_DIR = "MKImageData"
types = ["Place","Finish","Drift"]
PLACE_NAME = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"]
DEBUG = False
# VIDEO =
def main():
    # type = ""
    # inputValid=False
    # while not(inputValid):
    #     for i in range(len(types)):
    #         print(str(i) + ". " + str(types[i]))
    #     type=input("Select Type:")
    #     try:
    #         inputValid = (int(type) >=0) & (int(type) < len(types))
    #         # print(inputValid)
    #         if(not(inputValid)):
    #             print("Invalid Input")
    #     except:
    #         print("Use Integer")

    files = os.listdir(TEMPLATE_DIR)
    # print(filterPlace(files,1))
    # place = getAverageFrameColor(filesToImage(filterPlace(files, 1))) 
# for im in place:
    # cv2.imshow('Pic',place)
    # cv2.imshow('HighPass',highPass(place))
    # cv2.imshow('OtherPass',getAverageFrameColor(filesToImage(filterPlace(files, 1))))
    # cv2.waitKey(0)
    # cv2.imshow('pic',getAverageFrameColor(filesToImage(filterString(files,["Drive"])))) 
    # cv2.imshow('Everything.10-30.'+".jpg", getAverageFrameColor(imagesFromFilter(files,["Drive"])))
    # for i in range(12):
    #     frame=getAverageFrameColor(filesToImage(filterPlace(files,i+1)))
    #     cv2.imshow('Debug' + str(i+1),frame)
    #     cv2.imwrite("PlaceTemplates/" + str(i+1)+"Place.jpg",highPass(deriveAttributes.cropFrame(frame,85, 79, 94.5, 95)))
    # cv2.imshow('pic2',getAverageFrameColor([getAverageFrameColor(filesToImage(filterPlace(files, 1))[:3]),np.tile(getAverageFrame(filesToImage(filterPlace(files, 1)))[...,None],3)]))
    cv2.waitKey(0)


def OutImagesFromFilter(files,filter,directory):
    return OutFilesToImage(filterString(files,filter),directory)
def imagesFromFilter(files,filter):
    return OutImagesFromFilter(files,filter,directory=TEMPLATE_DIR)
def OutFilesToImage(files,directory):
    list = []
    for f in files:
        # print(direct)
        list.append(cv2.imread(directory+"/"+f))
    return list
def filesToImage(files):
    return OutFilesToImage(files, directory=TEMPLATE_DIR)
def filterPlace(files, place):
    return filterString(files,[PLACE_NAME[place-1],"Drive","!PlaceChange"])
def filterString(files, strings):
    listOf = files.copy()
    for f in files:
        if not(".jpg" == f[-4:] or ".png" == f[-4:]):
                    print(f)
                    if f in listOf:
                        listOf.remove(f)
        else:
            for s in strings:
                if s[0:1] == "!":
                    if s[1:] + "." in f:
                        print(f)
                        if f in listOf:
                            listOf.remove(f)
                else:
                    if not(s + "." in f):
                        print(f)
                        if f in listOf:
                            listOf.remove(f)
    return listOf
def getAverageFrame(frameLine):
    # averageFrame = np.zeros((720,1280), np.uint8)
    # global DEBUG
    if len(frameLine) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = highPass(frameLine[0])
    for i in range(len(frameLine)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), highPass(frameLine[i+1]), getWeight(i),0.0)
        if DEBUG:
            cv2.imshow('Debug',averageFrame)
            cv2.imshow('DebugFrameAdded',frameLine[i+1])
            cv2.waitKey(0)
    return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    

def getWeight(iterations):
    base = 1/(iterations+2)
    return base
def getAverageFrameColor(frameLine):
    if len(frameLine) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = frameLine[0]
    for i in range(len(frameLine)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), frameLine[i+1], getWeight(i),0.0)
        if DEBUG:
            cv2.imshow('Debug',averageFrame)
            cv2.imshow('DebugFrameAdded',frameLine[i+1])
            cv2.waitKey(0)
            # cv2.destroyWindow("Debug")
    # return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return averageFrame

def highPass(frame):
    passF = frame - cv2.GaussianBlur(frame,(21,21),3)+127
    if(len(passF.shape)>2):
        passF = cv2.cvtColor(passF, cv2.COLOR_BGR2GRAY)
    passF = cv2.Laplacian(passF, -1)
    return passF
def grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
def colorPass(frame):
    passF = frame
    passF = passF - cv2.GaussianBlur(passF,(21,21),3)+127
    passF = cv2.Laplacian(passF, -1)

    return passF

# Start Main Function


