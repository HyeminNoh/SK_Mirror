//기본제공 이미지 리스트 뷰 db로드 후 반영
// get JSON with using pure javascript
var request= new XMLHttpRequest();

var url= "https://us-central1-backup-c8eab.cloudfunctions.net/app/baseimagelist";
request.open("GET", url);
request.responseType='json';
request.send();

request.onload = function() {
    var images = request.response;
    makeImageview(images);
}

function makeImageview(jsonObj) {
    var loadimages = jsonObj.test;
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

function checklogin(usernametxt){
    console.log(usernametxt);
    var userimagebtn = document.getElementById('userimagebtn')
    if(usernametxt==""){
        userimagebtn.style.visibility='hidden';
    }
}