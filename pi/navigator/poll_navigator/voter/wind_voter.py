from . import Voter

class WindVoter(Voter):

    def vote(self, heading):
        # finds the smallest angle between the candidate heading and the true wind direction
        t = self._driver.get_wind_dir_true()
        smallest_angle = min((heading-t)%180, (t-heading)%180)

        if smallest_angle < 45:
            return 0
        else:
            return 1