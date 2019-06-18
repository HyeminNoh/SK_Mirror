import numpy as np
import cv2

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0
pointx = 0

def makeresult(originurl):
    #haarcasecade호출
    faceCascade = cv2.CascadeClassifier('static\opencv\haarcascade\haarcascade_frontface.xml')
    eye_cascade = cv2.CascadeClassifier("static\opencv\haarcascade\haarcascade_eye.xml")

    # 이미지읽기 image는 추출할 이미지
    # image = cv2.imread('GC_Server\static\images\hair5.png', -1)
    resp = urllib.request.urlopen(originurl)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    bgimage = cv2.imread("GC_Server\static\images\\bg.png", -1)
    # 원본이미지 폭, 너비 구하기
    img_height = image.shape[0]
    img_width = image.shape[1]
    #이미지크기변경
    # image = cv2.resize(image, dsize=(500, 500), interpolation=cv2.INTER_AREA)
    bgimage = cv2.resize(bgimage, dsize=(img_width, img_height), interpolation=cv2.INTER_AREA)

    #Garyscale로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #msk = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    #inv = cv2.bitwise_not(msk)
    #얼굴인식
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    print
    "Face Count : {0}".format(len(faces))

    #얼굴인식 좌표
    for (x, y, w, h) in faces:
        #머리 중앙
        pointx = int((x + w + x) / 2)
        #얼굴크기
        #cv2.rectangle(image, (x, y-15), (x+w, y + h), (0, 255, 0), 2)
        #머리위치까지 확장
        #cv2.rectangle(image, (x, y-65), (x + w, y + h), (0, 255, 0), 2)
    # cv2.circle(image, (pointx, y-20), 1, (0, 0, 255), -1)
        #cv2.circle(image, (pointx+10, y-20), 1, (0, 0, 255), -1)
        #cv2.circle(image, (pointx-10, y-20), 1, (0, 0, 255), -1)
        #cv2.circle(image, (pointx - 10, y - 25), 1, (0, 0, 255), -1)
        #cv2.circle(image, (pointx + 10, y - 25), 1, (0, 0, 255), -1)
        #cv2.circle(image, (pointx-40, y - 40), 1, (0, 0, 255), -1)
        face_gray = gray[y:y + h, x:x + w]
        face_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(face_gray, 1.1, 3)
        for (ex, ey, ew, eh) in eyes:
            #cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 1)
            image[ey+y: ey + eh+y, ex+x: ex + ew+x] = [255, 255, 255]

    #image[ey+y: ey + eh+y, ex+x: ex + ew+x+20] = [255, 255, 255]
    color1 = image[y-20, pointx]
    color2 = image[y-20, pointx+20]
    color3 = image[y-20, pointx-20]
    color4 = image[y-20, pointx+10]
    color5 = image[y-20, pointx-10]

    color6 = image[y-30, pointx]
    color7 = image[y-30, pointx+20]
    color8 = image[y-30, pointx-20]
    color9 = image[y-30, pointx+10]
    color10 = image[y-30, pointx-10]


    color11 = image[y-40, pointx]
    color12 = image[y-40, pointx-20]
    color13 = image[y-40, pointx+20]
    color14 = image[y-40, pointx-10]
    color15 = image[y-40, pointx+10]

    color16 = image[y-20, pointx+30]
    color17 = image[y-20, pointx-30]
    color18 = image[y-20, pointx+40]
    color19 = image[y-20, pointx-40]


    color20 = image[y-30, pointx+30]
    color21 = image[y-30, pointx-30]
    color22 = image[y-30, pointx+40]
    color23 = image[y-30, pointx-40]

    color24 = image[y-40, pointx+30]
    color25 = image[y-40, pointx-30]
    color26 = image[y-40, pointx+40]
    color27 = image[y-40, pointx-40]

    pixel1 = np.uint8([[color1]])
    pixel2 = np.uint8([[color2]])
    pixel3 = np.uint8([[color3]])
    pixel4 = np.uint8([[color4]])
    pixel5 = np.uint8([[color5]])
    pixel6 = np.uint8([[color6]])
    pixel7 = np.uint8([[color7]])
    pixel8 = np.uint8([[color8]])
    pixel9 = np.uint8([[color9]])
    pixel10 = np.uint8([[color10]])
    pixel11 = np.uint8([[color11]])
    pixel12 = np.uint8([[color12]])
    pixel13 = np.uint8([[color13]])
    pixel14 = np.uint8([[color14]])
    pixel15 = np.uint8([[color15]])
    pixel16 = np.uint8([[color16]])
    pixel17 = np.uint8([[color17]])
    pixel18 = np.uint8([[color18]])
    pixel19 = np.uint8([[color19]])
    pixel20 = np.uint8([[color20]])
    pixel21 = np.uint8([[color21]])
    pixel22 = np.uint8([[color22]])
    pixel23 = np.uint8([[color23]])
    pixel24 = np.uint8([[color24]])
    pixel25 = np.uint8([[color25]])
    pixel26 = np.uint8([[color26]])
    pixel27 = np.uint8([[color27]])



    colorspace1 = cv2.cvtColor(pixel1, cv2.IMREAD_COLOR)
    colorspace2 = cv2.cvtColor(pixel2, cv2.IMREAD_COLOR)
    colorspace3 = cv2.cvtColor(pixel3, cv2.IMREAD_COLOR)
    colorspace4 = cv2.cvtColor(pixel4, cv2.IMREAD_COLOR)
    colorspace5 = cv2.cvtColor(pixel5, cv2.IMREAD_COLOR)
    colorspace6 = cv2.cvtColor(pixel6, cv2.IMREAD_COLOR)
    colorspace7 = cv2.cvtColor(pixel7, cv2.IMREAD_COLOR)
    colorspace8 = cv2.cvtColor(pixel8, cv2.IMREAD_COLOR)
    colorspace9 = cv2.cvtColor(pixel9, cv2.IMREAD_COLOR)
    colorspace10 = cv2.cvtColor(pixel10, cv2.IMREAD_COLOR)
    colorspace11 = cv2.cvtColor(pixel11, cv2.IMREAD_COLOR)
    colorspace12 = cv2.cvtColor(pixel12, cv2.IMREAD_COLOR)
    colorspace13 = cv2.cvtColor(pixel13, cv2.IMREAD_COLOR)
    colorspace14 = cv2.cvtColor(pixel14, cv2.IMREAD_COLOR)
    colorspace15 = cv2.cvtColor(pixel15, cv2.IMREAD_COLOR)
    colorspace16 = cv2.cvtColor(pixel16, cv2.IMREAD_COLOR)
    colorspace17 = cv2.cvtColor(pixel17, cv2.IMREAD_COLOR)
    colorspace18 = cv2.cvtColor(pixel18, cv2.IMREAD_COLOR)
    colorspace19 = cv2.cvtColor(pixel19, cv2.IMREAD_COLOR)
    colorspace20 = cv2.cvtColor(pixel20, cv2.IMREAD_COLOR)
    colorspace21 = cv2.cvtColor(pixel21, cv2.IMREAD_COLOR)
    colorspace22 = cv2.cvtColor(pixel22, cv2.IMREAD_COLOR)
    colorspace23 = cv2.cvtColor(pixel23, cv2.IMREAD_COLOR)
    colorspace24 = cv2.cvtColor(pixel24, cv2.IMREAD_COLOR)
    colorspace25 = cv2.cvtColor(pixel25, cv2.IMREAD_COLOR)
    colorspace26 = cv2.cvtColor(pixel26, cv2.IMREAD_COLOR)
    colorspace27 = cv2.cvtColor(pixel27, cv2.IMREAD_COLOR)


    colorspace1 = colorspace1[0][0]
    colorspace2 = colorspace2[0][0]
    colorspace3 = colorspace3[0][0]
    colorspace4 = colorspace4[0][0]
    colorspace5 = colorspace5[0][0]
    colorspace6 = colorspace6[0][0]
    colorspace7 = colorspace7[0][0]
    colorspace8 = colorspace8[0][0]
    colorspace9 = colorspace9[0][0]
    colorspace10 = colorspace10[0][0]
    colorspace11 = colorspace11[0][0]
    colorspace12 = colorspace12[0][0]
    colorspace13 = colorspace13[0][0]
    colorspace14 = colorspace14[0][0]
    colorspace15 = colorspace15[0][0]
    colorspace16 = colorspace16[0][0]
    colorspace17 = colorspace17[0][0]
    colorspace18 = colorspace18[0][0]
    colorspace19 = colorspace19[0][0]
    colorspace20 = colorspace20[0][0]
    colorspace21 = colorspace21[0][0]
    colorspace22 = colorspace22[0][0]
    colorspace23 = colorspace23[0][0]
    colorspace24 = colorspace24[0][0]
    colorspace25 = colorspace25[0][0]
    colorspace26 = colorspace26[0][0]
    colorspace27 = colorspace27[0][0]


    lower_blue1 = np.array([colorspace1[0] - 40, colorspace1[1] - 40, colorspace1[2] - 40])
    upper_blue1 = np.array([colorspace1[0] + 40, colorspace1[1] + 40, colorspace1[2] + 40])

    lower_blue2 = np.array([colorspace2[0] - 40, colorspace2[1] - 40, colorspace2[2] - 40])
    upper_blue2 = np.array([colorspace2[0] + 40, colorspace2[1] + 40, colorspace2[2] + 40])

    lower_blue3 = np.array([colorspace3[0] - 40, colorspace3[1] - 40, colorspace3[2] - 40])
    upper_blue3 = np.array([colorspace3[0] + 40, colorspace3[1] + 40, colorspace3[2] + 40])

    lower_blue4 = np.array([colorspace4[0] - 40, colorspace4[1] - 40, colorspace4[2] - 40])
    upper_blue4 = np.array([colorspace4[0] + 40, colorspace4[1] + 40, colorspace4[2] + 40])

    lower_blue5 = np.array([colorspace5[0] - 40, colorspace5[1] - 40, colorspace5[2] - 40])
    upper_blue5 = np.array([colorspace5[0] + 40, colorspace5[1] + 40, colorspace5[2] + 40])

    lower_blue6 = np.array([colorspace6[0] - 40, colorspace6[1] - 40, colorspace6[2] - 40])
    upper_blue6 = np.array([colorspace6[0] + 40, colorspace6[1] + 40, colorspace6[2] + 40])

    lower_blue7 = np.array([colorspace7[0] - 40, colorspace7[1] - 40, colorspace7[2] - 40])
    upper_blue7 = np.array([colorspace7[0] + 40, colorspace7[1] + 40, colorspace7[2] + 40])

    lower_blue8 = np.array([colorspace8[0] - 40, colorspace8[1] - 40, colorspace8[2] - 40])
    upper_blue8 = np.array([colorspace8[0] + 40, colorspace8[1] + 40, colorspace8[2] + 40])

    lower_blue9 = np.array([colorspace9[0] - 40, colorspace9[1] - 40, colorspace9[2] - 40])
    upper_blue9 = np.array([colorspace9[0] + 40, colorspace9[1] + 40, colorspace9[2] + 40])

    lower_blue10 = np.array([colorspace10[0] - 40, colorspace10[1] - 40, colorspace10[2] - 40])
    upper_blue10 = np.array([colorspace10[0] + 40, colorspace10[1] + 40, colorspace10[2] + 40])

    lower_blue11 = np.array([colorspace11[0] - 40, colorspace11[1] - 40, colorspace11[2] - 40])
    upper_blue11 = np.array([colorspace11[0] + 40, colorspace11[1] + 40, colorspace11[2] + 40])

    lower_blue12 = np.array([colorspace12[0] - 40, colorspace12[1] - 40, colorspace12[2] - 40])
    upper_blue12 = np.array([colorspace12[0] + 40, colorspace12[1] + 40, colorspace12[2] + 40])

    lower_blue13 = np.array([colorspace13[0] - 40, colorspace13[1] - 40, colorspace13[2] - 40])
    upper_blue13 = np.array([colorspace13[0] + 40, colorspace13[1] + 40, colorspace13[2] + 40])

    lower_blue14 = np.array([colorspace14[0] - 40, colorspace14[1] - 40, colorspace14[2] - 40])
    upper_blue14 = np.array([colorspace14[0] + 40, colorspace14[1] + 40, colorspace14[2] + 40])

    lower_blue15 = np.array([colorspace15[0] - 40, colorspace15[1] - 40, colorspace15[2] - 40])
    upper_blue15 = np.array([colorspace15[0] + 40, colorspace15[1] + 40, colorspace15[2] + 40])

    lower_blue16 = np.array([colorspace16[0] - 40, colorspace16[1] - 40, colorspace16[2] - 40])
    upper_blue16 = np.array([colorspace16[0] + 40, colorspace16[1] + 40, colorspace16[2] + 40])

    lower_blue17 = np.array([colorspace17[0] - 40, colorspace17[1] - 40, colorspace17[2] - 40])
    upper_blue17 = np.array([colorspace17[0] + 40, colorspace17[1] + 40, colorspace17[2] + 40])

    lower_blue18 = np.array([colorspace18[0] - 40, colorspace18[1] - 40, colorspace18[2] - 40])
    upper_blue18 = np.array([colorspace18[0] + 40, colorspace18[1] + 40, colorspace18[2] + 40])

    lower_blue19 = np.array([colorspace19[0] - 40, colorspace19[1] - 40, colorspace19[2] - 40])
    upper_blue19 = np.array([colorspace19[0] + 40, colorspace19[1] + 40, colorspace19[2] + 40])

    lower_blue20 = np.array([colorspace20[0] - 40, colorspace20[1] - 40, colorspace20[2] - 40])
    upper_blue20 = np.array([colorspace20[0] + 40, colorspace20[1] + 40, colorspace20[2] + 40])

    lower_blue21 = np.array([colorspace21[0] - 40, colorspace21[1] - 40, colorspace21[2] - 40])
    upper_blue21 = np.array([colorspace21[0] + 40, colorspace21[1] + 40, colorspace21[2] + 40])

    lower_blue22 = np.array([colorspace22[0] - 40, colorspace22[1] - 40, colorspace22[2] - 40])
    upper_blue22 = np.array([colorspace22[0] + 40, colorspace22[1] + 40, colorspace22[2] + 40])

    lower_blue23 = np.array([colorspace23[0] - 40, colorspace23[1] - 40, colorspace23[2] - 40])
    upper_blue23 = np.array([colorspace23[0] + 40, colorspace23[1] + 40, colorspace23[2] + 40])

    lower_blue24 = np.array([colorspace24[0] - 40, colorspace24[1] - 40, colorspace24[2] - 40])
    upper_blue24 = np.array([colorspace24[0] + 40, colorspace24[1] + 40, colorspace24[2] + 40])

    lower_blue25 = np.array([colorspace25[0] - 40, colorspace25[1] - 40, colorspace25[2] - 40])
    upper_blue25 = np.array([colorspace25[0] + 40, colorspace25[1] + 40, colorspace25[2] + 40])

    lower_blue26 = np.array([colorspace26[0] - 40, colorspace26[1] - 40, colorspace26[2] - 40])
    upper_blue26 = np.array([colorspace26[0] + 40, colorspace26[1] + 40, colorspace26[2] + 40])

    lower_blue27 = np.array([colorspace27[0] - 40, colorspace27[1] - 40, colorspace27[2] - 40])
    upper_blue27 = np.array([colorspace27[0] + 40, colorspace27[1] + 40, colorspace27[2] + 40])

    img_mask1 = cv2.inRange(image, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(image, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(image, lower_blue3, upper_blue3)
    img_mask4 = cv2.inRange(image, lower_blue4, upper_blue4)
    img_mask5 = cv2.inRange(image, lower_blue5, upper_blue5)
    img_mask6 = cv2.inRange(image, lower_blue6, upper_blue6)
    img_mask7 = cv2.inRange(image, lower_blue7, upper_blue7)
    img_mask8 = cv2.inRange(image, lower_blue8, upper_blue8)
    img_mask9 = cv2.inRange(image, lower_blue9, upper_blue9)
    img_mask10 = cv2.inRange(image, lower_blue10, upper_blue10)
    img_mask11 = cv2.inRange(image, lower_blue11, upper_blue11)
    img_mask12 = cv2.inRange(image, lower_blue12, upper_blue12)
    img_mask13 = cv2.inRange(image, lower_blue13, upper_blue13)
    img_mask14 = cv2.inRange(image, lower_blue14, upper_blue14)
    img_mask15 = cv2.inRange(image, lower_blue15, upper_blue15)
    img_mask16 = cv2.inRange(image, lower_blue16, upper_blue16)
    img_mask17 = cv2.inRange(image, lower_blue17, upper_blue17)
    img_mask18 = cv2.inRange(image, lower_blue18, upper_blue18)
    img_mask19 = cv2.inRange(image, lower_blue19, upper_blue19)
    img_mask20 = cv2.inRange(image, lower_blue20, upper_blue20)
    img_mask21 = cv2.inRange(image, lower_blue20, upper_blue21)
    img_mask22 = cv2.inRange(image, lower_blue20, upper_blue22)
    img_mask23 = cv2.inRange(image, lower_blue20, upper_blue23)
    img_mask24 = cv2.inRange(image, lower_blue20, upper_blue24)
    img_mask25 = cv2.inRange(image, lower_blue20, upper_blue25)
    img_mask26 = cv2.inRange(image, lower_blue20, upper_blue26)
    img_mask27 = cv2.inRange(image, lower_blue20, upper_blue27)



    img_mask = img_mask1 | img_mask2 | img_mask3 | img_mask4 | img_mask5 | img_mask6 | img_mask7 | img_mask8 | img_mask9 | img_mask10 | img_mask11 | img_mask12 | img_mask13 | img_mask14 | img_mask15 | img_mask16 | img_mask17 | img_mask18 | img_mask19 | img_mask20 | img_mask21 | img_mask22 | img_mask23 | img_mask24 | img_mask25 | img_mask26 | img_mask27

    img_result = cv2.bitwise_and(image, image, mask=img_mask)

    b_channel, g_channel, r_channel = cv2.split(img_result)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    rows, cols, channels = img_BGRA.shape

    roi = bgimage[0:rows, 0:cols]

    img2gray = cv2.cvtColor(img_BGRA, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_fg = cv2.bitwise_and(img_BGRA, img_BGRA, mask=mask)
    img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    dst = cv2.add(img1_fg, img2_bg)

    bgimage[0:rows, 0:cols] = dst

    #dst = cv2.add(img1_fg, img2_bg)
    #bgimage[0:rows, 0:cols] = dst
    #umimage = cv2.addWeighted(bgimage, 0.4, img_result, 0.4, 0)

    #cv2.imwrite("result.png", img2_bg)
    #cv2.imshow('1', mask_inv)
    #cv2.imshow('2', image)
    #cv2.imshow("3", dst)
    cv2.imwrite("segmentation_result.png", dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
    resultbase64 = Image.fromarray(dst.astype("uint8"))
    rawBytes = io.BytesIO()
    resultbase64.save(rawBytes, "PNG")
    rawBytes.seek(0)  # return to the start of the file
    encodingImage = base64.b64encode(rawBytes.read())

    return encodingImage