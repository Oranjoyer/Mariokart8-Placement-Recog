import cv2
import deriveAttributes
import getAverageFrame
from collections import Counter
import numpy as np
TALLY_LIMIT = 1
FRAME_MIX_LIMIT = 5
class VideoCap:
    def __init__(self,cv2Video,name):
        self.currentPlace = 0
        self.racing = 0
        self.placeChanging = 0
        self.cap = cv2Video
        self.finalPlace=-1
        self.placeTally = []
        self.frameBuffer = []
        self.frameMix = []
        self.name = name
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
        self.cap.read()

        ret, frame = self.cap.read()
        if(frame.shape[:1]!=[720,1280]):
            frame = cv2.resize(frame,(1280,720))
        if ret == True:
            frame=self.addFrame(frame)
            cv2.imshow('Frame'+str(self),frame)
            self.updateRacing(frame)
            # currentPlace=self.addTally(place[1])
            cv2.waitKey(1)
    def updateRacing(self,frame):
        if(self.racing == 0):
            if(deriveAttributes.getGo(frame)):
                print(self.name + " race started")
                # print(np.mean(frame))
                self.racing = 1
                self.finalPlace = 0
        else:
            if(self.racing):
                place = deriveAttributes.getPlace(frame)[1]
                # print(place)
                if(place != 0):
                    self.placeChanging=0
                    if(self.currentPlace!=place):
                        print(self.name + " moved to " + str(place))
                    self.currentPlace = place
                else:
                    if(not(self.placeChanging)):
                        print(self.name + " changing placement")
                    self.placeChanging = 1
                if(deriveAttributes.getFinish(frame)):
                    self.racing = 0
                    print(self.name + " Finished")
        if ((self.racing==0) & (self.finalPlace==0)):
            place = deriveAttributes.getPlace(frame)[1]
            if(place > 0):
                self.finalPlace=place
                self.currentPlace=place
                print(self.name + " Final Place is " + str(place))

    def __str__(self) -> str:
        return self.name
            

