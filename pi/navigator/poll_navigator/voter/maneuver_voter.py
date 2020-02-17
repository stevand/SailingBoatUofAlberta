from . import Voter

class ManueverVoter(Voter):
    def __init__(self, driver, get_curr_heading, **kwargs):
        """
        Voter that tries to prevent excessive maneuvering.
        Args:
            get_curr_heading: function that returns the navigator's current heading.
        """
        super().__init__(driver, **kwargs)
        self._get_curr_heading = get_curr_heading

    def vote(self, heading):
        if self._get_curr_heading() == heading:
            return 0.5
        return 0