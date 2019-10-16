import serial
from imu.IMU import IMU
from .abstract_boat_driver import AbstractBoatDriver
from time import perf_counter
from threading import Lock

lock = Lock()

class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        self._ser = serial.Serial(kwargs['arduino_port'], 9600, timeout=0.5)
        self._imu = IMU()
        self.set_rudder(0)
        self._rudder = 0
        self.set_sail(0)
        self._sail = 0
        self._lastupdate = perf_counter()-1
        self._status = {}

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
        print("response is ", resp)
        return float(resp)

    def set_rudder(self, angle):
        # maps angle from (-45, 45) to (0, 90)
        resp = self._send('r' + str(int(angle+45)))
        self._rudder = angle
        print('Setting rudder to', resp, 'degrees')
_
    def get_rudder(self):
        return self._rudder

    def set_sail(self, angle):
        resp = self._send('s' + str(int(angle)))
        self._sail = angle
        print('Setting sail to', resp, 'degrees')

    def get_sail(self):
        return self._sail

    def status(self):
        if perf_counter() - self._lastupdate > 1:
            self._status = {
                'wind_dir': self.get_wind_dir(),
                'rel_wind_dir': self.get_rel_wind_dir(),
                'heading': self.get_heading(),
                'position': self.get_position(),
                'sail': self.get_sail(),
                'rudder': self.get_rudder()
            }
            self._lastupdate = perf_counter()

        return self._status

    # sends message to arduino
    def _send(self, cmd):
        with lock:
            self._ser.write((cmd+'\n').encode('utf-8'))
            resp = self._ser.read_until().decode('utf-8').strip()
        return resp
