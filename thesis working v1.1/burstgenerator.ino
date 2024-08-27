/******************************************************
  License:CC4, 2024, Deniz Boztemur
  File Name: interface.py
  Description: Python Code for the August 2024 Thesis of Deniz Boztemur.
  Revision History: v1.1
******************************************************/
//libraries used
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

//rotary stage stepper pins
const int ROTARYENABLE = 40;
int dirPin = 49;
int pulPin = 48;
long initial_homing = -1;
int interruptPin = 52;
AccelStepper stepper(AccelStepper::DRIVER, pulPin, dirPin);

//linear stage stepper pins
const int LINEARENABLE = 41;
int LdirPin = 42;
int LpulPin = 43;
int interruptPin2 = 53;
AccelStepper Lstepper(AccelStepper::DRIVER, LpulPin, LdirPin);

//vfd screen pins
//vfd RS pin to digital pin 12
//vfd Enable pin to digital pin 11
//vfd D4 pin to digital pin 5
//vfd D5 pin to digital pin 4
//vfd D6 pin to digital pin 3
//vfd D7 pin to digital pin 2
//vfd R/W pin to ground
const int rs = 50, en = 51, d4 = 47, d5 = 46, d6 = 45, d7 = 44;
LiquidCrystal vfd(rs, en, d4, d5, d6, d7);

//burst generator PCB pins, all connected via hardware
const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 10;
const int M1 = 12;
const int M0 = 11;

//blue and infrared power pins
const int blLP = 15;
const int irLP = 14;

//PMT enable pin
const int pmtena = 22;

//acquisition signal pin
const int STARTIN = 9;

//PMT high voltage readout pin
const int pmtv = A0;


//create empty string for Si5351
String inString = "";

//create empty string for acquisition
String controlString = "";

//number of pulses
uint16_t aNumberrec;

//pulse number to be written in 74F525
uint16_t aNumber;

//dwell time frequency for Si5351
uint32_t freqmult;

uint16_t invertA;
uint8_t bNumber;
uint8_t invertB;
uint8_t cNumber;
uint8_t invertC;

//moving average number of points
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

  //set stage sensor pins and PMT HV pin as input
  pinMode(interruptPin, INPUT);
  pinMode(interruptPin2, INPUT);
  pinMode(pmtv, INPUT);

  //sets 74f525 to mode 6
  digitalWrite(M2, HIGH);
  digitalWrite(M1, HIGH);
  digitalWrite(M0, LOW);
  digitalWrite(STARTIN, LOW);

  //high disables all 3 power switches
  digitalWrite(pmtena, HIGH);
  digitalWrite(irLP, HIGH);
  digitalWrite(blLP, HIGH);
  Serial.begin(9600);

  //disable stepper motors
  digitalWrite(LINEARENABLE, LOW);
  digitalWrite(ROTARYENABLE, LOW);


  //function calls for serial command
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

  //initialize mcp23017, set all pins as outputs, define both to be used and set 0 on both
  mcp23017.init();
  mcp23017.portMode(MCP23017Port::A, 0b00000000);
  mcp23017.portMode(MCP23017Port::B, 0b00000000);
  mcp23017.writeRegister(MCP23017Register::GPIO_A, 0x00);
  mcp23017.writeRegister(MCP23017Register::GPIO_B, 0x00);

  //start si5351 and set 8mA drive on both channels
  si5351.init(0, 0, 0);
  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_8MA);
  si5351.drive_strength(SI5351_CLK1, SI5351_DRIVE_8MA);
  si5351.drive_strength(SI5351_CLK2, SI5351_DRIVE_8MA);

  //begin vfd and pmt HV movingavg function
  vfd.begin(24, 2);
  pmtbias.begin();

  //set stepper parameters, call both stages to initial position
  stepper.setMaxSpeed(100);
  stepper.setAcceleration(3000);
  Lstepper.setMaxSpeed(1000);
  Lstepper.setAcceleration(20000);
  initialhoming();

  //set AREF to 2.56V
  analogReference(INTERNAL2V56);


  Serial.println("hazırım hacı");
  vfd.clear();
  vfd.write("System Ready");
}

void countNumber() {
  //this function takes a number from the serial port in the form of "P X"
  //this number is split into 2-8 bit numbers, reversed by reverse_bits function
  //then added to each other and written into MCP23017 ports
  char *arg;
  arg = sCmd.next();
  if (arg != NULL) {
    aNumberrec = atoi(arg);
    aNumber = (aNumberrec * 2) + 1;
    if (aNumber == 0) {
      countNumber;
    }
    invertA = reverse_bits(aNumber);
    bNumber = aNumber >> 8;
    invertB = reverse_bits(bNumber);
    cNumber = aNumber;
    invertC = reverse_bits(cNumber);
    mcp23017.writePort(MCP23017Port::B, invertC);
    mcp23017.writePort(MCP23017Port::A, invertB);
  }
  vfd.clear();
  vfd.write("Pulse Count Received");
}
void latch() {
  //this function latches the number of pulses into 74F525
  digitalWrite(MR, LOW);
  delay(100);
  digitalWrite(MR, HIGH);
  delay(100);
  digitalWrite(WE, LOW);
  delay(100);
  digitalWrite(WE, HIGH);
  vfd.clear();
  vfd.write("System Armed");
}
void writepulse() {
  //this is the main functin of the experiment
  //takes two parameters, number of acquisitions and time between acquisitions
  //first parameter is the number of acquisitions, second is the time
  //in the for loop, triggers the counting process of 7F525, then sends the start signal to MCS-32
  //repeats this for the number of acquisitions
  //waits for the delay between acquisitions
  //first two nop's are for stability
  //portg | b0010000 sets XTR high
  //following 8 nops is for the XTR to be settled
  //portg & b11011111 sets XTR low
  //porth | b01000000 sets startin high
  //following nops are a requirement for easymcs to register an external trigger signal
  //porth & b10111111 sets startin low
  //rest of the nops are for stability
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
    delaytime = atoi(arg);
  }
  for (uint64_t i = 0; i <= (passnumber - 1); i++) {
    _NOP();
    _NOP();
    PORTG = PORTG | B00100000;  //this is digitalhigh/
    _NOP(); _NOP();
    _NOP(); _NOP();
    _NOP(); _NOP();
    _NOP(); _NOP();
    PORTG = PORTG & B11011111; //this is digitallow
    PORTH = PORTH | B01000000; //this is digitalhigh
    _NOP();
    _NOP();
    _NOP();
    _NOP();
    PORTH = PORTH & B10111111; //this is digitallow
    _NOP();
    _NOP();
    delay(delaytime);
  }
  controlString = "";
  vfd.clear();
  vfd.write("Experiment Done");
}
byte reverse_bits(byte inverting) {
  //this function reverses the order of bits of an 8-bit number
  byte  rtn = 0;
  for (byte i = 0; i < 8; i++) {
    bitWrite(rtn, 7 - i, bitRead(inverting, i));
  }
  return rtn;
}
void movingavg() {
  //this function takes a moving average of the specified analogread
  int raw = analogRead(pmtv); // read the photocell
  float biasvoltage = raw * 2.5;
  int avg = pmtbias.reading(biasvoltage);    // calculate the moving average
  vfd.setCursor(20, 2);
  vfd.println(avg);
  delay(10);
}
void initialhoming() {
  //this is the initial homing function
  //where both stages are called to their home position
  //when sensors are not triggered, turns the steppers until they are
  //sets absolute position for both home positions
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
  //when LOW, enables PMT HV
  digitalWrite(pmtena, LOW);
}
void pmtdis() {
  //when HIGH, disables PMT HV
  digitalWrite(pmtena, HIGH);
}
void irledPoweron() {
  //when LOW, enables IR LED power
  digitalWrite(irLP, LOW);
}
void irledPoweroff() {
  //when HIGH, disables IR LED power
  digitalWrite(irLP, HIGH);
}
void blPoweron() {
  //when LOW, enables Blue LED power
  digitalWrite(blLP, LOW);
}
void blPoweroff() {
  //when HIGH, disables Blue LED power
  digitalWrite(blLP, HIGH);
}
void frequencyCommand() {
  //this function sets the main dwell times
  //74f525 count rate is set to 125ns in this function by basefreq
  //led pulse width is set to 250ns using ledfreq
  //daq dwell time is calculated in python, then written here
  //Si5351 expects desired frequency x100 as an input
  //function takes desired frequency from serial port and multiplies
  //then writes into Si5351
  char *argu;
  uint32_t ledfreq = 400000000;
  uint32_t basefreq = 800000000;
  argu = sCmd.next();
  inString += argu;
  if (inString != NULL) {
    freqmult = (inString.toInt());
    freqmult = freqmult * 100;
    inString = "";
    si5351.set_freq(basefreq, SI5351_CLK0);
    si5351.set_freq(ledfreq, SI5351_CLK1);
    si5351.set_freq(freqmult, SI5351_CLK2);
    //si5351.set_clock_invert(SI5351_CLK2, 1);
    si5351.pll_reset(SI5351_PLLA);

    si5351.update_status();
  }
  vfd.clear();
  vfd.write("Dwell Time Received");
}
void lhoming() {
  //function to load tray into the experiment.
  //spins the motor until sensor is triggered
  //also sets an absolute position for the home position
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
  //function to eject tray from the experiment.
  //spins the motor for a fixed number of steps.
  digitalWrite(LINEARENABLE, HIGH);
  vfd.clear();
  vfd.write("Ejecting Tray");
  Lstepper.moveTo(-9500);
  Lstepper.runToPosition();
  Lstepper.run();
  delay(5);
  vfd.clear();
  vfd.write("Tray Ejected");
  digitalWrite(LINEARENABLE, LOW);
}
void homing() {
  //function to home the rotary stage.
  //home = sample1
  //spins the motor until sensor is triggered
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
  //function to first home, then turn the stage to sample position 1
  homing();
  digitalWrite(ROTARYENABLE, HIGH);
  delay(5);
  vfd.clear();
  vfd.write("Sample One");
  digitalWrite(ROTARYENABLE, LOW);
}
void sampletwo() {
  //function to first home, then turn the stage to sample position 2
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
  //function to first home, then turn the stage to sample position 3
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
  //function to first home, then turn the stage to sample position 4
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
  //function to first home, then turn the stage to sample position 5
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
  //function to first home, then turn the stage to sample position 6
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
  //function to first home, then turn the stage to sample position 7
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
  //function to first home, then turn the stage to sample position 8
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
  //infinite loop reads the serial port
  //on initialization, calls the moving average function
  //as soon as another function is called, moving average is stopped
  sCmd.readSerial();
  movingavg();
}

