#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include<Wire.h>
#include<LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);
int red1=D5;
int green1=D6;
int red2=D8;
int green2=D7;

HTTPClient http;    //Declare object of class HTTPClient
String sensorData1,sensorData2,sensorData3,sensorData4,sensorData5,sensorData6,sensorData7, postData;
const char *ssid = "project12345";  //ENTER YOUR WIFI ssid
const char *password = "project12345";//UR WIFI password
String myString;

void setup() {

  pinMode(red1,OUTPUT);
  pinMode(green1,OUTPUT);
  pinMode(red2,OUTPUT);
  pinMode(green2,OUTPUT);
  digitalWrite(red1,LOW);
  digitalWrite(green1,HIGH);
  digitalWrite(red2,LOW);
  digitalWrite(green2,HIGH);
  Serial.begin(9600);
   WiFi.begin(ssid, password);   

   lcd.init();
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("     Harbin bend       ");
  lcd.setCursor(0,1);
  lcd.print("     Detection          ");
}

void loop() {
  getcode();
  delay(3000);
}


void getcode()
{
      WiFiClient client1;
      HTTPClient http1;
  
      String serverName = "http://api.thingspeak.com/channels";
      String serverPath = serverName + "/2495982/fields//1/last";
      
      // Your Domain name with URL path or IP address with path
      http1.begin(client1, serverPath.c_str());
  
      // If you need Node-RED/server authentication, insert user and password below
      //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
        
      // Send HTTP GET request
      int httpResponseCode = http1.GET();
      
      if (httpResponseCode>0) {
       // Serial.print("HTTP Response code: ");
        //Serial.println(httpResponseCode);
        String payload = http1.getString();
        Serial.println(payload);
        if (payload.toInt()==1)
        {
          digitalWrite(red1,LOW);
          digitalWrite(green1,HIGH);
          digitalWrite(red2,HIGH);
          digitalWrite(green2,LOW);
          lcd.print("     Harbin 1       ");
          lcd.setCursor(0,1);
          lcd.print("  vehcile detected          ");
                  
        }
        if (payload.toInt()==2)
        {
              digitalWrite(red1,HIGH);
              digitalWrite(green1,LOW);
              digitalWrite(red2,LOW);
              digitalWrite(green2,HIGH);
              lcd.print("     Harbin 2      ");
              lcd.setCursor(0,1);
              lcd.print("  Vehicle  Detected         ");
          
        }
        if (payload.toInt()==0)
        {
                digitalWrite(red1,LOW);
              digitalWrite(green1,HIGH);
              digitalWrite(red2,LOW);
              digitalWrite(green2,HIGH);
               lcd.print(" Harbin 1 and 2   ");
              lcd.setCursor(0,1);
              lcd.print("      Free          ");
          
        }
      http1.end();
    }
    delay(1000);
  }
