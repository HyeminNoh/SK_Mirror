var videoTracks;
var selectedimg;
var snapURI;
var video = document.getElementById('myVideo');
function load() {
    if (navigator.webkitGetUserMedia) {
        navigator.webkitGetUserMedia({audio:true, video:true},
            function(stream) {
                video.srcObject=stream;
                videoTracks = stream.getVideoTracks();
                video.play();
            },
            function(error) { alert('ERROR: ' + error.toString()); } );
    } else {
        alert('webkitGetUserMedia not supported');
    }
}
function startCount(){
    var btn=document.getElementById("start_btn");
    var seconds=3;
    var countdown = setInterval(function() {
        btn.textContent=seconds;
        seconds--;
        if (seconds <= 0){
            clearInterval(countdown);
            btn.remove(true);
            takesnap();
        }
    }, 1001);
}
function takesnap(){
    var canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    var ctx = canvas.getContext('2d');
    //draw image to canvas. scale to target dimensions
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Stop all video streams.
    videoTracks.forEach(function(track) {track.stop()});
    //convert to desired file format
    snapURI = canvas.toDataURL('image/jpeg'); // can also use 'image/png'
    video.remove(true);
    var textdiv = document.getElementById("textdiv");
    textdiv.style.fontSize="30px";
    textdiv.innerHTML = "매칭중..."
    startmatching();
}
function makeImageview() {
    var hairname = document.getElementById('hairname');
    console.log(hairname.textContent);
    var name = hairname.textContent;
    var request= new XMLHttpRequest();
    var url= "https://us-central1-backup-c8eab.cloudfunctions.net/app/seletedimage?name="+name;
    request.open("GET", url);
    request.responseType='json';
    request.send();

    request.onload = function() {
        var image = request.response;
        selectedimg=image;
        //console.log(image);
        var keys = Object.keys(image);
        var loadimages = image[keys[0]].img_file;
        var imgbox = document.getElementById('imgbox');
        imgbox.src=loadimages;
        imgbox.style.height = '350';
        imgbox.style.width = '350px';
    }
}

function saveColor(colorName){
    sessionStorage.setItem('colorName', colorName);
    $('#myModal').modal('hide');
    console.log(sessionStorage.getItem('colorName'));
}
function resetColor(){
    sessionStorage.setItem('colorName', 'original');
    console.log(sessionStorage.getItem('colorName'));
}
function startmatching(){
    var keys = Object.keys(selectedimg);
    var originurl = selectedimg[keys[0]].img_file;
    var parsimgurl = selectedimg[keys[0]].pars_img
    var colorname = sessionStorage.getItem('colorName');
    // get JSON with using pure javascript
    var getrequest = new XMLHttpRequest();
    var data = {
        origin: originurl,
        parsimg: parsimgurl,
        snapuri: snapURI,
        colorname: colorname,
    };
    console.log(data);
    var url= "http://127.0.0.1:8080/imageresult";
    getrequest.open("POST", url);
    getrequest.setRequestHeader('Content-Type', 'application/json'); // 컨텐츠타입을 json으로
    getrequest.send(JSON.stringify(data)); // 데이터를 stringify해서 보냄

    getrequest.onload = function() {
        console.log(getrequest.response);
        if(getrequest.response!=null){
            var resulttxt = getrequest.response;
            var imgbox = document.getElementById('imgbox');
            var button = document.getElementById('seleccolor_btn');
            var textdiv = document.getElementById("textdiv");
            imgbox.src=resulttxt;
            imgbox.style.height = '100%';
            imgbox.style.width = '100%';
            button.hidden('true');
            textdiv.textContent="success";
        }
    }
}