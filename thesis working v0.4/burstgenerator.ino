#include <SerialCommand.h>
#include <MCP23017.h>
#define MCP23017_I2C_ADDRESS 0x20
MCP23017 mcp23017 = MCP23017(MCP23017_I2C_ADDRESS);
SerialCommand sCmd;
const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 10;
const int M1 = 12;
const int M0 = 11;
const int LP = 3;

void setup() {
  pinMode(WE, OUTPUT);
  pinMode(XTR, OUTPUT);
  pinMode(MR, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M0, OUTPUT);
  pinMode(LP, OUTPUT);
  digitalWrite(M2, HIGH);
  digitalWrite(M1, HIGH);
  digitalWrite(M0, LOW);
  Serial.begin(9600);
  sCmd.addCommand("P",     countNumber);
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
}

void countNumber() {
  uint16_t aNumberrec;
  uint16_t aNumber;
  char *arg;
  Serial.println("enter number");
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
  Serial.println("reset done");
  digitalWrite(WE, LOW);
  delay(100);
  digitalWrite(WE, HIGH);
  Serial.println("latch done");
}
void writepulse() {
  digitalWrite(XTR, HIGH);
  delay(100);
  digitalWrite(XTR, LOW);
  Serial.println("started counting");
}

void loop() {
  sCmd.readSerial();     // We don't do much, just process serial commands

}
