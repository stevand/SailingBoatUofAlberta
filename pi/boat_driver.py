import serial

class BoatDriver:
    def __init__(self, port):
        print('opening port', port)
        self._ser = serial.Serial(port, 9600)

    def __del__(self):
        print('closing port', port)
        self._ser.close()

    def absolute_wind_direction(self):
        return float(self._send('d'))

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

if __name__ == 'main':
    port = 'COM3' #replace with '/dev/ttyUSB0' on linux
    driver = BoatDriver(port)  
