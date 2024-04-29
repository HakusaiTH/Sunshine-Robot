import requests

# talk 
'''
url = "https://5b1f-101-109-251-216.ngrok-free.app" + "/receive-data"
while True :

    user_input = input("input :")   # "สภาพอากาศจังหวัดอุบล"

    data = {
        "somevalue": "gpt call",
        "sentence": user_input
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("Failed to send data. Status code:", response.status_code)
'''

#ai 
url = "https://85af-49-228-43-213.ngrok-free.app" + "/ai_vision"

data = {
    "ai_value": "object_detect"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Data sent successfully")
else:
    print("Failed to send data. Status code:", response.status_code)

