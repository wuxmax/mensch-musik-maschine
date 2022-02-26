// #include <Arduino.h>

// int sensorValue = 0;
// int sensorPin = A0;
// int ledPin = 13;
// int buzzerPin = 2;

// int startTime = 0;
// int endTime = 0;
// int toneDuration = 500;
// int tonePause = 500;
  
// int thresholdValue = 900;

// void setup()
// {
//   Serial.begin(9600);
//   pinMode(sensorPin, INPUT);
//   pinMode(ledPin, OUTPUT);
// }

// void loop()
// {
//   sensorValue = analogRead(sensorPin);
//   Serial.println(sensorValue);
  
//   endTime = millis();
//   if (sensorValue > thresholdValue && endTime - startTime > toneDuration + tonePause)
//   {
//     digitalWrite(ledPin, HIGH);
//   }
//   else
//   {
//         digitalWrite(ledPin, LOW);
//   }
  
//   // noTone(buzzerPin);
  
//   delay(1); // Delay a little bit to improve simulation performance
// }