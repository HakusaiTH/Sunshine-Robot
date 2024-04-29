import requests

url = "http://192.168.0.0/snapshot.cgi?user=admin&pwd=fujiwara23121911"

response = requests.get(url)

if response.status_code == 200:
    with open("snapshot.jpg", "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully as snapshot.jpg")
else:
    print("Failed to download image. Status code:", response.status_code)
