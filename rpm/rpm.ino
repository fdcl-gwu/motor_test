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
#define TWI_BLCTRL_BASEADDR 0x2A
#define TWI_BLCTRL_BASEADDR_READ 0x2A

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
}
void send_command(int cmd){
      Wire.beginTransmission(0x2A);
      Wire.write(cmd);
      Wire.endTransmission();
}
void ESC_read(uint8_t *a, uint8_t *b, uint8_t *c, uint8_t *d, uint8_t *e, uint8_t *f) { //, uint8_t *g, uint8_t *h, uint8_t *m){

  Wire.requestFrom(TWI_BLCTRL_BASEADDR_READ, 6); //read 6 out of 9 bytes, all are uint8_t
  *a = Wire.read(); // Current -> current in 0.1 A steps, read back from BL
  *b = Wire.read(); // MaxPWM -> read back from BL -> is less than 255 if BL is in current limit, not running (250) or starting (40)
  *c = Wire.read(); // Temperature -> old Bl-Ctrl (i.e. earlier than 2.0) will return 255 here, the new version the temp in deg C
  *d = Wire.read(); // RPM -> Raw value for RPM
  *e = Wire.read(); // reserved1 -> Voltage (BL3) or mAh for BL2
  *f = Wire.read(); // Voltage -> in 0.1 V (BL3 is limited to 255, BL2 is only low-byte) ?? What does that mean?
  // Remaining 3 bytes not read
  //*g = Wire.read(); // SlaveI2cError; -> BL2 & BL3
  //*h = Wire.read(); // VersionMajor; -> BL2 & BL3
  //*m = Wire.read(); // VersionMinor; -> BL2 & BL3

  // Print to Serial Monitor: Current MaxPWM Temperature RPM reserved1 Voltage
  Serial.print("I2C:");
  Serial.print(*a);
  Serial.print("\t");
  Serial.print(*b);
  Serial.print("\t");
  Serial.print(*c);
  Serial.print("\t");
  Serial.print(*d);
  Serial.print("\t");
  Serial.print(*e);
  Serial.print("\t");
  Serial.print(*f);
  Serial.println();

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
//  Wire.beginTransmission(TWI_BLCTRL_BASEADDR);
//  Wire.endTransmission();

//  delay(1);

  // Read Data from ESC
  byte curr, maxpwm, tmpC, rpm, volt1, volt2;
  ESC_read(&curr, &maxpwm, &tmpC, &rpm, &volt1, &volt2);
   delay(10);
}

void blink() {
  state = !state;
  dt = micros() - timeold;
  timeold = micros();
}
