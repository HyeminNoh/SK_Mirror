// db 메모 데이터 로드 후 view 반영
window.onload(makeMemobox());

function makeMemobox(){
    // get JSON with using pure javascript
    var request= new XMLHttpRequest();

    //var url= "https://us-central1-backup-c8eab.cloudfunctions.net/app/memodata?username=?ysss";
    var url= "http://127.0.0.1:8080/memodata";
    request.open("GET", url);
    request.responseType='json';
    request.send();
    request.onload = function() {
        var memodata = request.response;
        console.log(memodata);
        var memobody = document.getElementById('memo');
        for (var i = 0; i < Object.keys(memodata).length; i++) {
            row = memobody.insertRow(memobody.rows.length);
            row.style.fontSize="20px"

            icon = row.insertCell(0);
            text = row.insertCell(1);

            var keys = Object.keys(memodata);
            var content = memodata[keys[i]].write;
            console.log(content);
            icon.innerHTML = '<i class="far fa-check-square"></i>';
            text.innerHTML = content;
        }
    }
}