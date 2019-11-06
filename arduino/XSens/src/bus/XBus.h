#ifndef XBUS_SENSOR_H
#define XBUS_SENSOR_H

#include <Arduino.h>

#define XSENS_CONTROL_PIPE 0x03
#define XSENS_PIPE_STATUS 0x04
#define XSENS_NOTIF_PIPE 0x05
#define XSENS_MEAS_PIPE 0x06

class XBus{
	public:
		XBus(uint8_t address = 0x1d);
		
		enum MesID{WAKEUP = 0x3E, GOTOCONFIG = 0x30, GOTOMEAS = 0x10, RESET = 0x40, 
		REQDID = 0x00, DEVID = 0x01, INITMT = 0x02, INITMTRES = 0x03, REQPRODUCT = 0x1C, 
		PRODUCT = 0x1D, REQFIRM = 0x12, FIRM = 0x13, REQDATALEN = 0x0a, DATALEN = 0x0b, 
		RUNSELFTEST=0x24, SELFTEST = 0x25, ERROR = 0x42, REQGPSSTAT = 0xA6, GPSSTAT = 0xA7,
		REQBAUD = 0x18, FACTORYRESET = 0x0E, SYNCINSET = 0xD6, SYNCOUTSET = 0xD8, REQCONFIg = 0x0C,
		CONFIG = 0x0D, PERIOD = 0x04, OUTSETTING = 0xD2, REQDATA = 0x34, DATA = 0x32, DATA2 = 0x36, RESETORIENTATION = 0xA4, REQUTC = 0x60, UTC = 0x61};
		
		enum DataID{PACKCOUNTER = 0x1020, SAMPTIME = 0x1060, QUAT = 0x2010, ROTMAT = 0x2020, EULERD = 0x2030,
		DV = 0x4010, ACCEL = 0x4020, FACCEL = 0x4030, ACCELHR = 0x4040, ROT = 0x8020, DQ = 0x8030, ROTHR = 0x8040, MAG = 0xC020, STAT = 0xE020};
		
		void parseData(uint8_t* data, uint8_t datalength);
		void read();
		
		float quat[4];
		float accel[3];
		float headingYaw;
		float mag[3];
		float rot[3];
		
		uint8_t* buildMessage(MesID MID, uint8_t* data, uint8_t length);
	private:
		void readPipeStatus();
		void readPipeNotif();
		void readPipeMeas();
		void quatToHeading();
		
		void dataswapendian(uint8_t* data, uint8_t length);
		
		uint8_t data[4];
		uint8_t datanotif[4];
		uint8_t datameas[256];
		
		uint16_t notificationSize;
		uint16_t measurementSize;
		uint8_t address;
};

#endif