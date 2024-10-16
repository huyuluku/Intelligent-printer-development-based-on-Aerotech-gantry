#include <Wire.h>
#include <PID_v1.h>

// System 1
const int pressurePin = A0;
const int valvePin_1 = 9;
const int solenoidPin_1 = 10;
double setpoint_1 = 0, input_1, output_1;
double Kp_1 = 50.0, Ki_1 = 0.5, Kd_1 = 0.5;
PID pid1(&input_1, &output_1, &setpoint_1, Kp_1, Ki_1, Kd_1, DIRECT);

// System 2
const int I2C_ADDRESS = 0x28;
const int valvePin_2 = 5;
const int solenoidPin_2 = 6;
double setpoint_2 = 0, input_2, output_2;
double Kp_2 = 50.0, Ki_2 = 0.5, Kd_2 = 0.5;
PID pid2(&input_2, &output_2, &setpoint_2, Kp_2, Ki_2, Kd_2, DIRECT);

String receivedString = "";
unsigned long lastReadTime = 0;
unsigned long readInterval = 100; // Read every 100 milliseconds

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.setClock(400000); // Set I2C bus speed to 400 kHz
  pinMode(valvePin_1, OUTPUT);
  pinMode(solenoidPin_1, OUTPUT);
  pinMode(valvePin_2, OUTPUT);
  pinMode(solenoidPin_2, OUTPUT);
  pid1.SetMode(AUTOMATIC);
  pid1.SetSampleTime(20);
  pid2.SetMode(AUTOMATIC);
  pid2.SetSampleTime(20);
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastReadTime > readInterval) {
    lastReadTime = currentTime;
    // Read and control System 1
    int sensorValue_1 = analogRead(pressurePin);
    input_1 = sensorValue_1 / 1024.0 * 150.0 - 14.90;
    pid1.Compute();
    int valveOutput_1 = constrain(output_1, 0, 255);
    analogWrite(valvePin_1, valveOutput_1);
    //analogWrite(valvePin_1, map(output_1, 0, 100, 150, 255));
    //Serial.print("System 1 - Setpoint: ");
    //Serial.print(setpoint_1);
    //Serial.print(", Output: ");
    //Serial.println(valveOutput_1);

    // Read and control System 2
    Wire.requestFrom(I2C_ADDRESS, 2);
    if (Wire.available() == 2) {
      byte highByte = Wire.read();
      byte lowByte = Wire.read();
      int16_t combinedValue_2 = (highByte << 8) | lowByte;
      input_2 = (combinedValue_2 / (float)pow(2, 14)) * 150.0 - 15.00;
      pid2.Compute();
      int valveOutput_2 = constrain(output_2, 0, 255);
      analogWrite(valvePin_2, valveOutput_2);
      //analogWrite(valvePin_2, map(output_2, 0, 100, 150, 255));
      //Serial.print("System 2 - Setpoint: ");
      //Serial.print(setpoint_2);
      //Serial.print(", Output: ");
      //Serial.println(valveOutput_2);
    }
  }

  // Read and control System 2
  Wire.requestFrom(I2C_ADDRESS, 2);
  if (Wire.available() == 2) {
    byte highByte = Wire.read();
    byte lowByte = Wire.read();
    int16_t combinedValue_2 = (highByte << 8) | lowByte;
    input_2 = (combinedValue_2 / (float)pow(2, 14)) * 150.0 - 15.00;
    pid2.Compute();
    int valveOutput_2 = constrain(output_2, 0, 255);
    analogWrite(valvePin_2, valveOutput_2);
    //analogWrite(valvePin_2, map(output_2, 0, 100, 150, 255));
    //Serial.print("System 2 - Setpoint: ");
    //Serial.print(setpoint_2);
    //Serial.print(", Output: ");
    //Serial.println(valveOutput_2);
  }

  // Process serial commands
  processSerialCommands();
}

void processSerialCommands() {
  while (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (isdigit(receivedChar) || receivedChar == '-' || receivedChar == ',') {
      receivedString += receivedChar;
    } else if (receivedChar == '\n') {
      int commaIndex = receivedString.indexOf(',');
      int systemNumber = receivedString.substring(0, commaIndex).toInt();
      int commandValue = receivedString.substring(commaIndex + 1).toInt();

      // Determine which system and command
      if (systemNumber == 1) {
        if (commandValue >= 0 && commandValue <= 100) setpoint_1 = commandValue;
        else if (commandValue == -1) digitalWrite(solenoidPin_1, HIGH);
        else if (commandValue == -2) digitalWrite(solenoidPin_1, LOW);
      } else if (systemNumber == 2) {
        if (commandValue >= 0 && commandValue <= 100) setpoint_2 = commandValue;
        else if (commandValue == -1) digitalWrite(solenoidPin_2, HIGH);
        else if (commandValue == -2) digitalWrite(solenoidPin_2, LOW);
      }
      receivedString = ""; // Clear for next command
    }
  }
}
