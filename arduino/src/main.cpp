#include <Arduino.h>
#include <Wire.h>

int OwnI2CAdress = 11;

int n_sensors = 6;
unsigned int sensorPins[6] = {A0, A1, A2, A3, A6, A7};
unsigned int sensorValues[6] = {0, 0, 0, 0, 0, 0};

// int n_sensors = 4;
// unsigned int sensorPins[4] = {A0, A1, A2, A3};
// unsigned int sensorValues[4] = {0, 0, 0, 0};


// void receiveEvents(int nBytes)
// {  
//   int msg = Wire.read();
// }

void requestEvents()
{
  // Serial.print(F("sending value: "));
  // Serial.println((sensorValue));
  Wire.write(static_cast<char*>(static_cast<void*>(&sensorValues)), n_sensors * 2);
}

void setup()
{
  for (int i; i < n_sensors; i++) {
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
  for (int i = 0; i < n_sensors; i++) {
    sensorValues[i] = analogRead(sensorPins[i]);
    Serial.print(sensorPins[i]);
    Serial.print(": ");
    Serial.println(sensorValues[i]);
  }

  // delay(500);  // TODO: remove!
}