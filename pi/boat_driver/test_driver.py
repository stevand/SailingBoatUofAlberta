from boat_driver.abstract_boat_driver import AbstractBoatDriver

class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        self._rudder = 0
        self._sail = 0

    def close(self):
        pass

    def get_heading(self):
        print('queried for heading:', 0)
        return 0

    def get_position(self):
        print('queried for position:', 0, 0)
        return (0, 0)

    def get_wind_dir(self):
        print('queried for wind_dir:', 0)
        return 0

    def set_rudder(self, angle):
        print('rudder set to:', angle)
        self._rudder = angle

    def get_rudder(self):
        print('queried for rudder:', self._rudder)
        return self._rudder

    def set_sail(self, angle):
        print('sail set to:', angle)
        self._sail = angle

    def get_sail(self):
        print('queried for sai:', self._sail)
        return self._sail