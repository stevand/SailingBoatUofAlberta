#include "XSens.h"
#include <Wire.h>

void XSens::begin(){
	Wire.beginTransmission(address);
	Wire.write(XSENS_PIPE_STATUS);
	Wire.endTransmission();
	
	uint8_t data[4];
	Wire.requestFrom(address,(uint8_t)4);
	while(Wire.available()>0) {
		for(int i = 0; i < 3; i++){
			data[i] = Wire.read();
		}
	}
	if(data[0] == 0x3e)
		wokeUp = true;
}

void XSens::updateMeasures(){
	xbus.read();
}
