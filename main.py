import getAverageFrame
import deriveAttributes
import cv2

getAverageFrame.main()

print(deriveAttributes.getPlace(cv2.imread("MKImageData/TheUnlabeleds/2024103017090500_s.jpg")))
