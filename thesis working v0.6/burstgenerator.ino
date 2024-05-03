#include <SerialCommand.h>
#include <MCP23017.h>
#include "si5351.h"
#include "Wire.h"
#define MCP23017_I2C_ADDRESS 0x20
MCP23017 mcp23017 = MCP23017(MCP23017_I2C_ADDRESS);
SerialCommand sCmd;
Si5351 si5351;

const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 10;
const int M1 = 12;
const int M0 = 11;
const int LP = 3;
const int STARTIN = 9;
String inString = "";
String delayString = "";
uint16_t aNumberrec;
uint16_t aNumber;
uint32_t freqprint;

void setup() {
  pinMode(WE, OUTPUT);
  pinMode(XTR, OUTPUT);
  pinMode(MR, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M0, OUTPUT);
  pinMode(LP, OUTPUT);
  pinMode(STARTIN, OUTPUT);
  digitalWrite(M2, HIGH);
  digitalWrite(M1, HIGH);
  digitalWrite(M0, LOW);
  digitalWrite(STARTIN, LOW);
  Serial.begin(9600);
  sCmd.addCommand("P",     countNumber);
  sCmd.addCommand("F",     frequencyCommand);
  sCmd.addCommand("LATCH", latch);
  sCmd.addCommand("START", writepulse);
  sCmd.addCommand("POWERON", ledPoweron);
  sCmd.addCommand("POWEROFF", ledPoweroff);
  Wire.begin();
  mcp23017.init();
  mcp23017.portMode(MCP23017Port::A, 0b00000000);
  mcp23017.portMode(MCP23017Port::B, 0b00000000);
  mcp23017.writeRegister(MCP23017Register::GPIO_A, 0x00);
  mcp23017.writeRegister(MCP23017Register::GPIO_B, 0x00);
  si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_8MA);
}

void countNumber() {

  char *arg;
  ////Serial.println("enter number");
  arg = sCmd.next();
  if (arg != NULL) {
    aNumberrec = atoi(arg);    // Converts a char string to an integer
    aNumber = aNumberrec + 1;
    uint16_t invertA = reverse_bits(aNumber);
    uint8_t bNumber = aNumber >> 8;
    uint8_t invertB = reverse_bits(bNumber);
    uint8_t cNumber = aNumber;
    uint8_t invertC = reverse_bits(cNumber);
    mcp23017.writePort(MCP23017Port::B, invertC);
    mcp23017.writePort(MCP23017Port::A, invertB);
  }
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
void latch() {
  digitalWrite(MR, LOW);
  delay(100);
  digitalWrite(MR, HIGH);
  ////Serial.println("reset done");
  digitalWrite(WE, LOW);
  delay(100);
  digitalWrite(WE, HIGH);
  ////Serial.println("latch done");
}
void writepulse() {
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
}
void loop() {
  sCmd.readSerial();     // We don't do much, just process serial commands

}
void frequencyCommand() {
  uint64_t freqrec;
  char *argu;
  ////Serial.println("We're in frequencyCommand");
  argu = sCmd.next();
  inString += argu;
  if (inString != NULL) {
    freqrec = (inString.toInt());    // Converts a char string to an integer
    ////Serial.println(inString);
    ////Serial.print("First argument was: ");
    ////Serial.println(freqprint);
    freqrec = freqrec * 100;
    si5351.set_freq(freqrec, SI5351_CLK0);
    si5351.update_status();
    inString = "";
    sCmd.readSerial();
  }
}
