#include <Arduino.h>
#include <Anemometer.h>

Anemometer::Anemometer(int rvPin, int tmpPin)
{
    this->rvPin = rvPin;
    this->tmpPin = tmpPin;
}

float Anemometer::getWindspeed()
{
    return 20.0;
}

