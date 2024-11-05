import cv2
import os
import getAverageFrame
import threading
import queue
FILE_DIR="MKImageData/ToLabel"
FILES=os.listdir(FILE_DIR)
QUEUE = queue.Queue()
print(getAverageFrame.OutFilesToImage(FILES,FILE_DIR))
imagesList = getAverageFrame.OutImagesFromFilter(FILES,[],directory=FILE_DIR)
def main():
    for img in imagesList:
        cv2.imshow('Label',img)
        stringList
        cv2.imwrite(FILE_DIR+"/Labeled/"+stringList + ".jpg", img)
        print(FILE_DIR+"/Labeled/"+stringList)
main()