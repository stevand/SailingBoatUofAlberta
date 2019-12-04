from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver

class BoatDriver(AbstractBoatDriver):
    def __init__(self, **kwargs):
        self.verbose = kwargs['verbose']
        super().__init__(**kwargs)
        self.heading = 0
        self.position = (0, 0)
        self.wind_dir = 130
        self.wind_speed = 5


    def close(self):
        pass

    def get_heading(self):
        if self.verbose:
            print('queried for heading:', 0)
        return self.heading

    def get_position(self):
        if self.verbose:
            print('queried for position:', 0, 0)
        return self.position

    def get_wind_dir(self):
        super().get_wind_dir()
        if self.verbose:
            print('queried for wind_dir:')
        return self.wind_dir

    def get_wind_speed(self):
        super().get_wind_speed()
        return self.wind_speed

    def set_rudder(self, angle):
        super().set_rudder(angle)
        if self.verbose:
            print('rudder set to:', angle)

    def get_rudder(self):
        if self.verbose:
            print('queried for rudder:')
        return super().get_rudder()

    def set_sail(self, angle):
        super().set_sail(angle)
        if self.verbose:
            print('sail set to:', angle)

    def get_sail(self):
        if self.verbose:
            print('queried for sail:')
        return super().get_sail()