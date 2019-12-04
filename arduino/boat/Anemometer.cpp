#include <Arduino.h>
#include "Anemometer.h"

float ZERO_WIND_ADJUSTMENT = 0;

Anemometer::Anemometer(int rvPin, int tmpPin)
{
    this->rvPin = rvPin;
    this->tmpPin = tmpPin;
    pinMode(rvPin, INPUT);
    pinMode(tmpPin, INPUT);
}

float Anemometer::getWindspeed()
{
    int TMP_Therm_ADunits = analogRead(tmpPin);
    float RV_Wind_ADunits = analogRead(rvPin);
    float RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125);
    int TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;
    float zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39

    float zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - ZERO_WIND_ADJUSTMENT;
    float WindSpeed_MPH = pow(((RV_Wind_Volts - zeroWind_volts) / .2300), 2.7265);
    return WindSpeed_MPH;
}
