#include <ArduinoJson.h>
#include <ETH.h>
#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiClient.h>
#include <WiFiGeneric.h>
#include <WiFiMulti.h>
#include <WiFiScan.h>
#include <WiFiServer.h>
#include <WiFiSTA.h>
#include <WiFiType.h>
#include <WiFiUdp.h>
#include <HTTPClient.h>
#include <Wire.h>                                 // Подключаем библиотеку для работы с аппаратной шиной I2C.
#include <iarduino_I2C_Motor.h>                   // Подключаем библиотеку для работы с мотором I2C-flash.
iarduino_I2C_Motor mot(0x09);

#define InPinSensor_1 19
#define InPinSensor_2 23

int sensor1 = 0; //Переменная для хранения значения
int sensor2 = 0;

void loggin(int floor, String controlmode){
  while (!timeClient.update()) {
    timeClient.forceUpdate();
  }

  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;    //Declare object of class HTTPClient

    http.begin("http://983eda387f31.ngrok.io/postjson");      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header

    StaticJsonDocument<200> doc;

    formattedDate = timeClient.getFormattedDate();
    int splitT = formattedDate.indexOf("T");
    dayStamp = formattedDate.substring(0, splitT);
    Serial.println(dayStamp);
    timeStamp = formattedDate.substring(splitT + 1, formattedDate.length() - 1);
    Serial.println(timeStamp);
    
    doc["floor"] = floor;
    doc["controlmode"] = controlmode;
    doc["time"] = timeStamp;
    doc["data"] = dayStamp;

    Serial.println(doc);
    
    String requestBody;
    serializeJson(doc, requestBody);

    int httpCode = http.POST(requestBody);   //Send the request
    String payload = http.getString();                                        //Get the response payload

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

  } else {

    Serial.println("Error in WiFi connection");

  }
}

void setup () {
  mot.begin();
  pinMode(InPinSensor_1, INPUT);
  pinMode(InPinSensor_2, INPUT);
  Serial.begin(115200);
  WiFi.begin("HONOR_20", "1904sunday");

  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.println("Connecting..");

  }
  Serial.println("Connected to WiFi Network");

    timeClient.begin();
  timeClient.setTimeOffset(10800);

}

void loop() {


  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;  //Declare an object of class HTTPClient

    http.begin("http://7fabe3686783.ngrok.io/data"); //Specify request destination

    int httpCode = http.GET(); //Send the request

    if (httpCode > 0) { //Check the returning code

      String payload = http.getString();   //Get the request response payload
      Serial.print("Данные с сервера /data:");
      Serial.println(payload);             //Print the response payload
      if (payload == "0") {
        sensor1 = digitalRead(InPinSensor_1);
        sensor2 = digitalRead(InPinSensor_2);
        Serial.print("Данные датчика на 1 этаже:");
        Serial.println(sensor1);
        Serial.print("Данные датчика на 2 этаже:");
        Serial.println(sensor2);
        mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
        mot.setStop();
      }
      else if (payload == "1") {
        sensor1 = digitalRead(InPinSensor_1);
        sensor2 = digitalRead(InPinSensor_2);
        Serial.print("Данные датчика на 1 этаже:");
        Serial.println(sensor1);
        Serial.print("Данные датчика на 2 этаже:");
        Serial.println(sensor2);
        //если лифт не находится в поле зрения ни одног из датчиков то едем автоматом сначало к 1 этажу
        if ((sensor1 == 1) && (sensor2 == 1)) {
          while (sensor1 == 1) {
            mot.setSpeed(-60, MOT_RPM);
            Serial.println("Лифт плавает, едем на 1й");
            sensor1 = digitalRead(InPinSensor_1);
            Serial.print("Данные датчика на 1 этаже:");
            Serial.println(sensor1);
          }
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
        }
        //если лифт на 2м этаже, то едем на 1й
        if (sensor2 == 0) {
          mot.setSpeed(-60, MOT_RPM);
          Serial.print("Поехали");
          Serial.print("Данные датчика на 1 этаже:");
          Serial.println(sensor1);
          sensor1 = digitalRead(InPinSensor_1);
          while (sensor1 == 1) {
            mot.setSpeed(-60, MOT_RPM);
            sensor1 = digitalRead(InPinSensor_1);
            Serial.print("Данные датчика на 1 этаже:");
            Serial.println(sensor1);
          }
          delay(1000);
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
        }

      }
      else if (payload == "2") {
        sensor1 = digitalRead(InPinSensor_1);
        sensor2 = digitalRead(InPinSensor_2);
        Serial.print("Данные датчика на 1 этаже:");
        Serial.println(sensor1);
        Serial.print("Данные датчика на 2 этаже:");
        Serial.println(sensor2);
        //если лифт не находится в поле зрения ни одног из датчиков то едем автоматом сначало к 1 этажу
        if ((sensor1 == 1) && (sensor2 == 1)) {
          while (sensor1 == 1) {
            mot.setSpeed(-60, MOT_RPM);
            Serial.println("Лифт плавает, едем на 1й");
            sensor1 = digitalRead(InPinSensor_1);
            Serial.print("Данные датчика на 1 этаже:");
            Serial.println(sensor1);
          }
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
        }
        //если лифт на 1м эатже, едем ко 2му
        if (sensor1 == 0) {
          mot.setSpeed( 60, MOT_RPM);
          Serial.print("Поехали");
          sensor2 = digitalRead(InPinSensor_2);
          while (sensor2 == 1) {
            mot.setSpeed( 60, MOT_RPM);
            sensor2 = digitalRead(InPinSensor_2);
            Serial.print("Данные датчика на 2 этаже:");
            Serial.println(sensor2);

          }
          delay(2000);
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
        }

      }
      else if (payload == "A") {
        sensor1 = digitalRead(InPinSensor_1);
        sensor2 = digitalRead(InPinSensor_2);
        Serial.print("Данные датчика на 1 этаже:");
        Serial.println(sensor1);
        Serial.print("Данные датчика на 2 этаже:");
        Serial.println(sensor2);
        if (sensor1 == 0) {
          mot.setSpeed( 20, MOT_RPM);

          while (sensor2 == 1) {
            mot.setSpeed( 20, MOT_RPM);
            sensor2 = digitalRead(InPinSensor_2);

          }
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
          delay(10000);
        }
        if (sensor2 == 0) {
          mot.setSpeed( -20, MOT_RPM);

          while (sensor1 == 1) {
            mot.setSpeed( -20, MOT_RPM);
            sensor1 = digitalRead(InPinSensor_1);

          }
          mot.setStopNeutral(true);                     // Указываем освободить мотор при его остановке. Ротор остановленного мотора можно вращать.
          mot.setStop();
          delay(10000);

        }
      }


      else {
        Serial.println("An error ocurred in data");

      }
    }

    else {
      Serial.println("An error ocurred in get request");
    }

    http.end();
  }   //Close connection




  delay(10000);    //Send a request every 10 seconds

}
