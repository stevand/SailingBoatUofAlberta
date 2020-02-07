import abc

class Voter(abc.ABC):

    def __init__(self, driver, directive):
        self._driver = driver
        self._directive = directive

    @abc.abstractmethod
    def vote(self, heading):
        """Votes on a particular heading, returning an approval value 0 to 1"""
