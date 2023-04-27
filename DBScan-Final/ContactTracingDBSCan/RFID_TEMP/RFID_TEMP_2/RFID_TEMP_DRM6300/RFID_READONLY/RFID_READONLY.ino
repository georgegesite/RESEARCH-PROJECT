#include <SoftwareSerial.h>
#include <OS_SerialRFID.h>
#define RFID_TX 2
SerialRFID myRFID(RFID_TX);

void setup() 
{
  Serial.begin(9600);
}

void loop()
{
  unsigned long IDnum;
  unsigned long startTime = millis();
  IDnum = myRFID.readIDDec();
  unsigned long endTime = millis();

  if(IDnum != 0)
  {
    Serial.print("ID = ");
    Serial.println(myRFID.readIDString());
    Serial.print("Response time = ");
    Serial.print(endTime - startTime);
    Serial.println(" ms");
  }
  delay(100);
}