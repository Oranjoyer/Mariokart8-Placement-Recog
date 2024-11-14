from flask import Flask,render_template,request,make_response
import videoDerive
from threading import Thread
import cv2
import json
import numpy as np
import time
import base64
jsonObj = ""
cameraList=[]
UNLIMITED_POWER=True
stopCollection=True
videoSource=[]
cameraCaptureList=[]
def main():
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
    
    def cameraSpot():
        return render_template('places.html')
    @app.route('/manage', methods=["POST","GET"])
    def management():
        return render_template("manage.html")
    @app.route('/sendCams/<theThing>',methods=['POST','GET'])
    def sendCams(theThing):
        if(request.method=='POST'):
            cameraList= json.decoder(theThing)
        if(request.method=='GET'):
            cameraList=json.loads(str(theThing))
            setCameraSource(cameraList)
            return "Data Pulled"
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
    @app.route("/camList")
    def cameras():
        if(len(cameraList)==0):
            checkCameras()
        return json.dumps(cameraList)
    @app.route("/checkCams")
    def checkCams():
        checkCameras()
    @app.route("/camImage/<number>")
    def cameraImg(number):
        ret, capture = cameraCaptureList[int(number)].read()
        retval, image = cv2.imencode('.png',capture)
        # response = make_response(str(base64.b64encode(image)))
        # response.headers.set('Content-Type','image/png')
        return base64.b64encode(image)
        
    # @app.route("/startCollection")
    # def startCollection():
    #     manageCollectionFunction(True)
    # @app.route("/stopCollection")
    # def stopCollection():
    #     manageCollectionFunction(False)
    #     print("Data Collection Stopped")
    #     return "Data Collection Stopped"
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
        return render_template("manage.js")
    @app.route('/newRodin.otf')
    def font():
        return render_template("newRodin.otf")
    @app.route('/jsonObj')
    def data():
        # print(jsonObj)
        return jsonObj
    @app.route('/<number>/jsonObj')
    def camJson(number):
        # print(jsonObj)
        return jsonObj
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
            break
        if(UNLIMITED_POWER==False):
            time.sleep(0.03333333)
        for i in range(len(videos)):
            # I know this is very bad thread management
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
    # print("Stuff Running")
    # print(video)
    video.getCurrentFrame()
    # print(list[position])
    list[int(position)]=({"name":video.name, "place":video.currentPlace,"finished":video.finished==1,"racing":video.racing==1,"team":video.team})
def updateVideoData(video):
    video.updateFrame()
def checkCameras():
    manageCollectionFunction(False)
    borkedCameras=0
    i=0
    while True:
        print("Checking " + str(i))
        feed = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if(not(feed.read()[0])):
            borkedCameras+=1
            print("Camera " + str(i) + " is borked")
            if(borkedCameras>=2):
                break
        else:
            cameraList.append(i)
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
def setCameraSource(*list):
    # print(list[0])
    videoSource.clear()
    for cam in list[0]:
        print("Loading Camera " + str(cam[0])+" named " + cam[1])
        videoSource.append(videoDerive.VideoCap(cameraCaptureList[cam[0]],cam[1]))

main()