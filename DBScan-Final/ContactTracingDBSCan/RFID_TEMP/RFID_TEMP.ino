#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
#include <Adafruit_MLX90614.h>
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
 
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  while (!Serial);
  pinMode(13, OUTPUT);

  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);
  };
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
}
void loop() 
{  
  char RxedByte = 0;
  if (Serial.available() > 0){
    RxedByte = Serial.read(); 
    //Serial.print(RxedByte);
    switch(RxedByte)
      {
        case 'A':  
          temp();
          break;
        case 'B': //your code
          rfid();
          break;
      }//end of switch()

  }
  delay(1000);
} 


void rfid()
{
  String content= " ";
  delay(1000);
    // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println(content); 
}
void temp(){
  delay(1000);
   Serial.print(mlx.readObjectTempC()); Serial.println(" C");
}
