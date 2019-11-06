// // Create and Deploy Your First Cloud Functions   --- default
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
//exports.helloWorld = functions.https.onRequest((request, response) => {
//response.send("Hello from Firebase!");
//});
const functions = require('firebase-functions');
var admin = require('firebase-admin');
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
//var mime = require('mime');
var cors = require('cors'); 
//var fs = require('fs');
var engines = require('consolidate');
var url = require('url');
//let {PythonShell} = require('python-shell');
//var router = require('./router/main')(app);

const path = require('path');
var routes = require('./router/main');

var serviceAccount = require();

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://backup-c8eab.firebaseio.com"
});


//파이썬 실행 옵션
//파이썬 실행 옵션
let options = {
  mode: 'text',
  pythonPath: '',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: '',
  args: ['value1']
};

// Automatically allow cross-origin requests
app.use(cors());


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended : true}));

// view 경로 설정
app.set('views', path.join(__dirname, '/views'));

// 화면 engine을 html로 설정
app.engine('html', engines.mustache);
app.set('view engine', 'html');

// 기본 path를 /public으로 설정(css, javascript 등의 파일 사용을 위해)
app.use(express.static(path.join(__dirname, '/public')));
/*
app.set('views',path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);
*/

app.use('/', routes);

var db = admin.database();

var image = db.ref('images');
var baseimage = db.ref('baseimage');

//이미지 리스트 출력화면
app.get('/baseimagelist', function(req, res){
  console.log("Http Get Request");
  
  baseimage.on("value",
    function(snapshot){
      console.log(snapshot.val());
      //res.send(snapshot.val());
      res.json(snapshot.val());
      baseimage.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});

//이미지 snap화면 전송 (json key값 snap, 그안에 base64인코딩 이미지)
app.get('/matchingsnap', function(req, res){
  console.log("Http Get Request");
  //res.send(binaryimg);
});

//이미지매칭 파이썬 실행 종료 명령전달
app.post('/endstreaming', function(req, res){
  //python-shell 스크립트 종료시키기 ('q' 전달)
  
});

/*
app.get('/images', function(req, res){
  image.child('Ig1o1aP8EgZW2HXjoGfTAaJYGgp1')
  .on("value", function(snapshot){
      console.log(snapshot.val());
      res.send(snapshot.val());
      //res.json(snapshot.val());
      memoReference.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});
*/

app.get('/memodata', function(req,res){
  var parseObj = url.parse(req.url, true);
  var username = parseObj.query.username;
  var memodata = db.ref('memos').child(username).orderByChild('tomirror').equalTo('true')
  .once("value", function(snapshot){
    console.log(snapshot.val());
    res.json(snapshot.val());
  });
});


//이미지 리스트 출력화면
app.get('/seletedimage', function(req, res){
  console.log("Http Get Request");
  
  var parseObj = url.parse(req.url, true);
  var imgname = parseObj.query.name;
  console.log(imgname);
  baseimage.child('test').orderByChild('img_name').equalTo(imgname)
  .on("value", function(snapshot){
      console.log(snapshot.val());
      //res.send(snapshot.val());
      res.json(snapshot.val());
      baseimage.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});

app.get('/users', function(req, res){
  db.ref('users').on("value",
    function(snapshot){
      console.log(snapshot.val());
      res.json(snapshot.val());
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});

app.get('/useraddress', function(req,res){
  var memodata = db.ref('users').child('Ig1o1aP8EgZW2HXjoGfTAaJYGgp1')
  .once("value", function(snapshot){
    console.log(snapshot.val());
    res.json(snapshot.val());
  });
});


//이미지 리스트 출력화면
app.get('/images', function(req, res){
  console.log("Http Get Request");
  
  var parseObj = url.parse(req.url, true);
  var username = parseObj.query.username;
  
  db.ref('images').child(username)
  .on("value", function(snapshot){
    console.log(snapshot.val());
    res.json(snapshot.val());
  });
  /*
 var parseObj = url.parse(req.url, true);
 var username = parseObj.query.username;
  console.log(username);
 var imagedata = db.ref().child('/images').orderByChild(username)
 .once("value", function(snapshot){
  console.log(snapshot.val());
  res.send(snapshot.val());
}); // 메모 참 데이터*/
/*
 let result = [];
 var imagedata = db.ref('/images').on("value", (snapshot) => {
   snapshot.forEach((child) => {
      let childRef = child.ref;
     childRef.on("value", (childSnapShot) => {
       if (childSnapShot.val() !== null) {
         result.push(childSnapShot.val())
       }
     });
   });

  res.json(result);
}); */
});


exports.app = functions.https.onRequest(app);

/*
//이미지 선택 후 해당이미지의 파싱이미지를 전송하며 python 실행
app.post('/imagematching', function(req, res){
  //console.log("post data :", req.body);
  res.sendFile('../views/imagematching.html');
  //파이썬 파일 실행....python shell matching image data 전송하기
  //PythonShell.run('../pyscript/ImageMatching.py', options, function (err, results) {
   // if (err) throw err;
    // results is an array consisting of messages collected during execution
      
  //});
});
*/


/*
app.get('/memodata', function(req, res){
  let result = [];
  var memodata = db.ref('/memos').on("value", (snapshot) => {
    snapshot.forEach((child) => {

      let childRef = child.ref;
      childRef.orderByChild('tomirror').equalTo('true').on("value", (childSnapShot) => {
        if (childSnapShot.val() !== null) {
          result.push(childSnapShot.val())
        }
      });
    });
    console.log(result);
    res.json(result);
  }); 
});*/

/*
app.get('/images', function(req, res){
  console.log("Http Get request image list JSON data");
  image.on("value",
    function(snapshot){
     
      console.log(snapshot.val());
      res.send(snapshot.val());
      //res.json(snapshot.val());
      memoReference.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});*/
