#ifndef XSENS_SENSOR_H
#define XSENS_SENSOR_H

#include "XBus.h"

class XSens{
	public:
		XSens(uint8_t address = 0x6b) : address(address), xbus(address), wokeUp(false){}
		
		void begin();
		void updateMeasures();
		
		float get_yaw(){return xbus.yaw;}
    float get_roll(){return xbus.roll;}
    float get_pitch(){return xbus.pitch;}
		
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
