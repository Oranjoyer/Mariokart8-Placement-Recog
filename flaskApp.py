from flask import Flask,render_template,request,make_response
import videoDerive
from threading import Thread
import cv2
import json
import numpy as np
import time
import base64
import platform
import sys
SYSTEM = platform.system()
CROP_LIST = [[0,0,50,50],[50,0,100,50],[0,50,50,100],[50,50,100,100]]
jsonObj = ""
cameraList=[]
UNLIMITED_POWER=False
dataUpdated=False
obsCamMode=False
obsCamera=-1
stopCollection=True
sortPlace = False
PRE_REC = False
videoSource=[]
cameraCaptureList=[]
fileList=[]
VID_FILES=[]
def checkArgs(args):
    global PRE_REC
    for arg in args:
        # print(getModeType(arg))
        PRE_REC = getModeType(arg)=="file"
def getModeType(string):
    # print("mode:  " + string[0:6])
    if(string[0:7]=="--mode="):
            type = string[7:]
            return type
    return None

            
def grabStringInQuotes(string):
    quoteSpots =[]
    if(len(string)<3):
        print("string too small")
        return None
    for i in range(len(string)):
        if(string[i]=="\""):
            quoteSpots.append(i)
        if(len(quoteSpots)==2):
            if((quoteSpots[0]+1)==quoteSpots[1]):
                print("Quotes Side-By-Side")
                return ""
            print(string[quoteSpots[0]+1:quoteSpots[1]-1])
            return string[quoteSpots[0]+1:quoteSpots[1]-1]
    print("No Quoted Text Found")
    return None
def setFiles(args):
    #Var to check if last argument declared was a --file flag
    fileLast=False
    videoData = []
    currentData = []
    for arg in args:
        fileLast
        if(arg[0:6]=="--file="):
            if(len(currentData)<2):
                currentData.append("")
            currentData.append(0)
            videoData.append(currentData)
            currentData = ""
            currentData.append(grabStringInQuotes(arg))
            fileLast=True
        elif(fileLast):
            currentData.append(grabStringInQuotes(arg))
            
def main():
    args = sys.argv.copy()[1:]
    if((len(args)==1)and(getModeType(args[0])=="file")):
        print("DEBUG: Mode Type Set to \'file\' without any files listed. Continuing in camera mode")
    elif(len(args) > 1):
        checkArgs(args)
    flaskApp()
    
def flaskApp():
    global PRE_REC
    if(not(PRE_REC)):
        checkCameras()
    app = Flask(__name__)
    # videoSource = []
    # for i in range(4):
    #     videoSource.append(videoDerive.VideoCap(cv2.VideoCapture(1),"Video"+str(i)))
    
    @app.route('/')
    def page():
        data = {"number":-1,"type":"both"}
        return render_template('places.html',data=json.dumps(data))
    @app.route('/place')
    def placeSpot():
        data = {'number':-1,'type':'place'}
        return render_template('places.html',data=json.dumps(data))
    @app.route('/name')
    def nameSpot():
        data = {'number':-1,'type':'name'}
        return render_template('places.html',data=json.dumps(data))
    @app.route('/<number>')
    def cameraSpot(number):
        data = {"number":number,"type":"both"}
        return render_template('places.html', data=json.dumps(data))
    @app.route('/<number>/place')
    def cameraPlaceSpot(number):
        data = {'number':number,'type':'place'}
        return render_template('places.html',data=json.dumps(data))
    @app.route('/<number>/name')
    def cameraNameSpot(number):
        data = {'number':number,'type':'name'}
        return render_template('places.html',data=json.dumps(data))
    # def cameraSpot():
    #     return render_template('places.html')
    @app.route('/sendOBS', methods=["POST","GET"])
    def setObs():
        if(request.method=="GET"):
            return "Wrong Way"
        global obsCamMode
        global obsCamera 
        obsCamera = cameraCaptureList[cameraList[int(request.data)]]
        print(int(request.data))
        obsCamMode = True
        return "Success"
    @app.route('/disableOBS')
    def disableObs():
        global obsCamera
        obsCamera = None
        global obsCamMode
        obsCamMode = False
        return "OBS Mode Disabled"
    @app.route('/manage')
    def management():
        if(PRE_REC):
            return render_template("preRecError.html",obsMode=obsCamMode, readingData=not(stopCollection))
        return render_template("manage.html",obsMode=obsCamMode, readingData=not(stopCollection))
    @app.route('/sendCams',methods=['POST','GET'])
    def sendCams():
        if(request.method=='POST'):
            print(request.data)
            cameraList= json.loads(request.data)
            if(obsCamMode):
                setOBSCams(cameraList)
            else:
                setCameraSource(cameraList)
            return "Cam Data Received"
        if(request.method=='GET'):
            return "Wrong Way"
    @app.route("/start")
    def start():
        manageCollectionFunction(True)
        print("Recognition Started")
        return "Recognition Started"
    @app.route("/stop")
    def stop():
        manageCollectionFunction(True)
        print("Recognition Stopped")
        return "Recognition Stopped"
    @app.route("/toggleOrder")
    def toggle():
        global sortPlace
        sortPlace=not(sortPlace)
        print("Sort Toggled")
        return "Sort Toggled"
    @app.route("/camList")
    def cameras():
        if(len(cameraList)==0):
            checkCameras()
        if(obsCamMode):
            # print(json.dumps(range(4)))
            return json.dumps([0,1,2,3])
        return json.dumps(cameraList)
    @app.route("/checkCams")
    def checkCams():
        checkCameras()
    @app.route("/camImage/<number>")
    def cameraImg(number):
        capture = None
        if(obsCamMode):
            ret, capture = obsCamera.read()
        else:
            ret, capture = cameraCaptureList[int(number)].read()
        if(obsCamMode):
            capture = cropFrame(capture,CROP_LIST[int(number)][0],CROP_LIST[int(number)][1],CROP_LIST[int(number)][2],CROP_LIST[int(number)][3])
            # capture = cropFrame(capture,CROP_LIST[int(number)])
        retval, image = cv2.imencode('.png',capture)
        # response = make_response(str(base64.b64encode(image)))
        # response.headers.set('Content-Type','image/png')
        return base64.b64encode(image)
    @app.route('/PlaceAtlasB.png')
    def placeAtlasB():
        return render_template("PlaceAtlasB.png")
    @app.route('/PlaceAtlasG.png')
    def placeAtlasGray():
        return render_template("PlaceAtlasG.png")
    @app.route('/PlaceAtlas/<color>')
    def placeAtlasColor(color):
        return render_template("PlaceAtlas"+str(color)+".png")
    @app.route('/PlaceAtlasBlue.png')
    def placeAtlasBlue():
        return render_template("PlaceAtlasBlue.png")
    @app.route('/PlaceAtlasRed.png')
    def placeAtlasRed():
        return render_template("PlaceAtlasRed.png")
    @app.route('/PlaceAtlasWhite.png')
    def placeAtlasWhite():
        return render_template("PlaceAtlasWhite.png")
    @app.route('/FinishFlag.png')
    def flag():
        return render_template("FinishFlag.png")
    @app.route('/PlaceAtlas.png')
    def placeAtlas():
        return render_template("PlaceAtlas.png")
    @app.route('/team/<color>')
    def setColor(color):
        for video in videoSource:
            video.team = color
        print("Team Colors Set to " + color)
        return "Team Colors Set"
    @app.route('/place.js')
    def script():
        return render_template("place.js")
    @app.route('/manage.js')
    def manage():
        return render_template("manage.js",obsMode=obsCamMode, readingData=not(stopCollection))
    @app.route('/BaiJam.ttf')
    def font():
        return render_template("BaiJam.ttf")
    @app.route('/jsonObj')
    def data():
        # print(jsonObj)
        return json.dumps([jsonObj,str(dataUpdated)])
    @app.route('/<number>/jsonObj')
    def camJson(number):
        # print(jsonObj)
        return json.dumps([jsonObj,str(dataUpdated)])
    @app.route('/dataUpdate')
    def updateData():
        global dataUpdated
        dataUpdated = True
        return "Message Received"
    @app.route('/inRace')
    def inRace():
        for video in videoSource:
            video.racing = 1
            video.finished = 0
        print("Put in Race")
        return "Put in Race"
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port="8000")


def runVideoData(*videos):
    listionary = np.tile(np.array([({})]),len(videos))
    print("Video Data Function Running")
    while True:
        if(stopCollection):
            print("I'm about to break")
            dataUpdated = False
            break
        if(UNLIMITED_POWER==False):
            time.sleep(0.02)
        for i in range(len(videos)):
            # I know this is very bad thread management
            # But it's pretty fast
            t1 = Thread(target=getVideoData, args=(videos[i],i,listionary))
            t1.start()
            # print(videoSource)
            # video = videoSource[i]
            # print(video)
            # print(type(videos[i]))
            t2 = Thread(target=updateVideoData(videos[i]))
            t2.start()
        global jsonObj
        jsonObj = json.dumps(listionary.tolist())
        # time.sleep(0.33333333)
def getVideoData(video,position,list):
    video.getCurrentFrame()
    list[int(position)]=({"name":video.name, "place":video.currentPlace,"finished":video.finished==1,"racing":video.racing==1,"team":video.team,"order":video.order,"sortByPlace":sortPlace})
def updateVideoData(video):
    video.updateFrame()
def checkCameras():
    manageCollectionFunction(False)
    borkedCameras=0
    i=0
    while True:
        print("Checking " + str(i))
        feed = None
        if(SYSTEM=="Windows"):
            feed = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        elif(SYSTEM=="Linux"):
            feed = cv2.VideoCapture(i, cv2.CAP_V4L2)
        else:
            feed = cv2.VideoCapture(i)
        if(not(feed.read()[0])):
            borkedCameras+=1
            print("Camera " + str(i) + " is borked")
            if(borkedCameras>=4):
                break
        else:
            cameraList.append(i)
            feed.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            print(f"Camera {i} has a resolution of {feed.read()[1].shape[1]} x {feed.read()[1].shape[0]}")
        cameraCaptureList.append(feed)
        i+=1
def manageCollectionFunction(p):
    global stopCollection
    if(stopCollection&p):
        stopCollection = False
        t1 = Thread(target=runVideoData, args=videoSource)
        t1.start()
        return
    stopCollection=True
def sortListByOrder(*list):
    newList=[]
    for l in list:
        newList.append(l)
    for i in range(len(newList)-1):
        if(newList[i].order>newList[i+1].order):
            temp=newList[i]
            newList[i]=newList[i+1]
            newList[i+1]=temp
    return newList
        
def setCameraSource(*list):
    # print(list[0])
    videoSource.clear()
    for cam in list[0]:
        print("Loading Camera " + str(cam[0])+" named " + cam[1])
        videoSource.append(videoDerive.VideoCap(cameraCaptureList[cam[0]],cam[1],cam[2]))
def setOBSCams(*list):
    global CROP_LIST
    global obsCamera
    videoSource.clear()
    for cam in list[0]:
        print("Loading Camera " + str(cam[0])+" named " + cam[1])
        video = videoDerive.VideoCap(obsCamera,cam[1],cam[2])
        video.crop = CROP_LIST[cam[0]]
        video.scale = 1
        videoSource.append(video)
def setVideoFileSource(*list):
    videoSource.clear()
    for cam in list:
        print("Loading File " + str(cam[0])+" named " + cam[1])
        videoSource.append(videoDerive.VideoCap(cv2.VideoCapture(cam[0]),cam[1],cam[2]))
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
main()