#include <Arduino.h>
#include "Anemometer.h"

const float ZERO_WIND_ADJUSTMENT = 0;
// minimum time between measurements (ms)
const int MEASURE_DELAY = 50;
// number of measurements to average
const int NUM_MEASURES = 50;
// Total 2.5 second rolling average

/**
 * Initializes the Anemometer that measures windspeed
 * 
 * @param rvPin the pin connected to the Anemometer's rv pin
 * @param tmpPin the pin connected to the Anemometer's tmp pin
*/
Anemometer::Anemometer(int rvPin, int tmpPin) : rvPin(rvPin), tmpPin(tmpPin)
{
    pinMode(rvPin, INPUT);
    pinMode(tmpPin, INPUT);
    measurements = new float[NUM_MEASURES];
    for (int i = 0; i < NUM_MEASURES; i++)
    {
        measurements[i] = 0;
    }
}

// Updates the rolling average windspeed
void Anemometer::update()
{
    if ((millis() - lastMeasurement) > MEASURE_DELAY)
        {
            total -= measurements[current];
            
            //dampens effect of rapid swings and neutralizes errenous sensor data
            measurements[current] = min(getCurrentWindspeed(), avg + 5);

            //measurements stored in circular array
            //last measurement is removed, new one is added
            total += measurements[current];
            current = (current + 1) % NUM_MEASURES;
            avg = total / NUM_MEASURES;
            lastMeasurement = millis();
        }
}

// Returns the current windspeed, taken from a single measurement
float Anemometer::getCurrentWindspeed()
{
    int TMP_Therm_ADunits = analogRead(tmpPin);
    float RV_Wind_ADunits = analogRead(rvPin);
    float RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125);
    int TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;
    float zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39

    float zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - ZERO_WIND_ADJUSTMENT;
    float WindSpeed_MPH = pow(((RV_Wind_Volts - zeroWind_volts) / .2300), 2.7265);

    //check if NAN
    if (WindSpeed_MPH != WindSpeed_MPH)
        return 0;
    return WindSpeed_MPH;
}

// Returns the rolling average of measurements taken over approximately the last second
float Anemometer::getWindspeed()
{   
    return avg;
}
