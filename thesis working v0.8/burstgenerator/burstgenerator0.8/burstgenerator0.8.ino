#include <SerialCommand.h>
#include <MCP23017.h>
#include "si5351.h"
#include <Wire.h>
#include <AccelStepper.h>
#include <LiquidCrystal.h>
#define MCP23017_I2C_ADDRESS 0x20
#include <movingAvg.h>
MCP23017 mcp23017 = MCP23017(MCP23017_I2C_ADDRESS);
SerialCommand sCmd;
Si5351 si5351;
int dirPin = 49;
int pulPin = 48;
long initial_homing = -1;
int interruptPin = 52;
AccelStepper stepper(AccelStepper::DRIVER, pulPin, dirPin);
int LdirPin = 42;
int LpulPin = 43;
int interruptPin2 = 53;
AccelStepper Lstepper(AccelStepper::DRIVER, LpulPin, LdirPin);
//LCD RS pin to digital pin 12
//LCD Enable pin to digital pin 11
//LCD D4 pin to digital pin 5
//LCD D5 pin to digital pin 4
//LCD D6 pin to digital pin 3
//LCD D7 pin to digital pin 2
//LCD R/W pin to ground
const int rs = 50, en = 51, d4 = 47, d5 = 46, d6 = 45, d7 = 44;
LiquidCrystal vfd(rs, en, d4, d5, d6, d7);
//LiquidCrystal vfd(50, 51, 44, 45, 46, 47);
const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 10;
const int M1 = 12;
const int M0 = 11;
const int blLP = 15;
const int irLP = 14;
const int pmtena = 22;
const int STARTIN = 9;
const int pmtv = A0;
const int ROTARYENABLE = 40;
const int LINEARENABLE = 41;
String inString = "";
String controlString = "";
uint16_t aNumberrec;
uint16_t aNumber;
uint16_t binNumber;
uint64_t freqrec;
movingAvg pmtbias(50);

void setup() {
  pinMode(WE, OUTPUT);
  pinMode(XTR, OUTPUT);
  pinMode(MR, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M0, OUTPUT);
  pinMode(irLP, OUTPUT);
  pinMode(blLP, OUTPUT);
  pinMode(pmtena, OUTPUT);
  pinMode(STARTIN, OUTPUT);
  pinMode(LINEARENABLE, OUTPUT);
  pinMode(ROTARYENABLE, OUTPUT);
  pinMode(interruptPin, INPUT);
  pinMode(interruptPin2, INPUT);
  pinMode(pmtv, INPUT);
  digitalWrite(M2, HIGH);
  digitalWrite(M1, HIGH);
  digitalWrite(M0, LOW);
  digitalWrite(STARTIN, LOW);
  digitalWrite(pmtena, HIGH);
  digitalWrite(irLP, HIGH);
  digitalWrite(blLP, HIGH);
  Serial.begin(9600);
  sCmd.addCommand("P",     countNumber);
  sCmd.addCommand("F",     frequencyCommand);
  sCmd.addCommand("L", latch);
  sCmd.addCommand("START", writepulse);
  sCmd.addCommand("IRPOWER", irledPoweron);
  sCmd.addCommand("IRPOWERO", irledPoweroff);
  sCmd.addCommand("BLPOWER", blPoweron);
  sCmd.addCommand("BLPOWERO", blPoweroff);
  sCmd.addCommand("PMTEN", pmten);
  sCmd.addCommand("PMTDIS", pmtdis);
  sCmd.addCommand("HOME",    homing);
  sCmd.addCommand("ONE",   sampleone);
  sCmd.addCommand("TWO",   sampletwo);
  sCmd.addCommand("THREE",   samplethree);
  sCmd.addCommand("FOUR",   samplefour);
  sCmd.addCommand("FIVE",   samplefive);
  sCmd.addCommand("SIX",   samplesix);
  sCmd.addCommand("SEVEN",   sampleseven);
  sCmd.addCommand("EIGHT",   sampleeight);
  sCmd.addCommand("LHOME", lhoming);
  sCmd.addCommand("EJECT", eject);

  Wire.begin();
  mcp23017.init();
  mcp23017.portMode(MCP23017Port::A, 0b00000000);
  mcp23017.portMode(MCP23017Port::B, 0b00000000);
  mcp23017.writeRegister(MCP23017Register::GPIO_A, 0x00);
  mcp23017.writeRegister(MCP23017Register::GPIO_B, 0x00);
  si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_8MA);
  vfd.begin(24, 2);
  pmtbias.begin();
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(20000);
  Lstepper.setMaxSpeed(1000);
  Lstepper.setAcceleration(20000);
  initialhoming();
  analogReference(INTERNAL2V56);
  Serial.println("Ready");
  vfd.clear();
  vfd.write("System Ready");
}

void countNumber() {
  char *arg;
  arg = sCmd.next();
  if (arg != NULL) {
    aNumberrec = atoi(arg);
    aNumber = aNumberrec + 1;
    uint16_t invertA = reverse_bits(aNumber);
    uint8_t bNumber = aNumber >> 8;
    uint8_t invertB = reverse_bits(bNumber);
    uint8_t cNumber = aNumber;
    uint8_t invertC = reverse_bits(cNumber);
    mcp23017.writePort(MCP23017Port::B, invertC);
    mcp23017.writePort(MCP23017Port::A, invertB);
    Serial.println("number received");
    Serial.println("invertC");
    Serial.println(invertC);
    Serial.println("imvertB");
    Serial.println(invertB);
  }
  vfd.clear();
  vfd.write("Pulse Count Received");
}
void latch() {
  char *arg;
  arg = sCmd.next();
  if (arg != NULL) {
    binNumber = atoi(arg);
  }
  digitalWrite(MR, LOW);
  delay(100);
  digitalWrite(MR, HIGH);
  digitalWrite(WE, LOW);
  delay(100);
  digitalWrite(WE, HIGH);
  Serial.println("latched");
  vfd.clear();
  vfd.write("System Armed");
}
void writepulse() {
  uint64_t passnumber;
  uint32_t delaytime;
  char *arg;
  vfd.clear();
  vfd.write("Experiment Running");
  arg = sCmd.next();
  controlString += arg;
  if (controlString != NULL) {
    passnumber = controlString.toInt();    // Converts a char string to an integer
  }
  arg = sCmd.next();
  if (arg != NULL) {
    delaytime = atol(arg);
  }
  for (uint64_t i = 0; i <= (passnumber - 1); i++) {
    digitalWrite(XTR, HIGH);
    digitalWrite(STARTIN, HIGH);
    _NOP();
    digitalWrite(STARTIN, LOW);
    delayMicroseconds(delaytime);
    delay(binNumber);
    digitalWrite(XTR, LOW);
  }
  controlString = "";
  vfd.clear();
  vfd.write("Experiment Done");
}
byte reverse_bits(byte inverting) {
  byte  rtn = 0;
  for (byte i = 0; i < 8; i++) {
    bitWrite(rtn, 7 - i, bitRead(inverting, i));
  }
  return rtn;
}
void movingavg() {
  int raw = analogRead(pmtv); // read the photocell
  float biasvoltage = raw * 2.5;
  int avg = pmtbias.reading(biasvoltage);    // calculate the moving average
  //Serial.println(avg);                // print the moving average
  vfd.setCursor(20, 2);
  vfd.println(avg);
  delay(100);
}
void initialhoming() {
  vfd.clear();
  vfd.write("Homing");
  digitalWrite(LINEARENABLE, HIGH);
  while (digitalRead(interruptPin2)) {
    Lstepper.move(10850);
    Lstepper.run();
  }
  Lstepper.setCurrentPosition(0);
  digitalWrite(LINEARENABLE, LOW);
  digitalWrite(ROTARYENABLE, HIGH);
  while (digitalRead(interruptPin)) {
    stepper.moveTo(11000);
    stepper.run();
    delay(5);
  }
  stepper.setCurrentPosition(0);
  digitalWrite(ROTARYENABLE, LOW);
}
void pmten() {
  digitalWrite(pmtena, LOW);
}
void pmtdis() {
  digitalWrite(pmtena, HIGH);
}
void irledPoweron() {
  digitalWrite(irLP, LOW);
}
void irledPoweroff() {
  digitalWrite(irLP, HIGH);
}
void blPoweron() {
  digitalWrite(blLP, LOW);
}
void blPoweroff() {
  digitalWrite(blLP, HIGH);
}
void frequencyCommand() {
  char *argu;
  argu = sCmd.next();
  inString += argu;
  if (inString != NULL) {
    freqrec = (inString.toInt());
    freqrec = freqrec * 100;
    si5351.set_freq(freqrec, SI5351_CLK0);
    si5351.update_status();
    inString = "";
    vfd.clear();
    vfd.write("Dwell Time Received");
    Serial.println("freq received");
    sCmd.readSerial();
  }
}
void lhoming() {
  digitalWrite(LINEARENABLE, HIGH);
  vfd.clear();
  vfd.write("Loading Tray");
  while (digitalRead(interruptPin2)) {
    Lstepper.move(10850);
    Lstepper.run();
  }
  vfd.clear();
  vfd.write("Tray Loaded");
  Lstepper.setCurrentPosition(0);
  digitalWrite(LINEARENABLE, LOW);
}
void eject() {
  digitalWrite(LINEARENABLE, HIGH);
  vfd.clear();
  vfd.write("Ejecting Tray");
  Lstepper.moveTo(-10350);
  Lstepper.runToPosition();
  Lstepper.run();
  delay(5);
  vfd.clear();
  vfd.write("Tray Ejected");
  digitalWrite(LINEARENABLE, LOW);
}
void homing() {
  digitalWrite(ROTARYENABLE, HIGH);
  vfd.clear();
  vfd.write("Rotary Homing");
  while (digitalRead(interruptPin)) {
    stepper.moveTo(11000);
    stepper.run();
    delay(5);
  }
  stepper.setCurrentPosition(0);
  vfd.clear();
  vfd.write("Rotary Home");
  digitalWrite(ROTARYENABLE, LOW);
}
void sampleone() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  delay(5);
  vfd.clear();
  vfd.write("Sample One");
  digitalWrite(ROTARYENABLE, LOW);
}
void sampletwo() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-200);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Two");
  digitalWrite(ROTARYENABLE, LOW);
}
void samplethree() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-420);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Three");
  digitalWrite(ROTARYENABLE, LOW);
}
void samplefour() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-600);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Four");
  digitalWrite(ROTARYENABLE, LOW);
}
void samplefive() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-820);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Five");
  digitalWrite(ROTARYENABLE, LOW);
}
void samplesix() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-1000);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Six");
  digitalWrite(ROTARYENABLE, LOW);
}
void sampleseven() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-1210);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Seven");
  digitalWrite(ROTARYENABLE, LOW);
}
void sampleeight() {
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  stepper.moveTo(-1400);
  stepper.runToPosition();
  delay(5);
  vfd.clear();
  vfd.write("Sample Eight");
  digitalWrite(ROTARYENABLE, LOW);
}
void loop() {
  sCmd.readSerial();
  movingavg();
}

