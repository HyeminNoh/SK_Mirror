/*
var express = require('express');
var http = require('http');
var app = express();
var server = http.createServer(app);


app.get('/', function(req, res){
    //res.send('root page');
    res.sendFile(__dirname + '/public/index.html');
});

app.get('/start', function(req, res){
    res.send('start page');
});

server.listen(3000, function(){
    console.log('Server listen on port' + server.address().port)
})
*/

/*

(function() {
    var firebase = require("firebase");
    require('firebase/database');
    var jsdom = require("jsdom");
    var JSDOM = jsdom.JSDOM;
    
    var admin = require("firebase-admin");
    
// Initialize Firebase
    const config = {
        apiKey: "AIzaSyAuy0TzbGG0UH8_vu583ommMSub_kNArEE",
        authDomain: "backup-c8eab.firebaseapp.com",
        databaseURL: "https://backup-c8eab.firebaseio.com",
        projectId: "backup-c8eab",
        storageBucket: "backup-c8eab.appspot.com",
        messagingSenderId: "543005010393"
    };
    firebase.initializeApp(config);

*/

/*
var ref = firebase.database().ref("/memos");                          
ref.on('value', function(snapshot){
    output.innerHTML = JSON.stringify(snapshot.val(), null, 2);
});
*/

/*
var query = firebase.database().ref("/memos").orderByKey();
query.once("value")
  .then(function(snapshot) {
    snapshot.forEach(function(childSnapshot) {
      // key will be "ada" the first time and "alan" the second time
      var key = childSnapshot.key;
      // childData will be the actual contents of the child
      var childData = childSnapshot.val();
  });
});
*/
/*
var admin = require("firebase-admin");


var serviceAccount = require("./backup-c8eab-firebase-adminsdk-f1n3v-e5b11fd78f.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://backup-c8eab.firebaseio.com"
});

    var db = admin.database();
    var ref = db.ref("/memos");
    ref.once("value", function(snapshot) {
      //output.innerHTML = JSON.stringify(snapshot.val(), null, 2);
      console.log(snapshot.val());
      output.innerHTML = JSON.stringify(snapshot.val(), null, 2);
    });
*/

/*
    const preObject = document.getElementById('object');
     // database 참조를 만들어서 data를 실시간으로 동기화해보자.
     // create references
    const dbRefObject = db.ref().child('/memos');
    dbRefObject.on('value', snap => preObject.innerText = JSON.stringify(snap.val(), null, 3));
*/
/*
const dom = new JSDOM(`<body>
  <script>document.body.appendChild(document.createElement("object"));</script>
</body>`, { runScripts: "dangerously" });

// The script will be executed and modify the DOM:
//dom.window.document.body.children.length === 100;

const preObject = new JSDOM.window.getElementById('object');
//document.onkeydown = move;
var dbRefObject = firebase.database().ref('/memos');

dbRefObject.on('value', snap=>{
     // on()는 객체가 변할 때마다 동기화 함
	  // on() 1번 파라미터 : 이벤트 타입(데이터 베이스의 데이터를 어느 단계까지 동기화 할 것인가 결정)
	  // value는 데이터베이스(해당 로케이션)에 변경이 있을 때마다 함수를 호출 하는 것
	  // on() 2번 파라미터 : 콜백 함수
	  dom.innerText = JSON.stringify(snap.val(), null, 100);
});


  // get element
  const preObject = document.getElementById('object');
  // database 참조를 만들어서 data를 실시간으로 동기화해보자.
  // create references
  const dbRefObject = firebase.database().ref().child('/memos');
  dbRefObject.on('value', snap => preObject.innerText = JSON.stringify(snap.val(), null, 3)); // 여백 3
})();

*/

var express = require('express');
var app = express();

var admin = require("firebase-admin");
var serviceAccount = require("./backup-c8eab-firebase-adminsdk-f1n3v-e5b11fd78f.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://backup-c8eab.firebaseio.com"
});

   var db = admin.database();
   // var ref = db.ref("/memos");


app.get('/', function(req, res){
  console.log("Http Get Request");
  var memoReference = db.ref("/memos");
  memoReference.on("value",
    function(snapshot){
      console.log(snapshot.val());
      res.json(snapshot.val());
      memoReference.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});

app.get('/memo', function(req, res){
 /*
  var memodata = db.ref('/memos').orderByChild('tomirror')
              .equalTo(true).once("value", function(snapshot){
                console.log(snapshot.val());
                res.send(snapshot.val());
              }); // 메모 참 데이터
 */
                     
  //console.log(memodata);
  var memodata = db.ref('/memos');
  memodata.orderByChild('tomirror').equalTo("true").on("value", function(snapshot){
    console.log(snapshot.val());
  });   
});

  //to handle HTTP get request
app.get('/about', function (req, res) {
  console.log("Get about");
  res.send("Get about");
});
  


  //start server on port: 8080
  var server = app.listen(3000, function () {
  
    var host = server.address().address;
    var port = server.address().port;
  
    console.log("server listening at http://%s:%s", host, port);
  });

