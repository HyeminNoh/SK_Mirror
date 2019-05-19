# facerecognition.py
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

facedetector = cv2.CascadeClassifier('static\opencv\haarcascade\haarcascade_frontalface_default.xml')

def startInit(originurl):
    #original = cv2.imread('static\opencv\image\original.jpg')
    resp = urllib.request.urlopen(originurl)
    original = np.asarray(bytearray(resp.read()), dtype="uint8")
    original = cv2.imdecode(original, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    originface = facedetector.detectMultiScale(gray, 1.3, 5)
    print("원본안면인식크기 width:"+str(originface[0][2])+" height:"+str(originface[0][3]))

    return originface

def startMatching():
    #originurl = "https://firebasestorage.googleapis.com/v0/b/backup-c8eab.appspot.com/o/images%2FHairexamples%2Fimage1.jpg?alt=media&token=c127a1cc-0e36-40bc-a44a-b19bbffb6d15"
    #parsurl = "https://firebasestorage.googleapis.com/v0/b/backup-c8eab.appspot.com/o/hairResult%2Fhair01_pars.PNG?alt=media&token=88d46032-f7bf-4482-8ac6-d95154c7e50d"
    
    originurl = "https://firebasestorage.googleapis.com/v0/b/backup-c8eab.appspot.com/o/images%2FHairexamples%2Fimage1.jpg?alt=media&token=d37f7003-ccb5-4867-8b51-f6e30721d862"
    parsurl = "https://firebasestorage.googleapis.com/v0/b/backup-c8eab.appspot.com/o/hairResult%2Fhair01_pars.PNG?alt=media&token=de224eb3-ad07-4f3e-85bf-7aacf8f18594"

    originface = startInit(originurl)
    #hair = cv2.imread('static\opencv\image\TestImage.png', -1)
    #matchingsnap = cv2.imread('static/opencv/image/testuserimg.jpg')
    matchingsnap = makesnap()

    gray = cv2.cvtColor(matchingsnap, cv2.COLOR_BGR2GRAY)
    faces = facedetector.detectMultiScale(gray, 1.3, 5)
    encodingImage = ''

    print("사용자안면인식 width:"+str(faces[0][2])+" height:"+str(faces[0][3]))
    for (x, y, w, h) in faces:
        overlayHair = changeSize(parsurl, (w, h), (originface[0][2], originface[0][3]))

        cv2.imwrite('overlayHair.png',overlayHair)
        hair_height, hair_width = overlayHair.shape[:2]
        
        x = int(x-(hair_width-w)/2)
        #y = int(y-2*y/5)
        #y = int(y-originface[0][3]/5)
        y = int(y-(hair_height-h)/4)
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
   # return matchingsnap
    
def makesnap():
    #cam = cv2.VideoCapture(videoUrl)
    cam = cv2.VideoCapture("http://192.168.137.14:8090/?action=stream")
    #cam = cv2.VideoCapture(0)
    
    cam.set(cv2.CAP_PROP_FPS, 30)
    ret, frame = cam.read()


    matchingorigin = cv2.flip(frame, 1)
    cv2.imwrite('userimg.jpg', matchingorigin)
    cam.release()
    #print(matchingorigin)
    return matchingorigin

def changeSize(hair, detectSize=(0,0), originsize=(0,0)):
    urlresp = urllib.request.urlopen(hair)
    parshair = np.asarray(bytearray(urlresp.read()), dtype="uint8")
    parshair = cv2.imdecode(parshair, cv2.IMREAD_UNCHANGED)
    #사용자 얼굴이 더클때
    #if detectSize[0]>originsize[0] and detectSize[1]>originsize[1]:
    w = detectSize[0]/originsize[0]
    h = detectSize[1]/originsize[1]
    print("안면비율차이 w: "+str(w)+"h: "+str(h))
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
    
    cv2.imwrite('overlaysrc.jpg', src)
    return src

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    frame = startMatching()
    cv2.imwrite('frame.jpg', frame)
    cv2.destroyAllWindows()

'''
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name) #skmirrorhw
    blob = bucket.blob(destination_blob_name) #result_b.

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

@app.route('/')
def index():
    return """
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""


def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('result.jpg')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url
'''