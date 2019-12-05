#include <Servo.h>
#include "Anemometer.h"
#include "XSens.h"
#include <Wire.h>

//take care to properly connect components
const int RUDDER_PIN = 3;
const int SAIL_PIN = 4;
const int WIND_DIRECTION_PIN = A0;
//anemometer pins
const int RV_PIN = A1;
const int TMP_PIN = A2;

//Initializing XSens at ADDRESS 0X6B
XSens xsens(0x6b);

Servo rudder;
Servo sail;
Anemometer anemometer(RV_PIN, TMP_PIN);



void setup()
{
	Serial.setTimeout(50);
	Serial.begin(9600);
	while (!Serial)
		;
	Wire.begin();
	//Wake up process
	xsens.begin();
	pinMode(WIND_DIRECTION_PIN, INPUT);
	rudder.attach(RUDDER_PIN);
	sail.attach(SAIL_PIN);
	Serial.println("ready");
}

void loop()
{
  String input = readInput();
	if (input.length() > 0)
    handleInput(input);
  xsens.updateMeasures();
}

//blocking function
String readInput()
{
	return Serial.readStringUntil('\n');
}

//parses int in the range [start, stop)
int parseInt(String str, int start, int stop)
{
	int total = 0;
	for (int i = start; i < stop; i++)
	{
		total *= 10;
		total += str.charAt(i) - '0'; //converts ascii digit to int
	}
	return total;
}

void setRudder(int angle)
{
	Serial.println(angle);
	rudder.write(angle);
}

void setSail(int angle)
{
	int adjusted = map(angle, 0, 90, 26, 83); //angles adjusted for our particular winch
	Serial.println(angle);
	sail.write(adjusted);
}

void sendPosition()
{
	Serial.print(0.0);
	Serial.print(',');
	Serial.println(0.0);
}

void sendWindspeed()
{
	Serial.println(anemometer.getWindspeed());
}

void sendWindDirection()
{
	//input comes in [0, 706], mapping it to [0, 360]
	int direction = map(analogRead(WIND_DIRECTION_PIN), 0, 706, 0, 360);
	Serial.println(direction);
}

void sendYaw()
{
	
	Serial.println(xsens.get_yaw());
}

/*
first char determines the type of request

rxxx: set rudder angle to xxx degrees
sxxx: set sail angle to xxx degrees
p: return position
w: return windspeed
d: return wind direction
y: return yaw (heading)
*/
void handleInput(String input)
{
	int angle;
	switch (input.charAt(0))
	{
	case 'p':
		sendPosition();
		break;
	case 'w':
		sendWindspeed();
		break;
	case 'd':
		sendWindDirection();
		break;
	case 'r':
		angle = parseInt(input, 1, input.length());
		setRudder(angle);
		break;
	case 's':
		angle = parseInt(input, 1, input.length());
		setSail(angle);
		break;
	case 'y':
		sendYaw();
		break;
	default:
		Serial.print("Invalid Command");
	}
}
