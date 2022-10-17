/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int pos = 0;    // variable to store the servo position

const int BUTTON_PIN = 3;
int lastState = HIGH;
int currentState;

String nom = "Arduino";
String msg;

String valid_person;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(pos);

  Serial.begin(9600);
  Serial.flush();
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  currentState = digitalRead(BUTTON_PIN);
  if(lastState == HIGH && currentState == LOW){
     activate();
  }
  lastState = currentState;
  delay(500);
}

void activate(){
  Serial.println(1);
  delay(1000);
  Serial.flush();
  valid_person = Serial.readString();
  Serial.flush();
  if (valid_person == "1"){
     myservo.write(180);
     delay(5000);
     myservo.write(0);
  } else {
    myservo.write(0);
  }
}
