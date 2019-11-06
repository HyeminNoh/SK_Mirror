//사용자이미지 리스트 뷰 db데이터 로드해서 반영

var username = document.getElementById('usernamep');
console.log(username.textContent);

// get JSON with using pure javascript
var request= new XMLHttpRequest();

//var url= "http://us-central1-backup-c8eab.cloudfunctions.net/app/images?username="+username.textContent;
var url = "http://127.0.0.1:8080/userimagelist"
console.log(url);
request.open("GET", url);
request.responseType='json';
request.send();

request.onload = function() {
    var images = request.response;
    console.log(images);
    checkimage(images);
    makeImageview(images);
}

function makeImageview(jsonObj) {
    var loadimages = jsonObj;
    var container = document.getElementById('images');
    for (var i = 0; i < Object.keys(loadimages).length; i++) {
        var imgbox = document.createElement('img');
        var keys = Object.keys(loadimages);
        var url = loadimages[keys[i]].img_file;
        console.log(keys[i]);
        imgbox.src = url;
        imgbox.style.margin='10px';
        imgbox.style.height = '200px';
        imgbox.style.width = '200px';
        imgbox.style.display = 'inline-block';
        imgbox.name=keys[i];
        imgbox.onclick=function() {sendData(this.name)};
        //imgbox.onclick=function() {alert('준비중입니다.')};
        container.appendChild(imgbox);
    }
}

function sendData(imgName){
    var select = document.getElementById('selectImage');
    select.value=imgName;
    console.log(imgName);
    var form = document.getElementById('imageradio');
    form.submit();
}
function checkimage(jsonObj){
    var loadimages = jsonObj;
    for (var i = 0; i < Object.keys(loadimages).length; i++) {
        var keys = Object.keys(loadimages);
        var img_url = loadimages[keys[i]].img_file;
        var pars_url = loadimages[keys[i]].pars_img;
        var hair_type = loadimages[keys[i]].type;
        if(pars_url=="" || pars_url==null){
            startparsing(keys[i], img_url, hair_type)
        }
    }
}
function startparsing (img_name, img_url, hair_type){
    // get JSON with using pure javascript
    var pars_request= new XMLHttpRequest();
    var data = {
        "img_name": img_name,
        "img_url": img_url,
        "type": hair_type
    };
    var url= "http://127.0.0.1:8080/segmentation";
    console.log(data)
    pars_request.open("POST", url, false);
    pars_request.setRequestHeader('Content-Type', 'application/json'); // 컨텐츠타입을 json으로
    pars_request.send(JSON.stringify(data)); // 데이터를 stringify해서 보냄

    pars_request.onload = function() {
        var result_url = pars_request.response;
        console.log(result_url);
    }
}