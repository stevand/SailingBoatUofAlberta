import threading
from .. import AbstractNavigator
from .voter import WaypointVoter, WindVoter

class PollNavigator(AbstractNavigator):
    def __init__(self, driver, helmsman, interval=500, num_headings=180, **kwargs):
        super().__init__(driver, helmsman, **kwargs)
        # constructs all necessary voters and their weights
        self._voters = []
        # constructs a dictionary that holds approval for each candidate heading
        self.headings = {2*i: 0 for i in range(num_headings)}

    def poll(self):
        """Polls all voters and returns the heading with the highest approval"""
        for candidate_heading in self.headings.keys():
            self.headings[candidate_heading] = sum(voter.vote(candidate_heading) for voter in self._voters)
        

    