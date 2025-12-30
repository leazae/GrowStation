#include <AM2302-Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define HEATMAT_PIN A0

#define FAN_PIN 2
#define DHT22_PIN 3
#define TERMISTOR_PIN 4

struct sensorsData
{
  float airTemperature;
  float airHumidity;
  float soilTemperature;
};

AM2302::AM2302_Sensor dht22{DHT22_PIN}; // DHT22

OneWire onewire(TERMISTOR_PIN);         // DS18B20
DallasTemperature soilSensor(&onewire);

void setup() 
{
  Serial.begin(9600);
  dht22.begin();
  soilSensor.begin();
  // ACTUATORS
  pinMode(FAN_PIN, OUTPUT);
  pinMode(HEATMAT_PIN, OUTPUT);
  // DATA COLLECTION
  pinMode(DHT22_PIN, INPUT);

}

void loop() 
{
  commandHandler();
}

sensorsData readData()
{
  sensorsData data;
  dht22.read();
  data.airTemperature = dht22.get_Temperature();
  data.airHumidity = dht22.get_Humidity();
  soilSensor.requestTemperatures();
  data.soilTemperature = soilSensor.getTempCByIndex(0);
  return data;
}

// FAN CONTROL
void fanOn(){digitalWrite(FAN_PIN, HIGH);}
void fanOff(){digitalWrite(FAN_PIN, LOW);}

// HEATMAT CONTROL
void heatmatOn(){digitalWrite(HEATMAT_PIN, HIGH);}
void heatmatOff(){digitalWrite(HEATMAT_PIN, LOW);}


void commandHandler()
{
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // usuwa białe znaki na początku i końcu

   if (command.equalsIgnoreCase("fan on")) 
    {
      fanOn();
    }
    else if (command.equalsIgnoreCase("fan off")) 
    {
      fanOff();
    }
    else if (command.equalsIgnoreCase("heatmat on")) 
    {
    heatmatOn();
    }
    else if (command.equalsIgnoreCase("heatmat off")) 
    {
    heatmatOff();
    }
    else if (command.equalsIgnoreCase("read soil temperature")) 
    {
      sensorsData d = readData();
      Serial.print("Soil Temperature: ");
      Serial.println(d.soilTemperature);
    }
    else if (command.equalsIgnoreCase("read air temperature")) 
    {
      sensorsData d = readData();
      Serial.print("Air Temperature: ");
      Serial.println(d.airTemperature);
    }
    else if (command.equalsIgnoreCase("read air humidity")) 
    {
      sensorsData d = readData();
      Serial.print("Air Humidity: ");
      Serial.println(d.airHumidity);
    }
    else if (command.equalsIgnoreCase("read all"))
    {
    sensorsData d = readData();
    Serial.print("Air Temperature: ");
    Serial.println(d.airTemperature);
    Serial.print("Air Humidity: ");
    Serial.println(d.airHumidity);
    Serial.print("Soil Temperature: ");
    Serial.println(d.soilTemperature);
    }
    else if (command.equalsIgnoreCase("import read all"))
    {
    sensorsData d = readData();
    Serial.print("{");
    Serial.print("\"airTemperature\":"); Serial.print(d.airTemperature); Serial.print(",");
    Serial.print("\"airHumidity\":"); Serial.print(d.airHumidity); Serial.print(",");
    Serial.print("\"soilTemperature\":"); Serial.print(d.soilTemperature);
    Serial.println("}");
    }
    else 
    {
      Serial.println("Unknown command");
    }
  }
}
