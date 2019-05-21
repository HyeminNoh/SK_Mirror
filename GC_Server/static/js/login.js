window.onload(logincheck());
function logincheck(){
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');
    var logindiv = document.getElementById('logindiv');
    console.log("세션값확인 사용자이름:"+username);
    if(username){
        //로그인 되어있는 상태인 것.
        var usertxt = document.createElement('div');
        usertxt.innerHTML="<p style='font-size:25px'>"+username+"님의 스마트미러</p>"
        var logoutbtn = document.createElement('button');
        logoutbtn.className="btn btn-secondary btn-lg";
        logoutbtn.textContent="Logout"
        logoutbtn.onclick = function(){location.href="http://127.0.0.1:8080/logout"};
        logindiv.appendChild(usertxt)
        logindiv.appendChild(logoutbtn)
        var usernametoimage = document.getElementById('usernametxt');
        var usernametocolor = document.getElementById('usernametocolor');
        usernametoimage.value=username;
        usernametocolor.value=username;
    }
    if(!username){
        var loginbtn = document.createElement('button');
        var coment = document.createElement('p');
        coment.textContent="로그인하시면 사용자 업로드 이미지와 컬러도 사용 가능합니다."
        loginbtn.id = "login_btn";
        loginbtn.className="btn btn-secondary btn-lg";
        loginbtn.style.margin="5px";
        loginbtn.innerHTML="Login";
        loginbtn.onclick=function(){
            $("#loginModal").modal();
        };
        logindiv.appendChild(coment);
        logindiv.appendChild(loginbtn);
    }
}

$("#btnLogin").click(function(event) {

    //Fetch form to apply custom Bootstrap validation
    var form = $("#formLogin")

    if (form[0].checkValidity() === false) {
      event.preventDefault()
      event.stopPropagation()
    }
    
    form.addClass('was-validated');
  });
