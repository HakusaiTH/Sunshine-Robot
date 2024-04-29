// "use strict";
alert("robot online complet !");
console.log("robot online");

const firebaseConfig = {
    apiKey: "AIzaSyAfm-wnbuOAVQESBQASW6iyULVu6-Epr3M",
    authDomain: "my-robot-9fdff.firebaseapp.com",
    databaseURL: "https://my-robot-9fdff-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "my-robot-9fdff",
    storageBucket: "my-robot-9fdff.appspot.com",
    messagingSenderId: "989347540267",
    appId: "1:989347540267:web:cfbfa6664cc4e5d2f0e96e",
    measurementId: "G-LXEWXSLQC5"
};

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var storage = firebase.storage();

const faceImg = document.getElementById("face_img");
const audio = new Audio();

var first_talk = true;

var alert_content = document.getElementById('alert_content');
alert_content.style.display = 'inline-block';

var alertRef = database.ref("/room/A1/Robot/robot_status/ALERT");

var ai_content = document.getElementById('ai_content');
ai_content.style.display = 'none';

function main() {
    var ref = database.ref("/room/A1/Robot/robot_status/sentiment");
    ref.once("value", function (snapshot) {
        var data = snapshot.val();
        if (data == "N") {
            faceImg.src = "/img/N_0.gif";   // /img/N_0.gif  /img/N_0.gif
        } else {
            faceImg.src = `/img/${data}.png`;   // /img/${data}.png /public/img/N_0.gif
        }
    });
    var talkStatusRef = database.ref("/room/A1/Robot/robot_status/talk_status");
    talkStatusRef.once("value", function (snapshot) {
        var talkStatus = snapshot.val();
        if (talkStatus === true) {
            setTimeout(playAudio, 100);
            talkStatusRef.set(false);
        }
    });
    
    var alert_audio = new Audio('/sound/YRL6BSM-siren.mp3');
    alertRef.once("value", function(snapshot) {
        var data = snapshot.val();
        if (data == "ON") {
            alert_audio.play();
            alert_content.style.display = 'inline-block';
        } else {
            alert_content.style.display = 'none';
        }
    });

}

function playAudio() {
    if (first_talk){
        var audioRef = storage.ref("/audio/first.mp3");
    }
    else{
        var audioRef = storage.ref("/audio/output.mp3");
    }
    audioRef.getDownloadURL().then(function (url) {
        console.log("Audio URL:", url);
        audio.src = url;
        audio.play();
    }).catch(function (error) {
        console.error("Error fetching audio:", error);
    });

    first_talk = false;
}

const postData = async (url = '', data = {}) => {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *client
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}
  
const sendDataToAPI = async (post_data) => {
    const url = 'https://85af-49-228-43-213.ngrok-free.app/ai_vision';
    const data = { ai_value: post_data };
    try {
        const response = await postData(url, data);
        console.log('Success:', response);
        
        // Extracting img_url and names from the response
        const imgUrl = response.img_url;
        const names = response.names;
        
        console.log('Image URL:', imgUrl);
        console.log('Detected Names:', names);
        
        document.getElementById('ai_content').style.display = 'inline-block';
        document.getElementById('ai_content_img').src = imgUrl;
        if(post_data == 'face_reco'){
            document.getElementById('ai_content_text').innerHTML = "บุคคลที่พบคือ" + names;
        } else {
            document.getElementById('ai_content_text').innerHTML = "วัตถุที่พบคือ" + names;
        }


    } catch (error) {
        console.error('Error:', error);
    }
}

// face_reco button 
document.getElementById('face_reco').addEventListener('click',()=>{
    sendDataToAPI('face_reco');
});

// object_detect button 
document.getElementById('obj_detect').addEventListener('click',()=>{
    sendDataToAPI('object_detect');
})

main();
setInterval(main, 1000);

document.getElementById("ennable_sound").addEventListener('click', function () {
    document.getElementById("content").style.display = "inline-block";
    document.getElementById("ennable_sound").style.display = "none";
    playAudio();
});

document.getElementById('close').addEventListener('click',()=>{
    alertRef.set("OFF")
    .then(function() {
      console.log("Alert status set to OFF");
    })
    .catch(function(error) {
      console.error("Error setting alert status: ", error);
    });
    alert_content.style.display = 'none';
})

document.getElementById('ai_close').addEventListener('click',()=>{
    document.getElementById('ai_content').style.display = 'none';
})