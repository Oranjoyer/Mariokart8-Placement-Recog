from flask import Flask,render_template,request
import videoDerive
from threading import Thread
import cv2
import json
import numpy as np
import time
jsonObj = ""
UNLIMITED_POWER=True
def main():
    
    app = Flask(__name__)
    videoSource = []
    for i in range(4):
        videoSource.append(videoDerive.VideoCap(cv2.VideoCapture(0),"Video"+str(i)))
    t1 = Thread(target=runVideoData, args=videoSource)
    t1.start()
    @app.route('/', methods=['Get','Post'])
    def page():
        if request.method == 'GET':
            data = request.data
            print(str(data) + " I'm Data")
        return render_template('index.html', jsonObj=jsonObj)
    
    @app.route('/PlaceAtlasB.png')
    def placeAtlas():
        return render_template("PlaceAtlasB.png")
    
    @app.route('/place.js')
    def script():
        return render_template("place.js")
    
    @app.route('/jsonObj')
    def data():
        return jsonObj
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port="8000")


def runVideoData(*videos):
    listionary = np.tile(np.array([({})]),len(videos))
    while True:
        if(UNLIMITED_POWER==False):
            time.sleep(0.066666)
        for i in range(len(videos)):
            t2 = Thread(target=getVideoData, args=(videos[i],i,listionary))
            t2.start()
        global jsonObj
        jsonObj = json.dumps(listionary.tolist())
def getVideoData(video,position,list):
    video.getCurrentFrame()
    # print(list[position])
    list[int(position)]=({"name":str(video.name), "place":str(video.currentPlace),"finished":str(video.racing==0)})
    
    
main()