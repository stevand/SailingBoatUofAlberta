import serial
from imu.IMU import IMU

class BoatDriver():
    def __init__(self, port):
        self._ser = serial.Serial(port, 9600)
        self._imu = IMU()

    def __del__(self):
        self._ser.close()

    def wind_direction(self):
        resp = self._send('d')
        print(resp)
        return float(resp)

    def heading(self):
        return imu.heading()

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
        self._ser.write(cmd.encode('utf-8'))
        return self._ser.readline().decode('utf-8').strip()

