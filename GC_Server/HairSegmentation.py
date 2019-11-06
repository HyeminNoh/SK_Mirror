# 20190808 수정본
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

def makeresult(originurl, hair_type):
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,0.0)

    pointx = 0
    #haarcasecade호출
    faceCascade = cv2.CascadeClassifier('static\opencv\haarcascade\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier("static\opencv\haarcascade\haarcascade_eye.xml")

    # 이미지읽기 image는 추출할 이미지
    # image = cv2.imread('GC_Server\static\images\hair5.png', -1)
    resp = urllib.request.urlopen(originurl)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # 투명한 배경 로드
    bgimage = cv2.imread("static/images/bg.png", -1)
    # 원본이미지 폭, 너비 구하기
    height, width, channels = img.shape
     
    # 이미지크기변경
    # image = cv2.resize(image, dsize=(500, 500), interpolation=cv2.INTER_AREA)
    # bgimage = cv2.resize(bgimage, dsize=(500, 500), interpolation=cv2.INTER_AREA)
     
    #투명한배경이미지를 원본이미지 크기로 변경
    bgimage = cv2.resize(bgimage, dsize=(width, height), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

   #-----------배경제거-----------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)#이미지에서 사람윤곽선추출
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #추출된 윤곽선 기준으로 다각형생성
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #배경영역추출
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER) #팽창
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER) #침식
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0) #잡음제거
    mask_stack = np.dstack([mask]*3)   #알파채널 마스크생성

    #배경영역 흰색
    mask_stack  = mask_stack.astype('float32') / 255.0 #배경부분 형식변경
    img         = img.astype('float32') / 255.0 # 사람부분이미지 형식변경

    masked = (mask_stack * img) + ((1-mask_stack) * 1) #배경부분을 흰색으로 지정
    masked = (masked * 255).astype('uint8') # 이미지를 unit8형식으로 전환

    # 알파채널변경
    c_red, c_green, c_blue = cv2.split(img) #사람부분 이미지의 알파값추가

    # 배경 없애기
    img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0)) # 배경부분을 알파값으로변경

    # 사람영살만 저장
    cv2.imwrite('reback.png', img_a*255)
    #--------------------헤어추출-----------------------------
    #사람영역만 저장된 이미지 알파값포함 로드
    hairimg = cv2.imread('reback.png',-1)
    gray = cv2.cvtColor(hairimg, cv2.COLOR_BGR2GRAY)

    #알파값으로 얼굴인식 불가로 포맷 형식변경
    gray = np.array(gray, dtype='uint8')

    #faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    faces = faceCascade.detectMultiScale(gray, 1.3, 5, 0)
    print
    "Face Count : {0}".format(len(faces))

    #얼굴인식 좌표
    for (x, y, w, h) in faces:
        #pointx = int((x+w+x)/3)
        #pointx2 = int((x+w+x)/2.5)
        # pointx4 = int((x+w+x)/1.55)

        #우측 헤어 추출 기준 x좌표(얼굴인식 넓이끝)
        pointx = int((x+w))

        #좌우 추출 기준 y좌표(얼굴인식 높이 1/3지점)
        pointy = int((y+h)/1.55)


        #얼굴크기
        #cv2.rectangle(te, (x, y), (x+w, y + h), (0, 255, 0), 2)

        #머리위치까지 확장
        #cv2.rectangle(masked, (x-15, y-15), (x + w+15, y + h), (0, 255, 0), 2)

        face_gray = gray[y:y + h, x:x + w]
        face_color = hairimg[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(face_gray, 1.1, 3)
        for (ex, ey, ew, eh) in eyes:
            p = int((ex + ew + ex) / 2)
            q = int((ey + ey + eh) / 2)
            cv2.circle(face_color, (p, q), 15 ,(255, 255, 255), -1) #눈코입부분 흰색 원생성



    #함수 실행시 필요한 데이터 hairimg(배경제거된이미지), masked(배경이흰색인 이미지)
    if hair_type is "short" or hair_type=="short":
        shortcut(hairimg, masked, bgimage, pointx, pointy, x, y)
    elif hair_type is "long" or hair_type=="long":
        longcut(hairimg, masked, bgimage, pointx, pointy, x, y)
    elif hair_type is "middle" or hair_type=="middle":
        middlecut(hairimg, masked, bgimage, pointx, pointy, x, y)
         
def shortcut(hairimg, masked, bgimage, pointx, pointy, x, y):
    # 20-119까지 100개 포인트 머리상단
    for i in range(0, 150):
        toppixcolor = hairimg[y - 35, x + i] #배경이 제거된 이미지기반 포인트로 컬러값추출 x,y 는 얼굴인식의 시작 가로와높이값
        toppixel = np.uint8([[toppixcolor]])
        topcolorspace = cv2.cvtColor(toppixel, cv2.IMREAD_COLOR)
        globals()['topcolor{}'.format(i)] = topcolorspace[0][0] #변수명을 topcolor0~199까지 동적할당후 컬러값입력

    # 머리상단 포인트 범위설정. 동적할당된 topcolor0~199까지의 컬러를 +-10만큼 범위조정
    for i2 in range(0, 150):
        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['topcolor{}'.format(i2)][0]
        two = globals()['topcolor{}'.format(i2)][1]
        three = globals()['topcolor{}'.format(i2)][2]
        # print(one)
        globals()['toplow{}'.format(i2)] = np.array([one - 10, two - 10, three - 10])
        globals()['tophigh{}'.format(i2)] = np.array([one + 10, two + 10, three + 10])

    # 머리 상단 포인트기준 마스크
    for l in range(0, 150):
        #toplow~tophigh 컬러 기반으로 masked(흰배경이미지)에서 해당 컬러값범위 영역 추출. hairimg는 알파값포함 4자리의 컬러라 마스크 생성불가
        globals()['topmask{}'.format(l)] = cv2.inRange(masked, globals()['toplow{}'.format(l)], globals()['tophigh{}'.format(l)])

    # 마스크 통합
    img_mask = topmask0 |topmask1 |topmask2 |topmask3 |topmask4 |topmask5 |topmask6 |topmask7 |topmask8 |topmask9 |topmask10 |topmask11 |topmask12 |topmask13 |topmask14 |topmask15 |topmask16 |topmask17 |topmask18 |topmask19 | topmask20 | topmask21 | topmask22 | topmask23 | topmask24 | topmask25 | topmask26 | topmask27 | topmask28 | topmask29 | topmask30 | topmask31 | topmask32 | topmask33 | topmask34 | topmask35 | topmask36 | topmask37 | topmask38 | topmask39 | topmask40 | topmask41 | topmask42 | topmask43 | topmask44 | topmask45 | topmask46 | topmask47 | topmask48 | topmask49 | topmask50 | topmask51 | topmask52 | topmask53 | topmask54 | topmask55 | topmask56 | topmask57 | topmask58 | topmask59 | topmask60 | topmask61 | topmask62 | topmask63 | topmask64 | topmask65 | topmask66 | topmask67 | topmask68 | topmask69 | topmask70 | topmask71 | topmask72 | topmask73 | topmask74 | topmask75 | topmask76 | topmask77 | topmask78 | topmask79 | topmask80 | topmask81 | topmask82 | topmask83 | topmask84 | topmask85 | topmask86 | topmask87 | topmask88 | topmask89 | topmask90 | topmask91 | topmask92 | topmask93 | topmask94 | topmask95 | topmask96 | topmask97 | topmask98 | topmask99 | topmask100 | topmask101 | topmask102 | topmask103 | topmask104 | topmask105 | topmask106 | topmask107 | topmask108 | topmask109 | topmask110 | topmask111 | topmask112 | topmask113 | topmask114 | topmask115 | topmask116 | topmask117 | topmask118 | topmask119| topmask120| topmask121| topmask122| topmask123| topmask124| topmask125| topmask126| topmask127| topmask128| topmask129| topmask130| topmask131| topmask132| topmask133| topmask134| topmask135| topmask136| topmask137| topmask138| topmask139| topmask140| topmask141| topmask142| topmask143| topmask144| topmask145| topmask146| topmask147| topmask148| topmask149

    #hairimg(사람만있는이미지)에서 통합된 마스크를 씌워 겹치는 영역 추출 겹치지 않은 영역은 검정으로 추출
    img_result = cv2.bitwise_and(hairimg, hairimg, mask=img_mask)

    #b_channel, g_channel, r_channel = cv2.split(img_result) 해당줄은 추출전 배경제거에서 사용되어 지움

    #alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image. 해당줄은 추출전 배경제거에서 사용되어 지움

    #img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel)) 해당줄은 추출전 배경제거에서 사용되어 지움

    #추출된 이미지의 가로 세로 채널수를 구함
    rows, cols, channels = img_result.shape

    #빈 png파일의 가로새로크기를 구함
    roi = bgimage[0:rows, 0:cols]

    #추출된 헤어이미지를 그레이스케일로 변환
    img2gray = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)

    #변환된 이미지를 이진화
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    #이진화된 영상을 반전
    mask_inv = cv2.bitwise_not(mask)

    #추출된 이미지와 반전된 이미지 연산
    img1_fg = cv2.bitwise_and(img_result, img_result, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    dst = cv2.add(img1_fg, img2_bg)

    bgimage[0:rows, 0:cols] = dst

    cv2.imwrite("segmentation_result.png", dst)
    resultbase64 = Image.fromarray(dst.astype("uint8"))
    rawBytes = io.BytesIO()
    resultbase64.save(rawBytes, "PNG")
    rawBytes.seek(0)  # return to the start of the file
    encodingImage = base64.b64encode(rawBytes.read())

    return encodingImage

def middlecut(hairimg, masked, bgimage, pointx, pointy, x, y):
    # 0-120까지 100개 포인트 머리상단
    for i in range(0, 120):
        toppixcolor = hairimg[y - 35, x + i + 20]#숏컷과 동일
        toppixel = np.uint8([[toppixcolor]])
        topcolorspace = cv2.cvtColor(toppixel, cv2.IMREAD_COLOR)
        # print(topcolorspace)

        globals()['topcolor{}'.format(i)] = topcolorspace[0][0]

    # 0~249까지 250개 우측포인트
    for j in range(0, 125):
        rightpixcolor = hairimg[pointy + j, pointx]  #우측 헤어 추출 기준 x좌표(얼굴인식 넓이끝)와 좌우 추출 기준 y좌표(얼굴인식 높이 1/3지점)을 기반으로 우측시작지점부터 추출
        rightpixel = np.uint8([[rightpixcolor]])
        rightcolorspace = cv2.cvtColor(rightpixel, cv2.IMREAD_COLOR)
        globals()['rightcolor{}'.format(j)] = rightcolorspace[0][0]
    # print(rightcolor6)

    # 0~249까지 250개 좌측포인트
    for k in range(0, 125):
        leftpixcolor = hairimg[pointy + k, x] #x의 얼굴인식의 가로값과 얼굴인식높이 1/3지점부터 추출
        leftpixel = np.uint8([[leftpixcolor]])
        leftcolorspace = cv2.cvtColor(leftpixel, cv2.IMREAD_COLOR)
        globals()['leftcolor{}'.format(k)] = leftcolorspace[0][0]

    # 머리상단 포인트 범위설정
    for i2 in range(0, 120):
        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['topcolor{}'.format(i2)][0]
        two = globals()['topcolor{}'.format(i2)][1]
        three = globals()['topcolor{}'.format(i2)][2]
        # print(one)
        globals()['toplow{}'.format(i2)] = np.array([one - 10, two - 10, three - 10])
        globals()['tophigh{}'.format(i2)] = np.array([one + 10, two + 10, three + 10])
    # 오른쪽 머리 포인트
    for j2 in range(0, 125):
        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['rightcolor{}'.format(j2)][0]
        two = globals()['rightcolor{}'.format(j2)][1]
        three = globals()['rightcolor{}'.format(j2)][2]
        # print(one)
        globals()['rightlow{}'.format(j2)] = np.array([one - 10, two - 10, three - 10])
        globals()['righthigh{}'.format(j2)] = np.array([one + 10, two + 10, three + 10])
    # print(righthigh2)
    # 왼쪽 머리 포인트
    for k2 in range(0, 125):
        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['leftcolor{}'.format(k2)][0]
        two = globals()['leftcolor{}'.format(k2)][1]
        three = globals()['leftcolor{}'.format(k2)][2]
        # print(one)
        globals()['leftlow{}'.format(k2)] = np.array([one - 10, two - 10, three - 10])
        globals()['lefthigh{}'.format(k2)] = np.array([one + 10, two + 10, three + 10])
    # print(lefthigh3)

    # 머리 상단 포인트기준 마스크
    for l in range(0, 120):
        globals()['topmask{}'.format(l)] = cv2.inRange(masked, globals()['toplow{}'.format(l)],
                                                       globals()['tophigh{}'.format(l)])
    # 머리 좌 우 포인트 기준 마스크
    for m in range(0, 125):
        globals()['leftmask{}'.format(m)] = cv2.inRange(masked, globals()['leftlow{}'.format(m)],
                                                        globals()['lefthigh{}'.format(m)])
        globals()['rightmask{}'.format(m)] = cv2.inRange(masked, globals()['rightlow{}'.format(m)],
                                                         globals()['righthigh{}'.format(m)])

    # 마스크 통합
    img_mask =  topmask0 | topmask1 | topmask2 | topmask3 | topmask4 |  topmask5 | topmask6 | topmask7 | topmask8 | topmask9 | topmask10 | topmask11 | topmask12 |topmask13 | topmask14 | topmask15 | topmask16 | topmask17 | topmask18 | topmask19 | topmask20 | topmask21 | topmask22 | topmask23 | topmask24 | topmask25 | topmask26 | topmask27 | topmask28 | topmask29 | topmask30 | topmask31 | topmask32 | topmask33 | topmask34 | topmask35 | topmask36 | topmask37 | topmask38 | topmask39 | topmask40 | topmask41 | topmask42 | topmask43 | topmask44 | topmask45 | topmask46 | topmask47 | topmask48 | topmask49 | topmask50 | topmask51 | topmask52 | topmask53 | topmask54 | topmask55 | topmask56 | topmask57 | topmask58 | topmask59 | topmask60 | topmask61 | topmask62 | topmask63 | topmask64 | topmask65 | topmask66 | topmask67 | topmask68 | topmask69 | topmask70 | topmask71 | topmask72 | topmask73 | topmask74 | topmask75 | topmask76 | topmask77 | topmask78 | topmask79 |topmask80 | topmask81 | topmask82 | topmask83 | topmask84 | topmask85 | topmask86 | topmask87 | topmask88 | topmask89 | topmask90 | topmask91 | topmask92 | topmask93 | topmask94 | topmask95 | topmask96 | topmask97 | topmask98 | topmask99 | topmask100 | topmask101 | topmask102 | topmask103 | topmask104 | topmask105 | topmask106 | topmask107 | topmask108 | topmask109 | topmask110 | topmask111 | topmask112 | topmask113 | topmask114 | topmask115 | topmask116 | topmask117 | topmask118 | topmask119| leftmask5 | leftmask6 | leftmask7 | leftmask8 | leftmask9 | leftmask10 | leftmask11 | leftmask12 | leftmask13 | leftmask14 | leftmask15 | leftmask16 | leftmask17 | leftmask18 | leftmask19 | leftmask20 | leftmask21 | leftmask22 | leftmask23 | leftmask24 | leftmask25 | leftmask26 | leftmask27 | leftmask28 | leftmask29 | leftmask30 | leftmask31 | leftmask32 | leftmask33 | leftmask34 | leftmask35 | leftmask36 | leftmask37 | leftmask38 | leftmask39 | leftmask40 | leftmask41 | leftmask42 | leftmask43 | leftmask44 | leftmask45 | leftmask46 | leftmask47 | leftmask48 | leftmask49 | leftmask50 | leftmask51 | leftmask52 | leftmask53 | leftmask54 | leftmask55 | leftmask56 | leftmask57 | leftmask58 | leftmask59 | leftmask60 | leftmask61 | leftmask62 | leftmask63 | leftmask64 | leftmask65 | leftmask66 | leftmask67 | leftmask68 | leftmask69 | leftmask70 | leftmask71 | leftmask72 | leftmask73 | leftmask74 | leftmask75 | leftmask76 | leftmask77 | leftmask78 | leftmask79 | leftmask80 | leftmask81 | leftmask82 | leftmask83 | leftmask84 | leftmask85 | leftmask86 | leftmask87 | leftmask88 | leftmask89 | leftmask90 | leftmask91 | leftmask92 | leftmask93 | leftmask94 | leftmask95 | leftmask96 | leftmask97 | leftmask98 | leftmask99 | leftmask100 | leftmask101 | leftmask102 | leftmask103 | leftmask104 | leftmask105 | leftmask106 | leftmask107 | leftmask108 | leftmask109 | leftmask110 | leftmask111 | leftmask112 | leftmask113 | leftmask114 | leftmask115 | leftmask116 | leftmask117 | leftmask118 | leftmask119 | leftmask120 | leftmask121 | leftmask122 | leftmask123 | leftmask124 | rightmask5 | rightmask6 | rightmask7 | rightmask8 | rightmask9 | rightmask10 | rightmask11 | rightmask12 | rightmask13 | rightmask14 | rightmask15 | rightmask16 | rightmask17 | rightmask18 | rightmask19 | rightmask20 | rightmask21 | rightmask22 | rightmask23 | rightmask24 | rightmask25 | rightmask26 | rightmask27 | rightmask28 | rightmask29 | rightmask30 | rightmask31 | rightmask32 | rightmask33 | rightmask34 | rightmask35 | rightmask36 | rightmask37 | rightmask38 | rightmask39 | rightmask40 | rightmask41 | rightmask42 | rightmask43 | rightmask44 | rightmask45 | rightmask46 | rightmask47 | rightmask48 | rightmask49 | rightmask50 | rightmask51 | rightmask52 | rightmask53 | rightmask54 | rightmask55 | rightmask56 | rightmask57 | rightmask58 | rightmask59 | rightmask60 | rightmask61 | rightmask62 | rightmask63 | rightmask64 | rightmask65 | rightmask66 | rightmask67 | rightmask68 | rightmask69 | rightmask70 | rightmask71 | rightmask72 | rightmask73 | rightmask74 | rightmask75 | rightmask76 | rightmask77 | rightmask78 | rightmask79 | rightmask80 | rightmask81 | rightmask82 | rightmask83 | rightmask84 | rightmask85 | rightmask86 | rightmask87 | rightmask88 | rightmask89 | rightmask90 | rightmask91 | rightmask92 | rightmask93 | rightmask94 | rightmask95 | rightmask96 | rightmask97 | rightmask98 | rightmask99 | rightmask100 | rightmask101 | rightmask102 | rightmask103 | rightmask104 | rightmask105 | rightmask106 | rightmask107 | rightmask108 | rightmask109 | rightmask110 | rightmask111 | rightmask112 | rightmask113 | rightmask114 | rightmask115 | rightmask116 | rightmask117 | rightmask118 | rightmask119 | rightmask120 | rightmask121 | rightmask122 | rightmask123 | rightmask124| rightmask0 | rightmask1 | rightmask2 | rightmask3 | rightmask4 | leftmask0 | leftmask1 | leftmask2 | leftmask3 | leftmask4

    img_result = cv2.bitwise_and(hairimg, hairimg, mask=img_mask)

    # b_channel, g_channel, r_channel = cv2.split(img_result)

    # alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.

    img_BGRA = img_result  # cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    rows, cols, channels = img_BGRA.shape

    roi = bgimage[0:rows, 0:cols]

    img2gray = cv2.cvtColor(img_BGRA, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_fg = cv2.bitwise_and(img_BGRA, img_BGRA, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    dst = cv2.add(img1_fg, img2_bg)

    bgimage[0:rows, 0:cols] = dst

    cv2.imwrite("segmentation_result.png", dst)
    resultbase64 = Image.fromarray(dst.astype("uint8"))
    rawBytes = io.BytesIO()
    resultbase64.save(rawBytes, "PNG")
    rawBytes.seek(0)  # return to the start of the file
    encodingImage = base64.b64encode(rawBytes.read())

    return encodingImage

def longcut(hairimg, masked, bgimage, pointx, pointy, x, y):
    #20-119까지 100개 포인트 머리상단
    for i in range(0, 110):
        toppixcolor = hairimg[y-35, x + i + 20]
        toppixel = np.uint8([[toppixcolor]])
        topcolorspace = cv2.cvtColor(toppixel, cv2.IMREAD_COLOR)
        globals()['topcolor{}'.format(i)] = topcolorspace[0][0]

    #0~249까지 250개 우측포인트
    for j in range(0, 250):
        rightpixcolor = hairimg[pointy+j, pointx]
        rightpixel = np.uint8([[rightpixcolor]])
        rightcolorspace = cv2.cvtColor(rightpixel, cv2.IMREAD_COLOR)
        globals()['rightcolor{}'.format(j)] = rightcolorspace[0][0]
    #print(rightcolor6)

    #0~249까지 250개 좌측포인트
    for k in range(0, 250):
        leftpixcolor = hairimg[pointy+k, x]
        leftpixel = np.uint8([[leftpixcolor]])
        leftcolorspace = cv2.cvtColor(leftpixel, cv2.IMREAD_COLOR)
        globals()['leftcolor{}'.format(k)] = leftcolorspace[0][0]

    #머리상단 포인트 범위설정
    for i2 in range(0, 110):

       # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['topcolor{}'.format(i2)][0]
        two = globals()['topcolor{}'.format(i2)][1]
        three = globals()['topcolor{}'.format(i2)][2]
        #print(one)
        globals()['toplow{}'.format(i2)] = np.array([one - 10, two - 10, three - 10])
        globals()['tophigh{}'.format(i2)] = np.array([one + 10, two + 10, three + 10])
    #오른쪽 머리 포인트
    for j2 in range(0, 250):

        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['rightcolor{}'.format(j2)][0]
        two = globals()['rightcolor{}'.format(j2)][1]
        three = globals()['rightcolor{}'.format(j2)][2]
        # print(one)
        globals()['rightlow{}'.format(j2)] = np.array([one - 10, two - 10, three - 10])
        globals()['righthigh{}'.format(j2)] = np.array([one + 10, two + 10, three + 10])
    #print(righthigh2)
    #왼쪽 머리 포인트
    for k2 in range(0, 250):

        # print(globals()['topcolor{}'.format(i2)][0])
        one = globals()['leftcolor{}'.format(k2)][0]
        two = globals()['leftcolor{}'.format(k2)][1]
        three = globals()['leftcolor{}'.format(k2)][2]
        # print(one)
        globals()['leftlow{}'.format(k2)] = np.array([one - 10, two - 10, three - 10])
        globals()['lefthigh{}'.format(k2)] = np.array([one + 10, two + 10, three + 10])
    #print(lefthigh3)

    # 머리 상단 포인트기준 마스크
    for l in range(0, 110):
        globals()['topmask{}'.format(l)] = cv2.inRange(masked, globals()['toplow{}'.format(l)], globals()['tophigh{}'.format(l)])
    #머리 좌 우 포인트 기준 마스크
    for m in range(0, 250):
        globals()['leftmask{}'.format(m)] = cv2.inRange(masked, globals()['leftlow{}'.format(m)], globals()['lefthigh{}'.format(m)])
        globals()['rightmask{}'.format(m)] = cv2.inRange(masked, globals()['rightlow{}'.format(m)], globals()['righthigh{}'.format(m)])

    #img_mask = globals()['topmask{}'.format(0)] | globals()['leftmask{}'.format(0)] | globals()['rightmask{}'.format(0)]

    #마스크 통합
    img_mask =topmask0|topmask1|topmask2|topmask3|topmask4|topmask5|topmask6|topmask7|topmask8|topmask9|topmask10|topmask11|topmask12|topmask13|topmask14|topmask15|topmask16|topmask17|topmask18|topmask19|topmask20|topmask21|topmask22|topmask23|topmask24|topmask25|topmask26|topmask27|topmask28|topmask29|topmask30|topmask31|topmask32|topmask33|topmask34|topmask35|topmask36|topmask37|topmask38|topmask39|topmask40 |topmask41 |topmask42 |topmask43 |topmask44 |topmask45 |topmask46 |topmask47 |topmask48 |topmask49 |topmask50 |topmask51 |topmask52 |topmask53 |topmask54 |topmask55 |topmask56 |topmask57 |topmask58 |topmask59 |topmask60 |topmask61 |topmask62 |topmask63 |topmask64 |topmask65 |topmask66 |topmask67 |topmask68 |topmask69 |topmask70 |topmask71 |topmask72 |topmask73 |topmask74 |topmask75 |topmask76 |topmask77 |topmask78 |topmask79 |topmask80 |topmask81 |topmask82 |topmask83 |topmask84 |topmask85 |topmask86 |topmask87 |topmask88 |topmask89 |topmask90 |topmask91 |topmask92 |topmask93 |topmask94 |topmask95 |topmask96 |topmask97 |topmask98 |topmask99 |topmask100 |topmask101 |topmask102 |topmask103 |topmask104 |topmask105 |topmask106 |topmask107 |topmask108 |topmask109 | leftmask0| leftmask1| leftmask2| leftmask3| leftmask4| leftmask5| leftmask6| leftmask7| leftmask8| leftmask98| leftmask10| leftmask11| leftmask12| leftmask13| leftmask14| leftmask15| leftmask16| leftmask17| leftmask18| leftmask19 | leftmask20 |leftmask21 |leftmask22 |leftmask23 |leftmask24 |leftmask25 |leftmask26 |leftmask27 |leftmask28 |leftmask29 |leftmask30 |leftmask31 |leftmask32 |leftmask33 |leftmask34 |leftmask35 |leftmask36 |leftmask37 |leftmask38 |leftmask39 |leftmask40 |leftmask41 |leftmask42 |leftmask43 |leftmask44 |leftmask45 |leftmask46 |leftmask47 |leftmask48 |leftmask49 |leftmask50 |leftmask51 |leftmask52 |leftmask53 |leftmask54 |leftmask55 |leftmask56 |leftmask57 |leftmask58 |leftmask59 |leftmask60 |leftmask61 |leftmask62 |leftmask63 |leftmask64 |leftmask65 |leftmask66 |leftmask67 |leftmask68 |leftmask69 |leftmask70 |leftmask71 |leftmask72 |leftmask73 |leftmask74 |leftmask75 |leftmask76 |leftmask77 |leftmask78 |leftmask79 |leftmask80 |leftmask81 |leftmask82 |leftmask83 |leftmask84 |leftmask85 |leftmask86 |leftmask87 |leftmask88 |leftmask89 |leftmask90 |leftmask91 |leftmask92 |leftmask93 |leftmask94 |leftmask95 |leftmask96 |leftmask97 |leftmask98 |leftmask99 |leftmask100 |leftmask101 |leftmask102 |leftmask103 |leftmask104 |leftmask105 |leftmask106 |leftmask107 |leftmask108 |leftmask109 |leftmask110 |leftmask111 |leftmask112 |leftmask113 |leftmask114 |leftmask115 |leftmask116 |leftmask117 |leftmask118 |leftmask119 |leftmask120 |leftmask121 |leftmask122 |leftmask123 |leftmask124 |leftmask125 |leftmask126 |leftmask127 |leftmask128 |leftmask129 |leftmask130 |leftmask131 |leftmask132 |leftmask133 |leftmask134 |leftmask135 |leftmask136 |leftmask137 |leftmask138 |leftmask139 |leftmask140 |leftmask141 |leftmask142 |leftmask143 |leftmask144 |leftmask145 |leftmask146 |leftmask147 |leftmask148 |leftmask149 |leftmask150 |leftmask151 |leftmask152 |leftmask153 |leftmask154 |leftmask155 |leftmask156 |leftmask157 |leftmask158 |leftmask159 |leftmask160 |leftmask161 |leftmask162 |leftmask163 |leftmask164 |leftmask165 |leftmask166 |leftmask167 |leftmask168 |leftmask169 |leftmask170 |leftmask171 |leftmask172 |leftmask173 |leftmask174 |leftmask175 |leftmask176 |leftmask177 |leftmask178 |leftmask179 |leftmask180 |leftmask181 |leftmask182 |leftmask183 |leftmask184 |leftmask185 |leftmask186 |leftmask187 |leftmask188 |leftmask189 |leftmask190 |leftmask191 |leftmask192 |leftmask193 |leftmask194 |leftmask195 |leftmask196 |leftmask197 |leftmask198 |leftmask199 |leftmask200 |leftmask201 |leftmask202 |leftmask203 |leftmask204 |leftmask205 |leftmask206 |leftmask207 |leftmask208 |leftmask209 |leftmask210 |leftmask211 |leftmask212 |leftmask213 |leftmask214 |leftmask215 |leftmask216 |leftmask217 |leftmask218 |leftmask219 |leftmask220 |leftmask221 |leftmask222 |leftmask223 |leftmask224 |leftmask225 |leftmask226 |leftmask227 |leftmask228 |leftmask229 |leftmask230 |leftmask231 |leftmask232 |leftmask233 |leftmask234 |leftmask235 |leftmask236 |leftmask237 |leftmask238 |leftmask239 |leftmask240 |leftmask241 |leftmask242 |leftmask243 |leftmask244 |leftmask245 |leftmask246 |leftmask247 |leftmask248 |leftmask249 |rightmask0|rightmask1|rightmask2|rightmask3|rightmask4|rightmask5|rightmask6|rightmask7|rightmask8|rightmask9|rightmask10|rightmask11|rightmask12|rightmask13|rightmask14|rightmask15|rightmask16|rightmask17|rightmask18|rightmask19|rightmask20 |rightmask21 |rightmask22 |rightmask23 |rightmask24 |rightmask25 |rightmask26 |rightmask27 |rightmask28 |rightmask29 |rightmask30 |rightmask31 |rightmask32 |rightmask33 |rightmask34 |rightmask35 |rightmask36 |rightmask37 |rightmask38 |rightmask39 |rightmask40 |rightmask41 |rightmask42 |rightmask43 |rightmask44 |rightmask45 |rightmask46 |rightmask47 |rightmask48 |rightmask49 |rightmask50 |rightmask51 |rightmask52 |rightmask53 |rightmask54 |rightmask55 |rightmask56 |rightmask57 |rightmask58 |rightmask59 |rightmask60 |rightmask61 |rightmask62 |rightmask63 |rightmask64 |rightmask65 |rightmask66 |rightmask67 |rightmask68 |rightmask69 |rightmask70 |rightmask71 |rightmask72 |rightmask73 |rightmask74 |rightmask75 |rightmask76 |rightmask77 |rightmask78 |rightmask79 |rightmask80 |rightmask81 |rightmask82 |rightmask83 |rightmask84 |rightmask85 |rightmask86 |rightmask87 |rightmask88 |rightmask89 |rightmask90 |rightmask91 |rightmask92 |rightmask93 |rightmask94 |rightmask95 |rightmask96 |rightmask97 |rightmask98 |rightmask99 |rightmask100 |rightmask101 |rightmask102 |rightmask103 |rightmask104 |rightmask105 |rightmask106 |rightmask107 |rightmask108 |rightmask109 |rightmask110 |rightmask111 |rightmask112 |rightmask113 |rightmask114 |rightmask115 |rightmask116 |rightmask117 |rightmask118 |rightmask119 |rightmask120 |rightmask121 |rightmask122 |rightmask123 |rightmask124 |rightmask125 |rightmask126 |rightmask127 |rightmask128 |rightmask129 |rightmask130 |rightmask131 |rightmask132 |rightmask133 |rightmask134 |rightmask135 |rightmask136 |rightmask137 |rightmask138 |rightmask139 |rightmask140 |rightmask141 |rightmask142 |rightmask143 |rightmask144 |rightmask145 |rightmask146 |rightmask147 |rightmask148 |rightmask149 |rightmask150 |rightmask151 |rightmask152 |rightmask153 |rightmask154 |rightmask155 |rightmask156 |rightmask157 |rightmask158 |rightmask159 |rightmask160 |rightmask161 |rightmask162 |rightmask163 |rightmask164 |rightmask165 |rightmask166 |rightmask167 |rightmask168 |rightmask169 |rightmask170 |rightmask171 |rightmask172 |rightmask173 |rightmask174 |rightmask175 |rightmask176 |rightmask177 |rightmask178 |rightmask179 |rightmask180 |rightmask181 |rightmask182 |rightmask183 |rightmask184 |rightmask185 |rightmask186 |rightmask187 |rightmask188 |rightmask189 |rightmask190 |rightmask191 |rightmask192 |rightmask193 |rightmask194 |rightmask195 |rightmask196 |rightmask197 |rightmask198 |rightmask199 |rightmask200 |rightmask201 |rightmask202 |rightmask203 |rightmask204 |rightmask205 |rightmask206 |rightmask207 |rightmask208 |rightmask209 |rightmask210 |rightmask211 |rightmask212 |rightmask213 |rightmask214 |rightmask215 |rightmask216 |rightmask217 |rightmask218 |rightmask219 |rightmask220 |rightmask221 |rightmask222 |rightmask223 |rightmask224 |rightmask225 |rightmask226 |rightmask227 |rightmask228 |rightmask229 |rightmask230 |rightmask231 |rightmask232 |rightmask233 |rightmask234 |rightmask235 |rightmask236 |rightmask237 |rightmask238 |rightmask239 |rightmask240 |rightmask241 |rightmask242 |rightmask243 |rightmask244 |rightmask245 |rightmask246 |rightmask247 |rightmask248 |rightmask249

    img_result = cv2.bitwise_and(hairimg, hairimg, mask=img_mask)

    # b_channel, g_channel, r_channel = cv2.split(img_result)

    # alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.

    img_BGRA = img_result  # cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    rows, cols, channels = img_BGRA.shape

    roi = bgimage[0:rows, 0:cols]

    img2gray = cv2.cvtColor(img_BGRA, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_fg = cv2.bitwise_and(img_BGRA, img_BGRA, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    dst = cv2.add(img1_fg, img2_bg)

    bgimage[0:rows, 0:cols] = dst

    cv2.imwrite("segmentation_result.png", dst)
    resultbase64 = Image.fromarray(dst.astype("uint8"))
    rawBytes = io.BytesIO()
    resultbase64.save(rawBytes, "PNG")
    rawBytes.seek(0)  # return to the start of the file
    encodingImage = base64.b64encode(rawBytes.read())

    return encodingImage