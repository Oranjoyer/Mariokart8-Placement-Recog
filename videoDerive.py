import cv2
import deriveAttributes
import getAverageFrame
frameFeed = []
feedLimit = 30
cap = cv2.VideoCapture("mkVidT.mkv")
def addFrame(frame):
    frameFeed.append(frame)
    if(len(frameFeed) > feedLimit):
        frameFeed.pop(0)
    
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        addFrame(frame)
        frame = getAverageFrame.getAverageFrameColor(frameFeed)
        cv2.imshow('Frame',frame)
        place = deriveAttributes.getPlace(frame)
        print(place)
        placeConf, place = place
        if place == 0:
            cv2.imshow("hmm", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

