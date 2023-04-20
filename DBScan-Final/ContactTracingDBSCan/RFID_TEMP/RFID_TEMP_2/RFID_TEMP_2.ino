#include <SPI.h>  // include the SPI library
#include <MFRC522.h>  // include the MFRC522 library
 
#define SS_PIN 10  // define the slave select pin for the MFRC522
#define RST_PIN 9  // define the reset pin for the MFRC522
#include <Adafruit_MLX90614.h>  // include the Adafruit_MLX90614 library

// create instances of the MFRC522 and Adafruit_MLX90614 classes
MFRC522 mfrc522(SS_PIN, RST_PIN);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() 
{
  Serial.begin(9600);   // initialize serial communication at 9600 bits per second
  while (!Serial);  // wait for serial port to open
  pinMode(13, OUTPUT);  // set digital pin 13 as output
  pinMode(2, OUTPUT);   // Set pin 2 as output for the buzzer
  pinMode(3, OUTPUT);   // Set pin 3 as output for the red LED
  pinMode(4, OUTPUT);   // Set pin 4 as output for the green LED
  

  if (!mlx.begin()) {  // check if MLX90614 sensor is connected and working
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);  // infinite loop if sensor not connected
  };

  SPI.begin();      // initialize SPI bus
  mfrc522.PCD_Init();   // initialize MFRC522 reader
}

void loop() 
{  
  char RxedByte = 0;  // create a variable to store received character, initialize to 0
  if (Serial.available() > 0){  // check if there is data available on the serial port
    RxedByte = Serial.read();  // read the incoming byte and store it in RxedByte
    switch(RxedByte)  // use switch statement to execute code based on the value of RxedByte
      {
        case 'A':  // if RxedByte is 'A'
          temp();  // call the temp() function
          break;
        case 'B':  // if RxedByte is 'B'
          rfid();  // call the rfid() function
          break;
      }//end of switch()

  }
  delay(1000);  // delay for 1 second before checking for new data on serial port
} 
void rfid()
{
  String content= " ";
  delay(1000);

  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Show UID on serial monitor
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  content.toUpperCase();
  Serial.println(content); 
}
void temp(){
  delay(1000); // Wait for 1 second before proceeding

  float temperature = mlx.readObjectTempC();
  Serial.print(temperature);
  Serial.println(" C");
  
  if (temperature > 37.5) {
    digitalWrite(3, HIGH); // Turn on red LED
    tone(2, 1000, 5000);   // Sound buzzer for 5 seconds
    delay(5000);            // Wait 5 seconds
    digitalWrite(3, LOW);  // Turn off red LED
    noTone(2);             // Stop buzzer sound
  } else {
    digitalWrite(4, HIGH); // Turn on green LED
    delay(5000);            // Wait 5 seconds
    digitalWrite(4, LOW);  // Turn off green LED
  }
}

