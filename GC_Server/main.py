#헤어스타일링 지원 스마트미러 flask app
import logging
import requests
import ImageMatching as ImageMatching
import json
import base64
from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
from werkzeug.utils import secure_filename
import time
import maptogrid
import HairSegmentation as seg_hair
import rgbdata as rgb
import gcpCloudStorage as gcpCS
import FirebaseDatabase as FDB


app = Flask(__name__)
#선택 이미지 정보 저장 전역변수
selectedimage = {"origin":"", "parsimg":"", "userimg":"", "colorname":""}
selectcolor = "original"
app.secret_key = 'any random string'

#메인
@app.route('/', methods=["GET"])
def mirrormain():
    if "username" in session:
        return render_template('index.html', username=session["username"])    
    elif "username" not in session:
        return render_template('index.html', username="")

#로그인 요청
@app.route('/login', methods=['POST'])
def login():
    #form에서 이메일과 비밀번호 얻기
    checkname = request.form['uname1']
    checkpwd = request.form['pwd1']
    #파이어베이스 db 사용자 정보들과 비교
    userdata = FDB.readUser()
    if checkname in userdata.keys():
        loginuser_data = userdata[checkname]
        #print(loginuser_data)
        if loginuser_data['password'] == checkpwd:
            session['username'] = checkname
            print('success')
            return redirect(url_for('mirrormain',username=session['username']))
    return redirect(url_for('mirrormain',username=""))

#로그아웃 요청
@app.route('/logout', methods=['POST','GET'])
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('mirrormain', username=""))

#메모 로드 테스트
@app.route('/memotest', methods=['GET'])
def memotest():
    memodata = FDB.loadmemo("testuser")
    return memodata

#메모 데이터
@app.route('/memodata', methods=['GET'])
def memodata():
    if "username" in session:
        memodata = FDB.loadmemo(session['username'])
    elif "username" not in session:
        memodata = FDB.loadmemo("testuser")
    return memodata

#베이스 이미지 리스트 json
@app.route('/baseimagelist', methods=['GET'])
def baseimagelist():
    imagelist = FDB.baseimage()
    return imagelist

#사용자 이미지 리스트 json
@app.route('/userimagelist', methods=['GET'])
def userimagelist():
    if "username" in session:
        imagelist = FDB.userimage(session["username"])
    elif "username" not in session:
        imagelist = FDB.baseimage()
    return imagelist

#이미지리스트 뷰, 로그인 유무 확인
@app.route('/imagelist', methods=['POST', 'GET'])
def ImagelistView():
    if "username" not in session:
        return render_template('imageList.html',username="")
    elif "username" in session:
        return render_template('imageList.html',username=session["username"])

#사용자이미지 리스트 뷰
@app.route('/userimagelist', methods=['POST'])
def userImageView():
    #username = request.form['usernametxt']
    return render_template('userimagelist.html',username=session["username"])

#기본 컬러 리스트 뷰, 로그인 유무 확인
@app.route('/colorlist', methods=['POST','GET'])
def ColorlistView():
    if request.method == "POST":
        username = request.form['usernametocolor']
    elif request.method == "GET":
        username = request.args.get('username')
    if username is None:
        return render_template('colorList.html',username="")
    else:
        return render_template('colorList.html',username=username)

#사용자 컬러 리스트 뷰
@app.route('/usercolorlist', methods=['POST'])
def userColorView():
    return '준비중'

#이미지 매칭 기능 기본 뷰
@app.route('/imagematching', methods=['POST'])
def imagematching():
    selected = request.form['selectImage']
    selectedname = str(selected)
    return render_template('imagematching2.html', selectedname=selectedname)

#컬러매칭 기능 기본 뷰
@app.route('/colormatching', methods=['POST'])
def colormatching():
    selected = request.form['selectColor']
    selectedcolor = str(selected)
    rgbtuple = rgb.find(selectedcolor)
    return str(rgbtuple)

#선택된 이미지 정보 요청
@app.route('/selectedimage', methods=['POST','GET'])
def findselected():
    if request.method == "POST":
        img_name = request.json['img_name']
        if 'username' in session:
            selectedreturn = FDB.selectedimage(session['username'], img_name)
        elif 'username' not in session:
            selectedreturn = FDB.selectedimage("testuser", img_name)
        return selectedreturn
    elif request.method =="GET":
        selectedreturn = json.dumps(selectedimage)
        return selectedreturn
        
#헤어 이미지 추출 실행
@app.route('/segmentation', methods=['POST'])
def segmentation():
    originurl = request.json['img_url']
    img_name = request.json['img_name']
    hair_type = request.json['type']
    base64_result = seg_hair.makeresult(originurl, hair_type)
    url = ''
    with open("segmentation_result.png", "rb") as fh:
        url = gcpCS.upload(
            file=fh,
            bucket_name='skmirror',
            filepath='/imgMatch'
        )

        print('#################', url)
    data = {'result': url, 'img_name': img_name, 'username': session['username']}
    print(data)
    #response = requests.post('http://us-central1-backup-c8eab.cloudfunctions.net/app/segmentation_result', data=data)
    if 'username' in session:
        FDB.saveSegmentResult(session['username'], url, img_name)

    return url

#이미지 매칭 실행 후 결과 이미지 url을 반환
@app.route('/imageresult', methods=['POST'])
def imageresult():
    origin = request.json['origin']
    parsimg = request.json['parsimg']
    snapuri = request.json['snapuri']
    colorname = request.json['colorname']
    selectedimage["origin"] = origin
    selectedimage["parsimg"] = parsimg
    selectedimage["userimg"] = snapuri
    selectedimage["colorname"] = colorname

    resultbase = ImageMatching.startMatching()
    '''
    print(resultbase)
    result = base64.b64decode(resultbase).decode('utf-8')
    '''
    #with open("imageToSave.png", "wb") as fh:
    #    fh.write(base64.decodebytes(resultbase))
    url = ''
    with open("result.jpg", "rb") as fh:
        url = gcpCS.upload(
            file=fh,
            bucket_name='skmirror',
            filepath='/imgMatch'
        )

        print('#################', url)
    #data = {'result': url}
    #response = requests.post('http://us-central1-backup-c8eab.cloudfunctions.net/app/uploadresult', data=data)
    if 'username' in session:
        FDB.saveMatchingResult(session['username'], url)
    elif 'username' not in session:
        FDB.saveMatchingResult("testuser", url)
    return url

#기상청 API 활용 날씨 정보
@app.route('/forecast', methods=['GET'])
def forecast():
    #로그인상태일때 주소지
    if 'username' in session:
        #파이어베이스 db 사용자 정보로드
        username = session['username']
        userdata = FDB.readUser()
        address = userdata[username].get('address')
    #로그아웃상태일때 기본 주소지
    elif 'username' not in session:
        address = "서울특별시 종로구 세종로"
    findaddress = address
    print(findaddress)
    geo_params = {
        "address": findaddress,
        "key": 'AIzaSyAlkaLa_74zkXq1w98s4LAvOasKxdG-c_w'
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=geo_params)
    dictdata = response.json()
    locationresult = dictdata['results']
    #위도경도 파싱해냄 lat, lng 딕셔너리 형태 자료
    geovalue = locationresult[0].get('geometry').get('location')
    now = time.localtime()
    #예보 시간이 지정되어 있으므로 시간 체크 후 지정
    standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
    check_time = int(now.tm_hour) - 1
    day_calibrate = 0
    while not check_time in standard_time :
        check_time -= 1
        if check_time < 2 :
            day_calibrate = 1
            check_time = 23

    base_time = "%02d00" % (check_time)
    #오후 1시이후에 다음날 데이터를 받을 경우, now.tm_mday-day_calibrate로 수정하면 됨
    base_date = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday-day_calibrate)

    grid = maptogrid.mapToGrid(geovalue['lat'], geovalue['lng'])
    #기상예보 요청 파라미터
    ServiceKey = 'tKpVoRDuSAy%2BCSFhBp2rT2AbPcxEfzAeVbO2U8wgGZWwBt7mkhbsgPe7aFC3nWeJW0S%2FB4IKxqSvF9ZUJHstyw%3D%3D'
    nx = grid[0]
    ny = grid[1]
    forecast_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?ServiceKey='+ServiceKey+'&base_date='+base_date+'&base_time='+base_time+'&nx='+str(nx)+'&ny='+str(ny)+'&_type=json'
    forecast_response = requests.get(forecast_url)
    forecast_dict = forecast_response.json()
    parsed_json = forecast_dict['response']['body']['items']['item']

    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date #date of TMX, TMN
    if int(target_time) > 1300:
        date_calibrate = str(int(target_date) + 1)

    parsing_data = {}
    for one_parsed in parsed_json:
        if one_parsed['fcstDate'] == target_date and one_parsed['fcstTime'] == target_time: #get today's data
            parsing_data[one_parsed['category']] = one_parsed['fcstValue']

        if one_parsed['fcstDate'] == date_calibrate and (
                one_parsed['category'] == 'TMX' or one_parsed['category'] == 'TMN'): #TMX, TMN at calibrated day
            parsing_data[one_parsed['category']] = one_parsed['fcstValue']
    
    result = {"현재기온": " - °C", "하늘": " - ", "최고기온": " - °C", "최저기온": " - °C"}
    #현재기온
    nowtemp = '-'
    if 'T3H' in parsing_data.keys():
        result['현재기온'] = str(parsing_data['T3H'])+" °C"
    
    #최고기온
    maxtemp = '-'
    if 'TMX' in parsing_data.keys():
        result['최고기온'] = str(parsing_data['TMX'])+" °C"
    
    #최저기온
    mintemp = '-'
    if 'TMN' in parsing_data.keys():
        result['최저기온'] = str(parsing_data['TMN'])+" °C"

    #하늘상태 코드분류
    skystatus = '-'
    if 'SKY' in parsing_data.keys():
        if parsing_data['SKY'] == 1:
            skystatus = "맑음"
        elif parsing_data['SKY'] == 3:
            skystatus = "구름많음"
        elif parsing_data['SKY'] == 4:
            skystatus = "흐림"
        result['하늘'] = skystatus

    #강수확률
    rainiyamount = '-'
    if 'POP' in parsing_data.keys():
        result['비 올 확률'] = str(parsing_data['POP']) + "%"

    #강수형태 코드분류
    rainstatus = '-'
    if 'PTY' in parsing_data.keys():
        if parsing_data['PTY'] == 0:
            rainstatus = "보통"
        elif parsing_data['PTY'] == 1:
            rainstatus = "비"
        elif parsing_data['PTY'] == 2:
            rainstatus = "비/눈 (진눈개비)"
        elif parsing_data['PTY'] == 3:
            rainstatus = "눈"
        elif parsing_data['PTY'] == 4:
            rainstatus = "소나기"
        result['하늘'] = rainstatus

    forecast_json = json.dumps(result, ensure_ascii=False).encode('utf-8')

    return forecast_json

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]

