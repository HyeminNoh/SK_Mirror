import numpy as np
import cv2

facedetector = cv2.CascadeClassifier('Server\open_cv\haarcascade\haarcascade_frontalface_default.xml')
#dlib 설치 후 아래 데이터 활용 안면 윤곽 더 깔끔하게 인식 후 영역 제거 하려했음
#predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
img = cv2.imread('Server\open_cv\image\original.png')

#우리 피부색이 HSV, YCbCr 두가지로 인식가능 함
#해당영역을 추출해냄
#converting from gbr to hsv color space
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#skin color range for hsv color space 
HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17,170,255)) 
HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

#converting from gbr to YCbCr color space
img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
#skin color range for hsv color space 
YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

#merge skin detection (YCbCr and hsv) 
#두 영역 합친것 기반 영역 완성 (얼굴, 목 영역)
global_mask=cv2.bitwise_and(YCrCb_mask,HSV_mask)
global_mask=cv2.medianBlur(global_mask,3)
global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4,4), np.uint8))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#노이즈 제거
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
result_dist_transform = cv2.normalize(dist_transform, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(),255, cv2.THRESH_BINARY)


# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)


# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img, markers)

img[markers == -1] = [255, 0, 0]
img[markers == 1] = [255, 255, 0]

mask = np.zeros(img.shape[:2],np.uint8)

#전경, 배경 지정
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

#영역설정 후 배경제거
rect = (0,100,700,700)

cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

#흰, 검 영역 반전
#HSV_result = cv2.bitwise_not(HSV_mask)
#YCrCb_result = cv2.bitwise_not(YCrCb_mask)

#피부영역 bitwidw_and가 검정영역 다 제거시킴
global_result=cv2.bitwise_not(global_mask)
img = cv2.bitwise_and(img, img, mask=global_result)

#show results
cv2.imshow("Image.png",img)
cv2.imwrite("Image.png",img)

cv2.waitKey(0)
cv2.destroyAllWindows()  