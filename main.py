import getAverageFrame
import deriveAttributes
import cv2
import videoDerive
# getAverageFrame.main()

# print(deriveAttributes.getPlace(cv2.imread("MKImageData/TheUnlabeleds/2024103017090500_s.jpg")))
videoSource =[]
# videoSource.append(videoDerive.VideoCap(cv2.VideoCapture(0),"Cam"))
# videoSource.append(videoDerive.VideoCap(cv2.VideoCapture("mkVidT.mkv"),"Video1"))
for i in range(4):
    videoSource.append(videoDerive.VideoCap(cv2.VideoCapture(0),"Video"+str(i)))
# videoSource.append(videoDerive.VideoCap(cv2.VideoCapture("mkTrim.mkv"),"Video4"))
while(True):
    for video in videoSource:
        video.getCurrentFrame()