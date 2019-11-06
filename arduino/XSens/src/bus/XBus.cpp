#include "XBus.h"
#include <Wire.h>

XBus::XBus(uint8_t address) : address(address){
	for(int i = 0; i < 4; ++i){
		if(i < 3){
			accel[i] =0;
			rot[i] =0;
			mag[i] =0;
		}
		quat[i] = 0;
	}
}

void XBus::dataswapendian(uint8_t* data, uint8_t length){
	uint8_t cpy[length];
	memcpy(cpy,data,length);
	for(int i = 0; i < length/4; i++){
		for(int j = 0; j < 4; j++){
			data[j+i*4] = cpy[3-j+i*4];
		}
	}
}

void XBus::parseData(uint8_t* data, uint8_t datalength){
	if(datalength < 2)
	return;
	
	uint8_t actualMID = data[0];
	if(actualMID == 0x10 || actualMID == 0x20 || actualMID == 0x40 || actualMID == 0x80 || actualMID == 0xC0 || actualMID == 0xE0){
		uint8_t length = data[2];
		switch(((uint16_t)data[1] |((uint16_t)data[0]<<8)) & (uint16_t)0xFFF0){
		case (uint16_t)DataID::QUAT:
			dataswapendian(data+3, sizeof(float)*4);
			memcpy(quat, data+3, sizeof(float)*4);
			break;
		case (uint16_t)DataID::ACCEL:
			dataswapendian(data+3, 3*sizeof(float));
			memcpy(accel, data+3, sizeof(float)*3);
			break;
		case (uint16_t)DataID::MAG:
			dataswapendian(data+3, 3*sizeof(float));
			memcpy(mag, data+3, sizeof(float)*3);
			break;
		case (uint16_t)DataID::ROT:
			dataswapendian(data+3, 3*sizeof(float));
			memcpy(rot, data+3, sizeof(float)*3);
			break;
		}
		parseData(data+3+length, datalength - length - 3);
	}else{
		uint8_t length = data[1];
		if(actualMID == (uint8_t)MesID::DATA || actualMID == (uint8_t)MesID::DATA2)
		parseData(data+2, length);
	}
}

void XBus::readPipeStatus(){
	Wire.beginTransmission(address);
	Wire.write(XSENS_PIPE_STATUS);
	Wire.endTransmission();
	

	Wire.requestFrom(address,(uint8_t)4);
	if(Wire.available()>0) {
		for(int i = 0; i < 4; i++){
			data[i] = Wire.read();
		}
	}
	notificationSize = (uint16_t)data[0] | ((uint16_t)data[1]<<8);
	measurementSize = (uint16_t)data[2] | ((uint16_t)data[3]<<8);
}
void XBus::readPipeNotif(){
	Wire.beginTransmission(address);
	Wire.write(XSENS_NOTIF_PIPE);
	Wire.endTransmission();
	

	Wire.requestFrom(address,notificationSize);
	if(Wire.available()>0) {
		for(int i = 0; i < notificationSize; ++i){
			datanotif[i] = Wire.read();
		}
	}
}
void XBus::readPipeMeas(){
	Wire.beginTransmission(address);
	Wire.write(XSENS_MEAS_PIPE);
	Wire.endTransmission();
	
	Wire.requestFrom(address,measurementSize);
	if(Wire.available()>0) {
		for(int i = 0; i < measurementSize; ++i){
			datameas[i] = Wire.read();
		}
	}
}

uint8_t* XBus::buildMessage(MesID MID, uint8_t* data, uint8_t length){
	uint8_t* res = new uint8_t[length+4];
	res[0] = (uint8_t)MID;
	res[1] = length;
	if(length > 0 && data != NULL)
		memcpy(res+2, data, length);
	else
		res[2] = 0;
	uint8_t checksum = 0xFF;
	for(int i = 0; i< length+2; i++)
		checksum -= res[0];
	res[length+3] = checksum;
	
	return res;
}

void XBus::quatToHeading(){
	headingYaw = atan2(2*quat[0]*quat[3]+quat[1]*quat[2], 1-2*(quat[2]*quat[2]+quat[3]*quat[3]));
}

void XBus::read(){
	readPipeStatus();
	readPipeNotif();
	readPipeMeas();
	parseData(datameas, measurementSize);
	quatToHeading();
}