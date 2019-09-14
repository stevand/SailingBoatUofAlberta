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
	rudder.write(30);
}

void loop()
{
	handleInput(readInput());
}

//blocking function
String readInput(){
	while(!Serial.available())
		;
	return Serial.readString();
}

//parses int in the range [start, stop)
int parseInt(String str, int start, int stop){
	int total = 0;
	for (int i = start; i < stop; i++){
		total *= 10;
		total += str.charAt(i) - '0'; //converts ascii digit to int
	}
	return total;
}

void setRudder(int angle){
	Serial.print("Setting angle of rudder to ");
	Serial.print(angle);
	Serial.print(" degrees.\n");
	rudder.write(angle);
}

void setSail(int angle){
	Serial.print("Setting angle of rudder to ");
	Serial.print(angle);
	Serial.print(" degrees.\n");
	sail.write(angle);
}

/*
first char determines the type of request
requsts must match formats below exactly (leading zeros on numbers if necessary)

rxxx: set rudder angle to xxx degrees
sxxx: set sail angle to xxx degrees
*/
void handleInput(String input){
	switch (input.charAt(0))
	{
	case 'r':
		int angle = parseInt(input, 1, 4); 
		setRudder(angle);
		break;
	case 's':
		angle = parseInt(input, 1, 4);
		setSail(angle);
		break;
	
	default:
		Serial.print("Invalid Command");
	}
}