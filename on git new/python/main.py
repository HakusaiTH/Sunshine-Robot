import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, db, storage
import requests

from wether_and_pm25_module import weather, pm25, wether_location_def, pm25_location_def
from robot_chatbot import answer_question
from robot_dailog import detect_intent
from robot_tts import generate_and_play_audio
from robot_sentiment import analyze_sentiment 
from robot_event import robot_event 
from robot_iot import iot_call
from robot_vision import face_reco, object_detect

# Initialize Firebase
cred = credentials.Certificate('D:\\sanbot_final\\pythonbackend\\my-robot-9fdff-firebase-adminsdk-37upn-709ad75796.json')
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'my-robot-9fdff.appspot.com',
    'databaseURL': 'https://my-robot-9fdff-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

user_room = "A1"
print("user_room:", user_room)

# Function to control LED
def control_led(led_n, led_sta):  
    led_ref = db.reference(f'/room/{user_room}/{led_n}/')
    led_ref.set(led_sta)
    print(f"Set {led_sta} to {led_n}")

def robot_sentiment(content) :
    robot_sentiment_result = analyze_sentiment(content)

    print(robot_sentiment_result)
    robot_sentiment_ref = db.reference(f'/room/{user_room}/Robot/robot_status/sentiment')  # /room/{user_room}/Robot/robot_status/sentiment
    robot_sentiment_ref.set(robot_sentiment_result)

def upload_mp3_to_firebase(file_path, storage_path="audio"):
    bucket = storage.bucket()

    file_name = os.path.basename(file_path)
    destination_path = f"{storage_path}/{file_name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_name} uploaded to Firebase Storage at {destination_path}")

    robot_talk_ref = db.reference(f'/room/{user_room}/Robot/robot_status/talk_status')  # /room/{user_room}/Robot/robot_status/talk_status
    robot_talk_ref.set(True)

# Function to process robot
def process_robot(content,or_not=False):
    print("content:", content)
    if or_not :
        robot_sentiment(content)
    else :
        robot_sentiment_ref = db.reference(f'/room/{user_room}/Robot/robot_status/sentiment')  
        robot_sentiment_ref.set("H")
    
    generate_and_play_audio(content)
    upload_mp3_to_firebase("output.mp3")

with open("thai_provinces.json", "r", encoding="utf-8") as file:
    json_api = json.load(file)
    
# FastAPI instance
app = FastAPI()

# Allow requests from the origin of your web application
origins = [
    "https://my-robot-9fdff.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# API endpoint
@app.post("/receive-data")
async def receive_data(request: Request):
    try:
        data = await request.json()
        talkvalue, sentence = data.get("somevalue"), data.get("sentence")
        print("Received data - somevalue:", talkvalue, "sentence:", sentence)

        # Process robot
        if talkvalue == "t" :
            print("touch robot")
            process_touch_result = robot_event(sentence)  # api อาจจะไม่พอ
            process_robot(process_touch_result,False)

            return {"status": "success", "message": "robot_call"}

        else :
            iot_get = iot_call(sentence)
            iot_talk = iot_get[0]
            if (iot_talk == "unknown_command") :
                value_intent = detect_intent(sentence)

                if value_intent[0] == "wether_location":
                    print("wether_location call")
                    location = value_intent[1]
                    wether_location_result = wether_location_def(location, json_api)
                    process_robot(answer_question(wether_location_result))
                    return {"status": "success", "message": "robot_call"}

                if value_intent[0] == "pm25_location":
                    print("pm25_location call")
                    location = value_intent[1]
                    pm25_location_result = pm25_location_def(location, json_api)
                    process_robot(answer_question(pm25_location_result))
                    return {"status": "success", "message": "robot_call"}

                else  :
                    print("gpt call")
                    process_robot(answer_question(sentence),True)
                    return {"status": "success", "message": "robot_call"}

            else :
                print(iot_talk)
                control_led(iot_get[0], iot_get[1][0])

                return {"status": "success", "message": "robot_call"}
            
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Example usage
known_faces_paths = [
    "D:\\sanbot_final\\pythonbackend\\face_train\\phoovadet.jpg",
    "D:\\sanbot_final\\pythonbackend\\face_train\\ambutakam.jpg"
]

known_names = [
    "phoovadet",
    "ambutakam"
]

def get_camera() :
    url = "http://192.168.0.0/snapshot.cgi?user=admin&pwd=fujiwara23121911"

    response = requests.get(url)

    if response.status_code == 200:
        with open("snapshot.jpg", "wb") as f:
            f.write(response.content)
        return 'D:\\sanbot_final\\pythonbackend\\snapshot.jpg'
    else:
        print("Failed to download image. Status code:", response.status_code)

@app.post("/ai_vision")
async def receive_data(request: Request):
    try:
        data = await request.json()
        ai_value = data.get("ai_value")
        print("Received data - ai_value:", ai_value)
        if ai_value == "face_reco" :
            url_detected_name, detected_names = face_reco(known_faces_paths, known_names, get_camera())
            print(url_detected_name, detected_names)
            process_robot(f'สวัสดีครับคุณ {detected_names[0]}')
            return {"status": "success", "img_url": url_detected_name, "names": detected_names}
    
        if ai_value == "object_detect" :
            url_obj_detected_name, obj_detected_names = object_detect(get_camera())
            print(url_obj_detected_name, obj_detected_names)
            process_robot(f'วัตถุที่ตรวจพบคือ {obj_detected_names}')
            return {"status": "success", "img_url": url_obj_detected_name, "names": obj_detected_names}

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")