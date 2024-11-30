import cv2
import deriveAttributes
import getAverageFrame
from collections import Counter
import numpy as np
from threading import Thread
TALLY_LIMIT = 1
FRAME_MIX_LIMIT = 5

class VideoCap:
    def __init__(self,cv2Video,name,order):
        self.currentFrame = cv2Video.read()
        self.currentPlace = 0
        self.racing = 0
        self.placeChanging = 0
        self.finished = 0
        self.cap = cv2Video
        self.finalPlace=-1
        self.placeTally = []
        self.frameBuffer = []
        self.frameMix = []
        self.name = name
        self.team = "White"
        self.order = order
        self.crop = [0,0,100,100]
        self.scale = 1
    def updateFrame(self):
            ret, frame = self.cap.read()
            self.currentFrame = ret, self.addFrame(frame)
    def addTally(self,place):
        if(TALLY_LIMIT==1):
            return place
        self.placeTally.append(place)
        if len(self.placeTally)>TALLY_LIMIT:
            del self.placeTally[0]
        return Counter(self.placeTally).most_common(1)[0][0]
    def addFrame(self,frame):
        self.frameMix.append(frame)
        if len(self.frameMix)>FRAME_MIX_LIMIT:
            del self.frameMix[0]
        return getAverageFrame.getAverageFrameColor(self.frameMix)
    
    def getCurrentFrame(self):
        # self.updateFrame()
        # ret, frame = self.currentFrame[0], self.addFrame(self.currentFrame[1])
        ret, frame = self.currentFrame
        if(type(frame)==type(None)):
            print("Error, No image")
            return
        if(self.crop != [0,0,100,100]):
            frame = deriveAttributes.cropFrame(frame,self.crop[0],self.crop[1],self.crop[2],self.crop[3])
        if(frame.shape[:1]!=[720,1280]):
            frame = cv2.resize(frame,(1280,720))
        if ret == True:
            self.updateRacing(frame)
    def updateRacing(self,frame):
        if(self.racing == 0):
            if(deriveAttributes.getGo(frame,self.scale)):
                print(self.name + " race started")
                # print(np.mean(frame))
                self.racing = 1
                self.finalPlace = 0
        else:
            if(self.racing):
                confidence, place = deriveAttributes.getPlace(frame,self.scale)
                # print((confidence, place))
                if(place != 0):
                    self.placeChanging=0
                    if(self.currentPlace!=place):
                        print(self.name + " moved to " + str(place))
                    self.currentPlace = place
                else:
                    self.placeChanging = 1
                if(deriveAttributes.getFinish(frame,self.scale)):
                    self.racing = 0
                    self.finished = 1
                    print(self.name + " Finished")
        if self.racing==0:
            if (self.finalPlace==0):
                confidence, place = deriveAttributes.getPlace(frame,self.scale)
                if(place > 0):
                    # print(confidence)
                    self.finalPlace=place
                    self.currentPlace=place
                    print(self.name + " Final Place is " + str(place))
            else: 
                if(self.finished==1):
                    rankScreen = deriveAttributes.getRankings(frame,self.scale)
                    if(rankScreen):
                        self.finished=0

    def __str__(self) -> str:
        return self.name
            

