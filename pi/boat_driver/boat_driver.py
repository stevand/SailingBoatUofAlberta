import serial
from .abstract_boat_driver import AbstractBoatDriver
from time import perf_counter
from threading import Lock

lock = Lock()


class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        self._ser = serial.Serial(kwargs['arduino_port'], 9600, timeout=15)  # initial timeout set to 15 seconds

        # wait for Arduino to initialize
        print('Connecting to Arduino')
        msg = self._ser.read_until().decode('utf-8').strip()
        if msg != 'ready':
            print('msg:', msg)
            raise Exception('Could not connect to Arduino')
        print('Succesfully connected to Arduino')
        
        self._ser.timeout = 0.5  # set timeout to .5 seconds once initialization is over

        super().__init__(**kwargs)

        self._lastupdate = perf_counter()-1
        self._status = {}

    def close(self):
        self._ser.close()
        print('closed serial port')
        print('closed imu')

    def get_heading(self):
        resp = self._send('y')
        return float(resp)

    def get_position(self):
        return tuple(float(coord) for coord in self._send('p').split(','))

    def get_wind_dir(self):
        resp = self._send('d')
        return float(resp)

    def get_wind_speed(self):
        resp = self._send('w')
        return resp

    def set_rudder(self, angle):
        # maps angle from (-45, 45) to (0, 90)
        super().set_rudder(angle)
        resp = self._send('r' + str(int(angle+45)))
        self._rudder = angle
        print('Setting rudder to', int(resp)-45, 'degrees')

    def set_sail(self, angle):
        super().set_sail(angle)
        resp = self._send('s' + str(int(angle)))
        print('Setting sail to', resp, 'degrees')

    def status(self):
        if perf_counter() - self._lastupdate > 1:
            self._status = {
                'wind_dir': self.get_wind_dir(),
                'rel_wind_dir': self.get_wind_dir_rel(),
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
