import abc


class Simulator(abc.ABC):
    @abc.abstractmethod
    def next_state(prev_state, interval):
        """Given the previous state, returns a prediction of what the next state will be after a certain time interval. The previous state will NOT be mutated.

        Arguments:
            prev_state (mapping): contains information regarding the boat and its environment
            interval (float): the time interval in seconds

        Returns:
            (mapping): a new mapping containing the next state

        """
        pass
