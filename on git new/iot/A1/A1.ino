#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "FF1_15"
#define WIFI_PASSWORD "123456789"

// Insert Firebase project API Key
#define API_KEY "AIzaSyAfm-wnbuOAVQESBQASW6iyULVu6-Epr3M"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://my-robot-9fdff-default-rtdb.asia-southeast1.firebasedatabase.app/" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
bool signupOK = false;

int siren = D1;
int light = D2;
int analogPin = A0;
int val = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("ok");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  pinMode(light, OUTPUT);  // sets the pin as output
  digitalWrite(light, HIGH);

  pinMode(siren, OUTPUT);
}

bool alert_sta = true;

void loop() {
  val = analogRead(analogPin);  //อ่านค่าสัญญาณ analog 
  Serial.print("val = "); // พิมพ์ข้อมความส่งเข้าคอมพิวเตอร์ "val = "
  Serial.println(val); // พิมพ์ค่าของตัวแปร val
  if (val > 500) { // สามารถกำหนดปรับค่าได้ตามสถานที่ต่างๆ
    Serial.println("ALERT");
    if (Firebase.RTDB.setString(&fbdo, "/room/A1/Robot/robot_status/ALERT", "ON")) {
      Serial.println("Alert status set to ON");
    } else {
      Serial.println(fbdo.errorReason());
    }
    digitalWrite(light, HIGH); // สั่งให้ LED ติดสว่าง
    digitalWrite(siren, HIGH);
    alert_sta = true;
  } else {
    Serial.println("NOT ALERT");
    if(alert_sta){
      if (Firebase.RTDB.setString(&fbdo, "/room/A1/Robot/robot_status/ALERT", "OFF")) {
        Serial.println("Alert status set to ON");
      } else {
        Serial.println(fbdo.errorReason());
      }   
      alert_sta = false;
    }
  }
  
  if (Firebase.RTDB.getString(&fbdo, "/room/A1/led_1")) {
    String light_value = fbdo.stringData();
    Serial.println(light_value);
    if(light_value == "ON"){
      digitalWrite(light, LOW); // ส่งให้ไฟติด
    } else {
      digitalWrite(light, HIGH); // ส่งให้ไฟดับ
    }
  }
  else {
    Serial.println(fbdo.errorReason());
  }
  delay(1000);
}
