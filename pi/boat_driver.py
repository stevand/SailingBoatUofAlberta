import serial

class BoatDriver():
    def __init__(self, port):
        print('opening port', port)
        self._ser = serial.Serial(port, 9600)

    def __del__(self):
        self._ser.close()

    def wind_direction(self):
        resp = self._send('d')
        print(resp)
        return float(resp)

    def heading(self):
        return float(self._send('h'))

    def position(self):
        return tuple(float(coord) for coord in self._send('p').split(','))

    def rudder(self, angle):
        resp = self._send('r' + str(angle))
        print(resp)

    def sail(self, angle):
        resp = self._send('s' + str(angle))
        print(resp)

    def reconnect(self):
        pass

    def  _send(self, cmd):
        self._ser.write(cmd.encode('utf-8'))
        return self._ser.readline().decode('utf-8').strip()

