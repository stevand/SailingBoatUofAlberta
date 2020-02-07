from . import Voter
from pi.navutils import smallest_angle_between

class WindVoter(Voter):

    def vote(self, heading):
        # finds the smallest angle between the candidate heading and the true wind direction
        t = self._driver.get_wind_dir_true()
        print("true wind is: ", t)
        smallest_angle = smallest_angle_between(heading, t)

        if smallest_angle < 45:
            return 0
        else:
            return 1