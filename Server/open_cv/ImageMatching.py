# facerecognition.py
import numpy as np
import cv2
import requests
import json

url = "http://localhost:5000/ImageMatching"
data = {'msg': '이미지 매칭중'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

facedetector = cv2.CascadeClassifier('Server\open_cv\haarcascade\haarcascade_frontalface_default.xml')
hair = cv2.imread('Server\open_cv\image\TestImage.png', -1)

original = cv2.imread('Server\open_cv\original.jpg')
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
originface = facedetector.detectMultiScale(gray, 1.3, 5)
print("원본안면인식크기 width:"+str(originface[0][2])+" height:"+str(originface[0][3]))

cam = cv2.VideoCapture("http://192.168.137.225:8090/?action=stream")
cam.set(cv2.CAP_PROP_FPS, 30)

def changeSize(hair, detectSize=(0,0)):
    w = detectSize[0]/originface[0][2]
    h = detectSize[1]/originface[0][3]

    changeHair = cv2.resize(hair, None, fx=w, fy=h, interpolation=cv2.INTER_CUBIC)

    return changeHair

# Image Overlay
def overlayImage(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape
    rows, cols, _ = src.shape
    y, x = pos[0], pos[1]

    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


while (True):
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        overlayHair = changeSize(hair, (w, h))

        hair_height, hair_width = overlayHair.shape[:2]

        x = int(x-(hair_width-w)/2)
        y = int(y-2*y/5)
        #y = int(y-(hair_height-h)/4)
        w = hair_width
        h = hair_height

        hair_roi_color = frame[y:y + h, x:x + w]

        overlayImage(hair_roi_color, overlayHair)

    cv2.imshow('frame', frame)
    requests.post(url, data=json.dumps(data), headers=headers)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
