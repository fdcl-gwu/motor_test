#include "Wire.h"
const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = LOW;
volatile int timeold;
volatile int rpm= 0;
volatile int dt= 0;
int send_cmd=0, sensorValue;
int incomingByte = 0;
int analogPin = 0; 
int val = 0;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
}
void send_command(int cmd){
      Wire.beginTransmission(0x29);
      Wire.write(cmd);
      Wire.endTransmission();
}

void loop() {
//  Serial.print(" dt: ");
//  ardprintf("Volt: %d %l %c %s %f", l, k, s, j, f);
//  String dt_str = (String)dt;
  Serial.println(dt);
//  Serial.print("RPM: ");
//  Serial.println(30*1000000/dt);
//  digitalWrite(ledPin, state);
  send_command(send_cmd);
  val = analogRead(analogPin);
  String vol_str = "Voltage:"+(String)val;
  Serial.println(vol_str);
  String cmd_str = "cmd:"+(String)send_cmd;
  Serial.println(cmd_str);
    char buffer[] = {' ',' ',' '};
   if(Serial.available()!=0) {
      Serial.readBytesUntil('n',buffer,3);
      send_cmd = atoi(buffer);
//     Serial.print("cmd: ");
//     Serial.println(send_cmd,DEC);            
   }
   delay(10);
}

void blink() {
  state = !state;
  dt = micros() - timeold;
  timeold = micros();
}
