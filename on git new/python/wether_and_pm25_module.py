# wether_module.py
import requests
from bs4 import BeautifulSoup
import json

def weather():
    weather_url = 'https://aqicn.org/city/thailand/ubon-ratchathani/mueang/nai-mueang/'
    weather_response = requests.get(weather_url)

    soup = BeautifulSoup(weather_response.content, 'html.parser')

    temp_element = soup.find('span', {'class': 'temp'})
    if temp_element:
        temperature = temp_element.text.strip()
    else:
        temperature = 'N/A'

    return f'{temperature} องศาเซลเซียส'

def pm25():
    pm_url = 'https://aqicn.org/city/thailand/ubon-ratchathani/mueang/nai-mueang/'
    pm_response = requests.get(pm_url)

    soup = BeautifulSoup(pm_response.content, 'html.parser')
    aqi_element = soup.find('div', {'class': 'aqivalue'})

    if aqi_element:
        aqi_value = aqi_element.text.strip()
        info_element = soup.find('div', {'id': 'aqiwgtinfo'})

        if info_element:
            info_text = info_element.text.strip()

        output_tuple = aqi_value, info_text
        answer_function = " ".join(str(x) for x in output_tuple)
        return f'{output_tuple[0]} เอคิวไอ'
    else:
        return 'PM2.5 data not available'
    
def find_english_name(thai_name, json_data):
    for entry in json_data:
        if entry["name_th"] == thai_name:
            return entry["name_en"]
    return "Not found"

def wether_location_def(location, data):
    eng_location = find_english_name(location, data)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={eng_location}&appid=21e8f49290c4c4723a092ca40774b36e"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            description = data['weather'][0]['description']
            temp = data['main']['temp'] - 273.15
            humidity = data['main']['humidity']

            return f'จังหวัด {location} {description} สภาพอากาส {temp:.2f}  องศาเซลเซียส ความชื่น {humidity} %'
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return None

def pm25_location_def(location, data):  # Pass 'data' as an argument
    eng_location = find_english_name(location, data)
    api_url = f'http://api.waqi.info/feed/{eng_location}/?token=ce9ee7689a44d93c2250c426c003f14e95fb867c'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'iaqi' in data['data'] and 'pm25' in data['data']['iaqi']:
                pm25_value = data['data']['iaqi']['pm25']['v']
                return f'จังหวัด {location} PM2.5 {pm25_value} aqi'
            else:
                print("PM2.5 data not found in response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return None

# print(pm25_location_def("กรุงเทพมหานคร", data)) 
# print(wether_location_def("กรุงเทพมหานคร", data))