#ifndef XSENS_SENSOR_H
#define XSENS_SENSOR_H

#include "bus/XBus.h"

class XSens{
	public:
		XSens(uint8_t address = 0x1d) : address(address), xbus(address), wokeUp(false){}
		
		void begin();
		void updateMeasures();
		
		float getHeadingYaw(){return xbus.headingYaw;}
		
		float* getQuat(){return xbus.quat;}
		float* getAccel(){return xbus.accel;}
		float* getMag(){return xbus.mag;}
		float* getRot(){return xbus.rot;}
		
	private:
		uint8_t address;
		
		bool wokeUp;
		XBus xbus;
};

#endif