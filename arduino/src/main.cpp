#include <Arduino.h>
#include <Wire.h>

int OwnI2CAdress = 11;

unsigned int sensorPins[4] = {A0, A1, A2, A3};
unsigned int sensorValues[4] = {0, 0, 0, 0};


// void receiveEvents(int nBytes)
// {  
//   int msg = Wire.read();
// }

void requestEvents()
{
  // Serial.print(F("sending value: "));
  // Serial.println((sensorValue));
  Wire.write(static_cast<char*>(static_cast<void*>(&sensorValues)), 8);
}

void setup()
{
  for (int i; i < 4; i++) {
    pinMode(sensorPins[i], INPUT);
  }  

  Serial.begin(9600);
  
  Wire.begin(OwnI2CAdress);
  delay(1000);
  Wire.onRequest(requestEvents);
}



void loop()
{
  Serial.println("----------------");
  for (int i = 0; i < 4; i++) {
    sensorValues[i] = analogRead(sensorPins[i]);
    Serial.println(sensorValues[i]);
  }

  // delay(500);
}