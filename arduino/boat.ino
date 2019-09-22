#include <Servo.h>;

//take care to properly connect components
const int RUDDER_PIN = 3;
const int SAIL_PIN = 4;

Servo rudder;
Servo sail;

void setup()
{
	Serial.begin(9600);
	while (!Serial)
		;
	pinMode(LED_BUILTIN, OUTPUT);
	digitalWrite(LED_BUILTIN, LOW);
	rudder.attach(RUDDER_PIN);
	sail.attach(SAIL_PIN);
}

void loop()
{
	handleInput(readInput());
}

//blocking function
String readInput()
{
	while (!Serial.available())
		;
	return Serial.readString();
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
	Serial.println(angle);
	sail.write(angle);
}

void sendHeading()
{
	Serial.println(0.0);
}

void sendPosition()
{
	Serial.print(0.0);
	Serial.print(',');
	Serial.println(0.0);
}

void sendWindspeed()
{
	Serial.println(0.0);
}

void sendWindDirection()
{
	Serial.println(0.0);
}

/*
first char determines the type of request

rxxx: set rudder angle to xxx degrees
sxxx: set sail angle to xxx degrees
h: return heading
p: return position
w: return windspeed
d: return wind direction
*/
void handleInput(String input)
{
	int angle;
	switch (input.charAt(0))
	{
	case 'h':
		sendHeading();
		break;
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
	default:
		Serial.print("Invalid Command");
	}
}