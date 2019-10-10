import serial
from imu.IMU import IMU
from .abstract_boat_driver import AbstractBoatDriver


class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        self._ser = serial.Serial(kwargs['arduino_port'], 9600, timeout=0.5)
        self._imu = IMU()
        self.set_rudder(0)
        self._rudder = 0
        self.set_sail(0)
        self._sail = 0

    def close(self):
        self._ser.close()
        print('closed serial port')
        self._imu.close()
        print('closed imu')

    def get_heading(self):
        return self._imu.heading()

    def get_position(self):
        return tuple(float(coord) for coord in self._send('p').split(','))

    def get_wind_dir(self):
        resp = self._send('d')
        return float(resp)

    def set_rudder(self, angle):
        resp = self._send('r' + str(angle+45)) #maps angle from (-45, 45) to (0, 90)
        self._rudder = angle
        print('Setting rudder to', resp, 'degrees')

    def get_rudder(self):
        return self._rudder

    def set_sail(self, angle):
        resp = self._send('s' + str(angle))
        self._sail = angle
        print('Setting sail to', resp, 'degrees')

    def get_sail(self):
        return self._sail

    # sends message to arduino
    def _send(self, cmd):
        self._ser.write((cmd+'\n').encode('utf-8'))
        return self._ser.read_until().decode('utf-8').strip()
