import abc
from pi.boat_driver import AbstractBoatDriver

class Voter(abc.ABC):

    def __init__(self, driver: AbstractBoatDriver, **kwargs):
        """Initializes the Voter with the given driver"""
        self._driver = driver

    @abc.abstractmethod
    def vote(self, heading):
        """Votes on a particular heading, returning an approval value 0 to 1"""
