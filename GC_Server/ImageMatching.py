# OpenCV를 활용한 헤어스타일링 기능 코드
# 사용자 선택 png이미지를 합성하는 기능 수행

import numpy as np
import cv2
import sys
import urllib
import json
import base64
import requests
import logging
import io
from PIL import Image
import rgbdata as rgb
import ColorConverting as Colorcvt

facedetector = cv2.CascadeClassifier('static\opencv\haarcascade\haarcascade_frontalface_default.xml')

def startInit(originurl):
    #original = cv2.imread('static\opencv\image\original.jpg')
    resp = urllib.request.urlopen(originurl)
    original = np.asarray(bytearray(resp.read()), dtype="uint8")
    original = cv2.imdecode(original, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    originface = facedetector.detectMultiScale(gray, 1.3, 5)
    print("인식y좌표:"+str(originface[0][1])+"원본안면인식크기 width:"+str(originface[0][2])+" height:"+str(originface[0][3]))

    return originface

def startMatching():
    global encodingImage
    #request selected image
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.get('http://127.0.0.1:8080/selectedimage', headers=headers)
    dictdata = response.json()
    originurl = dictdata['origin']
    parsurl = dictdata['parsimg']
    userurl = dictdata['userimg']
    #colorname 변수 추가됨
    colorname = dictdata['colorname']
    print(colorname)
    #파싱이미지 png로드
    urlresp = urllib.request.urlopen(parsurl)
    parshair = np.asarray(bytearray(urlresp.read()), dtype="uint8")
    parshair = cv2.imdecode(parshair, cv2.IMREAD_UNCHANGED)
    #컬러선택됐으면 rgb데이터 로드
    if colorname != 'original' :
        #rgb data tuple형태로 (0,0,0)
        rgbtuple = rgb.find(colorname)
        #parshair 이미지 객체 변형 시키기445
        #parshair = 변형함수(rgbtuple) <--이런식으루
        parshair = Colorcvt.convertColor(parshair, rgbtuple)

    originface = startInit(originurl)
    #hair = cv2.imread('static\opencv\image\TestImage.png', -1)
    #matchingsnap = cv2.imread('static/opencv/image/testuserimg.jpg')
    encoded_data = userurl.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    matchingsnap = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    matchingsnap = cv2.flip(matchingsnap, 1)
    gray = cv2.cvtColor(matchingsnap, cv2.COLOR_BGR2GRAY)
    faces = facedetector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        overlayHair = changeSize(parshair, (w, h), (originface[0][2], originface[0][3]))

        hair_height, hair_width = overlayHair.shape[:2]
        y_position = originface[0][1]*(h/originface[0][3])
        # print(str(y)+":사용자얼굴인식y좌표->"+str(y_position))
        x = int(x-(hair_width-w)/2)
        y = int(y-y_position)
        #y = int(y-3*(y/5))
        #y = int(y-(hair_height-h)/4)
        w = hair_width
        h = hair_height

        hair_roi_color = matchingsnap[y:y + h, x:x + w]

        overlayImage(hair_roi_color, overlayHair)
    cv2.imwrite('result.jpg', matchingsnap)
    resultbase64 = Image.fromarray(matchingsnap.astype("uint8"))
    rawBytes = io.BytesIO()
    resultbase64.save(rawBytes, "PNG")
    rawBytes.seek(0)  # return to the start of the file
    encodingImage = base64.b64encode(rawBytes.read())
    return encodingImage

#파이썬코드만 테스트할때 썼음
def makesnap():
    #cam = cv2.VideoCapture(videoUrl)
    #cam = cv2.VideoCapture("http://192.168.137.170:8090/?action=stream")
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 30)
    ret, frame = cam.read()
    #frame = cv2.flip(frame, 1)
    #frame = cv2.transpose(frame) # 행렬 변경 
    matchingorigin = cv2.flip(frame, 1)   # 뒤집기
    cv2.imwrite('userimg.jpg', matchingorigin)
    cam.release()
    return matchingorigin

def changeSize(parshair, detectSize=(0,0), originsize=(0,0)):
    #사용자 얼굴이 더클때
    #if detectSize[0]>originsize[0] and detectSize[1]>originsize[1]:
    w = detectSize[0]/originsize[0]
    h = detectSize[1]/originsize[1]
    parshair = cv2.resize(parshair, None, fx=w, fy=h, interpolation=cv2.INTER_CUBIC)

    '''#사용자 얼굴이 더 작을때
    else:
        w = originsize[0]/detectSize[0]
        h = originsize[1]/detectSize[1]
        #print ('폭:'+str(w)+'너비:'+str(h))
        parshair = cv2.resize(parshair, None, fx=w, fy=h, interpolation=cv2.INTER_AREA)
    '''
    return parshair

# Image Overlay test1
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