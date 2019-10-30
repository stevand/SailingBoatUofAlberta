import abc


class Simulator(abc.ABC):

    #reference to factory method of state named tuple
    @property
    @abc.abstractmethod
    def state(self):
        pass

    @abc.abstractmethod
    def simulate(self, prev_state, interval):
        """Given the previous state, returns a prediction of what the next state will be after a certain time interval. The previous state will NOT be mutated.

        Arguments:
            prev_state (state): contains information regarding the boat and its environment
            interval (int): the time interval in ms

        Returns:
            (state): a new named tuple (of type specified by self.state) containing the next state

        """
        pass