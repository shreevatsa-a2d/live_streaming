
from flask import Flask, render_template, Response
import threading
import cv2
import os
from time import sleep


app = Flask(__name__)
frame = bytearray()

# !npm install -g localtunnel

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    global frame
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global frame
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def startStreaming():
    global frame
    while True:
        isclosed=0
        video = cv2.VideoCapture("input_video.mp4")
        while(video.isOpened()):
            success, image = video.read()

            if success:
                ret, jpeg = cv2.imencode('.jpg', image)
                frame = jpeg.tobytes()
                # if cv2.waitKey(1) == 27:
                #     isclosed=1
                #     break
            else:
                print("No video")
                break
        if isclosed:
            break

       
    video.release()
    cv2.destroyAllWindows()

def runServer():
    sleep(2)
    print(os.system('lt --port 5000'))

if __name__ == '__main__':
    p = threading.Thread(target=startStreaming)
    p.start()
    p = threading.Thread(target=runServer)
    p.start()
    app.run(port=5000)