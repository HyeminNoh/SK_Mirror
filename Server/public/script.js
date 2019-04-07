var firebase = require("firebase");


// Initialize Firebase
var config = {
    apiKey: "AIzaSyAuy0TzbGG0UH8_vu583ommMSub_kNArEE",
    authDomain: "backup-c8eab.firebaseapp.com",
    databaseURL: "https://backup-c8eab.firebaseio.com",
    projectId: "backup-c8eab",
    storageBucket: "backup-c8eab.appspot.com",
    messagingSenderId: "543005010393"
};
firebase.initializeApp(config);

/*
var ref = firebase.database().ref("/memos");                          
ref.on('value', function(snapshot){
    output.innerHTML = JSON.stringify(snapshot.val(), null, 2);
});*/

const preObject = document.getElementById('memos');
const dbRefObject = firebase.database().ref.child('memos');

dbRefObject.on('value', snap=>{
     // on()는 객체가 변할 때마다 동기화 함
	  // on() 1번 파라미터 : 이벤트 타입(데이터 베이스의 데이터를 어느 단계까지 동기화 할 것인가 결정)
	  // value는 데이터베이스(해당 로케이션)에 변경이 있을 때마다 함수를 호출 하는 것
	  // on() 2번 파라미터 : 콜백 함수
	  preObject.innerText = JSON.stringify(snap.val(), null, 3);
})

/*
var rootRef = firebase.database().ref();
rootRef.on('child_added', function(data){
	console.log(data.val())
});
*/

