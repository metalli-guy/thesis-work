#include <SerialCommand.h>
#include <MCP23017.h>
#define MCP23017_I2C_ADDRESS 0x20
MCP23017 mcp23017 = MCP23017(MCP23017_I2C_ADDRESS);
SerialCommand sCmd;
const int XTR = 4;
const int WE = 5;
const int MR = 8;
const int M2 = 13;
const int M1 = 12;
const int M0 = 11;
int LEDCONTROL = 3;
int Q = 2;

void setup() {
  pinMode(WE, OUTPUT);
  pinMode(XTR, OUTPUT);
  pinMode(MR, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M0, OUTPUT);
  pinMode(LEDCONTROL, OUTPUT);
  pinMode(Q, INPUT_PULLUP);
  digitalWrite(M2, LOW);
  digitalWrite(M1, LOW);
  digitalWrite(M0, LOW);
  digitalWrite(LEDCONTROL, LOW);
  attachInterrupt(digitalPinToInterrupt(Q), watcher, RISING);

  Serial.begin(9600);
  sCmd.addCommand("P",     countNumber);
  sCmd.addCommand("LATCH", latch);
  sCmd.addCommand("START", writepulse);

  Wire.begin();
  mcp23017.init();
  configurePinsWithPortMode();
  mcp23017.writeRegister(MCP23017Register::GPIO_A, 0x00);
  mcp23017.writeRegister(MCP23017Register::GPIO_B, 0x00);
}
void configurePinsWithPortMode() {
  mcp23017.portMode(MCP23017Port::A, 0b00000000);
  mcp23017.portMode(MCP23017Port::B, 0b00000000);
  Serial.println("Ready");
}

void countNumber() {
  digitalWrite(LEDCONTROL, LOW);
  uint16_t aNumber;
  char *arg;
  Serial.println("enter number");
  arg = sCmd.next();
  if (arg != NULL) {
    aNumber = atoi(arg);    // Converts a char string to an integer
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

void latch() {
  digitalWrite(LEDCONTROL, LOW);
  digitalWrite(MR, LOW);
  delay(10);
  digitalWrite(MR, HIGH);
  Serial.println("reset done");
  digitalWrite(WE, LOW);
  delay(10);
  digitalWrite(WE, HIGH);
  Serial.println("latch done");
}
void writepulse() {
  digitalWrite(LEDCONTROL, LOW);
  digitalWrite(XTR, HIGH);
  delay(10);
  digitalWrite(XTR, LOW);
  digitalWrite(LEDCONTROL, HIGH);
  Serial.println("started counting");
  if (digitalRead(Q) == HIGH) {
    digitalWrite(LEDCONTROL, LOW);
  }
}
void watcher() {
  digitalWrite(LEDCONTROL, LOW);
}

void loop() {
  sCmd.readSerial();     // We don't do much, just process serial commands

}
