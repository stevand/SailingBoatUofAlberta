import serial
from .imu.IMU import IMU
from .abstract_boat_driver import AbstractBoatDriver

class BoatDriver(AbstractBoatDriver):
    def __init__(self, port):
        self._ser = serial.Serial(port, 9600, timeout=0.5)
        self._imu = IMU()

    def __del__(self):
        self._ser.close()
        del self._imu

    def wind_direction(self):
        resp = self._send('d')
        return float(resp)

    def heading(self):
        return self._imu.heading()

    def position(self):
        return tuple(float(coord) for coord in self._send('p').split(','))

    def rudder(self, angle):
        resp = self._send('r' + str(angle))
        print('Setting rudder to', resp, 'degrees')

    def sail(self, angle):
        resp = self._send('s' + str(angle))
        print('Setting sail to', resp, 'degrees')

    #sends message to arduino
    def  _send(self, cmd):
        self._ser.write((cmd+'\n').encode('utf-8'))
        return self._ser.readline().decode('utf-8').strip()

