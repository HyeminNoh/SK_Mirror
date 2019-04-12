
const functions = require('firebase-functions');
var express = require('express');
var app = express();
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);
/*
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://backup-c8eab.firebaseio.com"
});

*/
var db = admin.database();

var memos = db.ref('memos').orderByChild('tomirror').equalTo('true');
var image = db.ref('images');
var baseimage = db.ref('baseimage');
var user = db.ref('users');

app.get('/image', function(req, res){
  console.log("Http Get Request");
  image.on("value",
    function(snapshot){
      
      console.log(snapshot.val());
      res.send(snapshot.val());
      image.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});

app.get('/baseimage', function(req, res){
  console.log("Http Get Request");
  
  baseimage.on("value",
    function(snapshot){
     
      console.log(snapshot.val());
      res.send(snapshot.val());
      baseimage.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});


app.get('/users', function(req, res){
  console.log("Http Get Request");
  user.on("value",
    function(snapshot){
      console.log(snapshot.val());
      res.send(snapshot.val());
      user.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});



app.get('/imgurl', function(req, res){
  console.log("Http Get Request");
  image.orderByChild('img_file').startAt('http').on("value", 
      function(snapshot) {
          console.log(snapshot.val());
          res.send(snapshot.val());
});
});

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
});


exports.app = functions.https.onRequest(app);



/*
app.get('/imgurl', function(req, res){
  console.log("Http Get Request");
  var memoReference = image.child("img_file");
  memoReference.on("value",
    function(snapshot){
      console.log(snapshot.val());
      res.send(snapshot.val());
      memoReference.off("value");
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });
});
*/

/*
  var memoReference = image.orderByChild("img_file");
  memoReference.on("value",
    function(snapshot){
      snapshot.val();
      console.log(snapshot.val());
      res.send(snapshot.val());
    },
    function (errorObject) {
      console.log("The read failed: " + errorObject.code);
      res.send("The read failed: " + errorObject.code);
   });*/




/*
memos.orderByChild("tomirror").equalTo("true")
   .on("value", function(snapshot) {
     console.log(snapshot.val());
     res.json(snapshot);
    });

*/
