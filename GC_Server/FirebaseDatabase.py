import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import json

cred = credentials.Certificate("backup-c8eab-firebase-adminsdk-f1n3v-952e4bd38d.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://backup-c8eab.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
#ref = db.reference('/')
#print(ref.get())

def readUser():
    ref = db.reference('/users')
    userdata = ref.get()
    return userdata

def loadmemo(username):
    ref = db.reference('/memos')
    allmemos = ref.get()
    usermemos = allmemos[username]
    tomirror_memos = []
    for key in usermemos.keys():
        tomirror_value = usermemos[key].get("tomirror")
        print(tomirror_value)
        if tomirror_value != "false":
            tomirror_memos = {key: usermemos[key]}
    return json.dumps(tomirror_memos, ensure_ascii=False)

def baseimage():
    ref = db.reference('/baseimage/test')
    imagelist = ref.get()
    return json.dumps(imagelist, ensure_ascii=False)

def userimage(username):
    ref = db.reference('/images')
    alluser = ref.get()
    userimagelist = alluser[username]
    return json.dumps(userimagelist, ensure_ascii=False)

def selectedimage(username, imagename):
    ref = db.reference("/baseimage/test")
    allimages = ref.get()
    if username == "testuser":
        selectedimage = {imagename: allimages[imagename]}
    else:
        userref = db.reference('/images')
        allusers = userref.get()
        userimages = allusers[username]
        if imagename in userimages.keys():
            selectedimage = {imagename: userimages[imagename]}
        elif imagename not in userimages.keys():
            selectedimage = {imagename: allimages[imagename]}
        
    return json.dumps(selectedimage, ensure_ascii=False)

def saveMatchingResult(username, imageurl):
    print(username+": db에 결과저장 시작")
    timestr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    ref = db.reference('/MatchingResult')
    if username == "testuser":
        ref = ref.child('testuser')
        new_ref = ref.push()
        new_ref.set({
            "date": timestr,
            "imageurl": imageurl
        })
    else:
        ref = ref.child(username)
        new_ref = ref.push()
        new_ref.set({
            "date": timestr,
            "imageurl": imageurl
        })
    return

def saveSegmentResult(username, imageurl, imagename):
    ref = db.reference('/images')
    userimages = ref.child(username)
    updateimage = userimages.child(imagename)
    updateimage.update({
        'pars_img': imageurl
    })
    return
