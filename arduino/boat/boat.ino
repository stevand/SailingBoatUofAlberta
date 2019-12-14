#include <Servo.h>
#include "Anemometer.h"
#include "XSens.h"
#include "commandbuffer.h"
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
//Commands are up to 5 characters long
CommandBuffer commBuff(5);

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
	commBuff.update();
	if (commBuff.commandReady()) {
		handleInput(commBuff.getCommand());
	}
	xsens.updateMeasures();
	anemometer.update();
}

//blocking function
String readInput()
{
	return Serial.readStringUntil('\n');
}

//parses int from position start to the end of the string
int parseInt(char* str, int start)
{
	int total = 0;
	int i = start;
	while(str[i] != '\0')
	{
		total *= 10;
		total += str[i]- '0'; //converts ascii digit to int
		i++;
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

// Stub
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
void handleInput(char* input)
{
	int angle;
	switch (input[0])
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
		angle = parseInt(input, 1);
		setRudder(angle);
		break;
	case 's':
		angle = parseInt(input, 1);
		setSail(angle);
		break;
	case 'y':
		sendYaw();
		break;
	default:
		Serial.println("ERR");
	}
}
