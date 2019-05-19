var selectedimg;
function startCount(){
        var btn=document.getElementById("start_btn");
        var seconds=3;
        var countdown = setInterval(function() {
        btn.textContent=seconds;
        seconds--;
        if (seconds <= 0){
            clearInterval(countdown);
            btn.remove(true);
            var touchdiv = document.getElementById("touchdiv");
            touchdiv.style.fontSize="30px";
            touchdiv.innerHTML = "매칭중..."
            startmatching();
        }
    }, 1001);
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
        imgbox.style.height = '450px';
        imgbox.style.width = '450px';

    }
}
function startmatching(){
    var keys = Object.keys(selectedimg);
    var originurl = selectedimg[keys[0]].img_file;
    var parsimgurl = selectedimg[keys[0]].pars_img
    // get JSON with using pure javascript
    var getrequest = new XMLHttpRequest();
    var data = {
        origin: originurl,
        parsimg: parsimgurl
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
            var touchdiv = document.getElementById("touchdiv");
            imgbox.src=resulttxt;
            imgbox.style.height = '450px';
            imgbox.style.width = '400px';
            touchdiv.textContent="success";
        }
        else if(getrequest.response==""){
            var touchdiv = document.getElementById("touchdiv");
            touchdiv.textContent="안면인식 실패<br>다시 시도해주세요";
        }
    }
}