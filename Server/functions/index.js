// // Create and Deploy Your First Cloud Functions   --- default
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
//exports.helloWorld = functions.https.onRequest((request, response) => {
//response.send("Hello from Firebase!");
//});

const functions = require('firebase-functions');
var express = require('express');
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

PythonShell.PythonShell.run('..\open_cv\ImageMatching.py', function (err, results) {
    if (err) throw err;
    console.log('results: %j', results);
});
    
app.post("/ImageMatching", (req, res) => {
      var msg=req.body.msg;
      console.log("python: " + msg);
      res.send("process complete");
});
   
app.listen(5001);