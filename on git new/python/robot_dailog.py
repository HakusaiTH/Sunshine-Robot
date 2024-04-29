import os
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'joshu-2-0-iypf'
DIALOGFLOW_LANGUAGE_CODE = 'th'
SESSION_ID = 'me'

# Define intent constants
INTENT_IOT_SL = "iot sl"
INTENT_WEATHER = "สภาพอากาศ"
INTENT_WEATHER_LOCATION = "wether location"
INTENT_PM25_LOCATION = "pm25 location"
INTENT_PM25 = "pm25"
INTENT_CALL_YAK = "call yak"
INTENT_CALL_GPT = "call gpt"

def detect_intent(text_to_be_analyzed):
    client = dialogflow.SessionsClient()
    session = client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = client.detect_intent(request={"session": session, "query_input": query_input})
    except InvalidArgument:
        raise

    re_intent = response.query_result.intent.display_name

    if re_intent == INTENT_CALL_GPT:
        return "gpt"
    if re_intent == INTENT_PM25:
        return "pm25"
    if re_intent == INTENT_WEATHER:
        return "สภาพอากาศ"
    
    if re_intent == INTENT_IOT_SL:
        return handle_iot_intent(response)
        
    if re_intent == INTENT_WEATHER_LOCATION:
        return wether_location(response)
    
    if re_intent == INTENT_PM25_LOCATION:
        return pm25_location(response)
    
    else :
        return "gpt call"

def wether_location(response):
    parameters = response.query_result.parameters

    location = parameters.get('location', None)
    return ["wether_location",location]

def pm25_location(response):
    parameters = response.query_result.parameters

    location = parameters.get('location', None)
    return ["pm25_location",location]

def control_light(room, action):
    led_mapping = {"ไฟนอกห้อง": "led_2", "ไฟในห้อง": "led_1"}
    return led_mapping.get(room, "ไม่มีห้องที่ระบุ"), "ON" if action == "เปิด" else "OFF" if action == "ปิด" else "ไม่มีการทำงาน"


def handle_iot_intent(response):
    parameters = response.query_result.parameters

    value = parameters.get('value', None)
    sta = parameters.get('sta', None)
    
    value, sta = control_light(value, sta)

    return ["iot_call",value, sta]

# print(detect_intent("สภาพอากาศจังหวัดสมุทรสาคร")[0])
# print(detect_intent("เปิดไฟในห้อง"))
'''
    if re_intent == INTENT_CALL_YAK: 
    return "yak"
'''