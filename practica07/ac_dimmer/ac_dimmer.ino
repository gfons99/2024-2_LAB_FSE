#include <Wire.h>

// Digital 2 is Pin 2 on UNO
#define ZXPIN 2
// Digital 3 is Pin 3 on UNO
#define TRIAC 3

// Constants
#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13

// Globals
volatile bool flag = false;
int pdelay = 0;
int inc = 1;
float power = 0;

// Prototypes
void turnLampOn(void);
void i2c_received_handler(int count);
void i2c_request_handler(int count);
void zxhandle(void);

/**
* Setup the Arduino
*/
void setup(void){
  // Setup interrupt pin (input)
  pinMode(ZXPIN, INPUT);
  // Attach interrupt to pin 2 (interrupt 0) for zero-cross detection
  attachInterrupt(0, zxhandle, RISING);
  // Setup output (triac) pin
  pinMode(TRIAC, OUTPUT);
  // Blink LED on interrupt
  pinMode(BOARD_LED, OUTPUT);
  
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
  Serial.println(receivedFloat);
  power = receivedFloat;
}

/**
* Handles zero-cross detection interrupt
*/
void zxhandle(){
  flag = true;
  // TRIAC automatically shuts down on zero-cross
  digitalWrite(TRIAC, LOW);
  digitalWrite(BOARD_LED, LOW);

  delayMicroseconds(pdelay);

  if(pdelay > 0) turnLampOn();
}

/**
* Turns the lamp on
*/
void turnLampOn(){
  // Turn sentinel LED on
  digitalWrite(BOARD_LED, HIGH);
  // Send a 10us pulse to the TRIAC
  digitalWrite(TRIAC, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIAC, LOW);
}

void loop(){
  char buffer[20];
  sprintf(buffer, "Power = %.2f\n", power);
  Serial.write(buffer);
  delay(1000);
}
