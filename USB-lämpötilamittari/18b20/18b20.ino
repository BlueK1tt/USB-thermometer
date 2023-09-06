#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#define ONE_WIRE_BUS 7

  OneWire oneWire(ONE_WIRE_BUS);
  DallasTemperature sensors(&oneWire);

  const int rs = 12, en = 11, d4 = 5,d5 = 4,d6 =3,d7 = 2;
  LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  lcd.begin(16, 2);
  sensors.begin();
  lcd.clear();
  }

void loop() {
  
  lcd.setCursor(2,0);
  sensors.requestTemperatures();
  lcd.print("Temperature:");
  
  lcd.setCursor(5,1);
  int temp = digitalRead(7);
  lcd.print(sensors.getTempCByIndex(0));
  lcd.print("C");
}
