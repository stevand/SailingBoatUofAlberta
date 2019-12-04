from boat_driver.abstract_boat_driver import AbstractBoatDriver

class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def close(self):
        pass

    def get_heading(self):
        print('queried for heading:', 0)
        return 30

    def get_position(self):
        print('queried for position:', 0, 0)
        return (0, 0)

    def get_wind_dir(self):
        super().get_wind_dir()
        print('queried for wind_dir:')
        return 130

    def get_wind_speed(self):
        super().get_wind_speed()
        return 2

    def set_rudder(self, angle):
        super().set_rudder(angle)
        print('rudder set to:', angle)

    def get_rudder(self):
        print('queried for rudder:')
        return super().get_rudder()

    def set_sail(self, angle):
        super().set_sail(angle)
        print('sail set to:', angle)
        self._sail = angle

    def get_sail(self):
        print('queried for sail:')
        return super().get_sail()