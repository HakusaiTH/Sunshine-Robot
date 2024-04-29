import os
from fastapi import FastAPI, HTTPException, Request
from wether_and_pm25_module import weather, pm25
from robot_chatbot import answer_question
from robot_dailog import detect_intent
from robot_tts import generate_and_play_audio
from robot_sentiment import analyze_sentiment 
from robot_event import process_touch 
from robot_iot import iot_call

import firebase_admin
from firebase_admin import credentials, db, storage

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
def process_robot(content,or_not):
    print("content:", content)
    if or_not :
        robot_sentiment(content)
    else :
        robot_sentiment_ref = db.reference(f'/room/{user_room}/Robot/robot_status/sentiment')  
        robot_sentiment_ref.set("H")
    
    if generate_and_play_audio(content) :
        upload_mp3_to_firebase("output.mp3")

# FastAPI instance
app = FastAPI()

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
            process_touch_result = process_touch(sentence)  # api อาจจะไม่พอ
            process_robot(process_touch_result,False)

            return {"status": "success", "message": "robot_call"}

        else:
            iot_get = iot_call(sentence)
            iot_talk = iot_get[0]
            if (iot_talk == "unknown_command") :
                value_intent = detect_intent(sentence)

                if value_intent in ["สภาพอากาศ", "pm25"]:
                    print(f"{value_intent} call")
                    process_robot(weather() if value_intent == "สภาพอากาศ" else pm25(),False)
                    return {"status": "success", "message": "robot_call"}

                else:
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
