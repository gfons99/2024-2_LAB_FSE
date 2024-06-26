// ****************************************
// profesor/author: Mauricio Matamoros
// student/editor: F.R., G.M.
// date: 2024-04
// description: Controlar la intensidad de una lámpara de AC.
// ****************************************

#include <Wire.h>

// Digital 2 is Pin 2 on UNO
#define ZXPIN 2
// Digital 3 is Pin 3 on UNO
#define TRIAC 3

// Constants
#define I2C_SLAVE_ADDR 0x0A

// Globals
volatile bool flag = false;
int pdelay = 0;
int inc = 1;
float power = 0;
int power_percent = 0;
int cont = 0;

// Prototypes
void zxhandle(void);

void i2c_received_handler(int count);
void i2c_request_handler(int count);

/**
* Setup the Arduino
*/
void setup(void){
  // Setup interrupt pin (input)
  pinMode(ZXPIN, INPUT);
  // Attach interrupt to pin 2 (interrupt 0) for zero-cross detection
  attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
  // Setup output (triac) pin
  pinMode(TRIAC, OUTPUT);
  
  // Configure I2C to run in slave mode with the defined address
  Wire.begin(I2C_SLAVE_ADDR);
  // Configure the handler for received I2C data
  Wire.onReceive(i2c_received_handler);
  // Configure the handler for request of data via I2C
  Wire.onRequest(i2c_request_handler);

  // Setup the serial port to operate at 9600bps
  Serial.begin(9600);
}

/**
* Handles data requests received via the I2C bus
* It will immediately reply with the power stored
*/
void i2c_request_handler(){
  Wire.write((byte*) &power, sizeof(float));
}

/**
* Handles received data via the I2C bus.
* Data is stored in the local variable power.
*/
void i2c_received_handler(int count){
  byte float_num[4]; // Allocate memory for the array
  for (int i = 0; i < 4; i++) {
    float_num[i] = Wire.read(); // Read each byte from the I2C buffer
  }
  // Interpret the array of bytes as a float value
  float receivedFloat = *((float*)float_num);
  // Print the received float value
  // Serial.println(receivedFloat);
  // power = receivedFloat;
  power_percent = (int)receivedFloat;
}

/**
* Handles zero-cross detection interrupt
* attachInterrupt(0, zxhandle, RISING);
*/
void zxhandle(){
  // Serial.println("Cruce uwu");
  digitalWrite(TRIAC, LOW);
  if (power_percent != 0){
    delayMicroseconds((100 - power_percent) * 80);
    digitalWrite(TRIAC, HIGH);
  }
  // f= 60 Hz // T = 0.016 [s] = 16000 [us]
  // En cada cruce por cero:
  // 8000 [us]  -> 100%
  // 80 [us]    -> 1%
}

void loop(){
  Serial.print("Power = ");
  Serial.print(power_percent);
  Serial.println("%");

  Serial.print("T encendido = ");
  Serial.print(power_percent * 80);
  Serial.println(" [us]");
  delay(1000);
}
