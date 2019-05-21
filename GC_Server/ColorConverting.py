import cv2
import numpy as np
import os

def convertColor(parshair, rgbtp):

        r = rgbtp[0]
        g = rgbtp[1]
        b = rgbtp[2]

        height, width, channel = parshair.shape
        output = parshair[:,:,0:3]

        for i in range(height):
            for j in range(width):
                if parshair[i][j][3] != 0:
                    parshair[i][j][3] = 255
        temp = np.zeros(shape=(height,width,4),dtype=np.uint8)
        hair_check = np.zeros(shape=(height,width),dtype=np.uint8) 
        
        for i in range(height):
            for j in range(width):
                temp[i][j][3] = parshair[i][j][3]
                if parshair[i][j][3] == 255:
                    temp[i][j][0] = parshair[i][j][0]
                    temp[i][j][1] = parshair[i][j][1]
                    temp[i][j][2] = parshair[i][j][2]
                    output[i][j][0] = parshair[i][j][0]
                    output[i][j][1] = parshair[i][j][1]
                    output[i][j][2] = parshair[i][j][2]
                    hair_check[i][j] = True # 알파 채널을 통하여 hair인 부분 체크
                else :
                    hair_check[i][j] = False
        # cv2.imshow("원본", parshair[:,:,3])
        
        grayscale = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY) #그레이 스케일 변환과정 명암값을 구하기 위해
        clahe = cv2.createCLAHE(clipLimit=64.0, tileGridSize=(4,4)) #이미지 평활화 과정
        eq_gray = clahe.apply(grayscale) 
        for i in range(height):
            for j in range(width):
                if(hair_check[i][j]):
                    if eq_gray[i][j] > 230:
                        temp[i][j][0] = (eq_gray[i][j]) / 255 * b  #B
                        temp[i][j][1] = (eq_gray[i][j]) / 255 * g  #G
                        temp[i][j][2] = (eq_gray[i][j]) / 255 * r  # R 214,196,194
                        output[i][j][0] = (eq_gray[i][j]) / 255 * b  #B
                        output[i][j][1] = (eq_gray[i][j]) / 255 * g  #G
                        output[i][j][2] = (eq_gray[i][j]) / 255 * r  # R 214,196,194
                
                    else :
                        temp[i][j][0] = (255 - eq_gray[i][j]) / 255 * b  #B
                        temp[i][j][1] = (255 - eq_gray[i][j]) / 255 * g  #G
                        temp[i][j][2] = (255 - eq_gray[i][j]) / 255 * r  #R 214,196,194
                        output[i][j][0] = (255 - eq_gray[i][j]) / 255 * b  #B
                        output[i][j][1] = (255 - eq_gray[i][j]) / 255 * g  #G
                        output[i][j][2] = (255 - eq_gray[i][j]) / 255 * r  #R 214,196,194
        
        cv2.imshow("frame", output) # result
        cv2.imshow("frame", temp) # only hair
        

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            if not (os.path.isdir("out")):
                os.mkdir("out")

        cv2.imwrite("out/out.png", output)
        cv2.imwrite("out/onlyhair.png", temp)

        return temp
   