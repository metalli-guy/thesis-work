#include <SerialCommand.h>
#include <MCP23017.h>
#include "si5351.h"
#include <Wire.h>
#include <AccelStepper.h>
#include <LiquidCrystal.h>
#define MCP23017_I2C_ADDRESS 0x20
MCP23017 mcp23017 = MCP23017(MCP23017_I2C_ADDRESS);
SerialCommand sCmd;
Si5351 si5351;


int dirPin = 49;
int pulPin = 48;
int interruptPin = 52;
AccelStepper stepper(AccelStepper::DRIVER, pulPin, dirPin);

int LdirPin = 42;
int LpulPin = 43;
int interruptPin2 = 53;
AccelStepper Lstepper(AccelStepper::DRIVER, LpulPin, LdirPin);

const int rs = 50, en = 51, d4 = 47, d5 = 46, d6 = 45, d7 = 44;
LiquidCrystal vfd(rs, en, d4, d5, d6, d7);

const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 10;
const int M1 = 12;
const int M0 = 11;
const int LP = 14;
const int pmtP = 15;
const int STARTIN = 9;
const int ROTARYENABLE = 40;
const int LINEARENABLE = 41;

String inString = "";
String delayString = "";
uint16_t aNumberrec;
uint16_t aNumber;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(interruptPin, INPUT);
  pinMode(interruptPin2, INPUT);

  pinMode(WE, OUTPUT);
  pinMode(XTR, OUTPUT);
  pinMode(MR, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M0, OUTPUT);
  pinMode(LP, OUTPUT);
  pinMode(pmtP, OUTPUT);

  pinMode(LINEARENABLE, OUTPUT);
  pinMode(ROTARYENABLE, OUTPUT);

  pinMode(STARTIN, OUTPUT);

  digitalWrite(M2, HIGH);
  digitalWrite(M1, HIGH);
  digitalWrite(M0, LOW);
  digitalWrite(STARTIN, LOW);
  digitalWrite(LINEARENABLE, LOW);
  digitalWrite(ROTARYENABLE, LOW);


  sCmd.addCommand("P",     countNumber);
  sCmd.addCommand("F",     frequencyCommand);
  sCmd.addCommand("LATCH", latch);
  sCmd.addCommand("START", writepulse);
  sCmd.addCommand("POWERON", ledPoweron);
  sCmd.addCommand("POWEROFF", ledPoweroff);
  sCmd.addCommand("PPOWERON", pmtPoweron);
  sCmd.addCommand("PPOWEROF", pmtPoweroff);
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

  mcp23017.init();
  mcp23017.portMode(MCP23017Port::A, 0b00000000);
  mcp23017.portMode(MCP23017Port::B, 0b00000000);
  mcp23017.writeRegister(MCP23017Register::GPIO_A, 0x00);
  mcp23017.writeRegister(MCP23017Register::GPIO_B, 0x00);

  si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_8MA);

  vfd.begin(24, 2);

  stepper.setMaxSpeed(500);
  stepper.setAcceleration(20000);

  Lstepper.setMaxSpeed(1000);
  Lstepper.setAcceleration(20000);
  
  initialhoming();
  
  Serial.println("Ready");
  vfd.clear();
  vfd.write("System Ready");
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
  }
  vfd.clear();
  vfd.write("Pulse Number Received");
}
byte  reverse_bits(byte inverting) {
  byte  rtn = 0;
  for (byte i = 0; i < 8; i++) {
    bitWrite(rtn, 7 - i, bitRead(inverting, i));
  }
  return rtn;
}
void ledPoweron() {
  digitalWrite(LP, HIGH);
}
void ledPoweroff() {
  digitalWrite(LP, LOW);
}
void pmtPoweron() {
  digitalWrite(pmtP, HIGH);
}
void pmtPoweroff() {
  digitalWrite(pmtP, LOW);
}
void latch() {
  digitalWrite(MR, LOW);
  delay(100);
  digitalWrite(MR, HIGH);
  digitalWrite(WE, LOW);
  delay(100);
  digitalWrite(WE, HIGH);
  vfd.clear();
  vfd.write("System Armed");
}
void writepulse() {
  vfd.clear();
  vfd.write("Experiment Started");
  uint64_t passnumber;
  uint64_t delaytime;
  char *passlength;

  passlength = sCmd.next();
  delayString += passlength;
  if (delayString != NULL) {
    delaytime = delayString.toInt();
    uint32_t delayprint = delaytime;
  }
  passlength = sCmd.next();
  if (passlength != NULL) {
    passnumber = delayString.toInt();
    for (int i = 0; i <= (passnumber - 1); i++) {
      digitalWrite(XTR, HIGH);
      delay(10);
      digitalWrite(XTR, LOW);
      digitalWrite(STARTIN, HIGH);
      delayMicroseconds(1);
      digitalWrite(STARTIN, LOW);
      delayMicroseconds(delaytime);
    }
  }
  delayString = "";
  vfd.clear();
  vfd.write("Experiment Finished");
}
void frequencyCommand() {
  uint64_t freqrec;
  char *argu;
  argu = sCmd.next();
  inString += argu;
  if (inString != NULL) {
    freqrec = (inString.toInt());
    freqrec = freqrec * 100;
    si5351.set_freq(freqrec, SI5351_CLK0);
    si5351.update_status();
    inString = "";
    sCmd.readSerial();
  }
  vfd.clear();
  vfd.write("Frequency Received");
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
  stepper.moveTo(-400);
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
  stepper.moveTo(-800);
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
  stepper.moveTo(-1200);
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
}

