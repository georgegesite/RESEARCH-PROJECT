#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup()
{
  Serial.begin(9600);
   if (!mlx.begin()) {  // check if MLX90614 sensor is connected and working
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);  // infinite loop if sensor not connected
  };
}

void loop()
{
  unsigned long startTime = millis();
  float Temp = mlx.readObjectTempC();
  unsigned long endTime = millis();

  if (Temp != 0.0)
  {
    Serial.print("Ambient temperature = ");
    Serial.print(Temp);
    Serial.print(" °C, ");
    Serial.print("Response time = ");
    Serial.print(endTime - startTime);
    Serial.println(" ms");
  }

  delay(1000);
}
