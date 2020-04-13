import abc


class Simulator(abc.ABC):

    @abc.abstractmethod
    def simulate(self, prev_state, env, control, interval: int):
        """Given the previous state, returns a prediction of what the next state will be after a certain time interval. The previous state will NOT be mutated.

        Arguments:
            prev_state: a named tuple (of tpe specified by the state property) that represents the boat's state at the beginning of the interval
            env: a named tuple (of type specified by the env property) that represents the boat's environment 
            control: a named tuple (of type specified by the control property) that represents how the boat is being controlled
            interval: the time interval in ms

        Returns:
            a new named tuple (of type specified by the state property) containing the next state
        """
        pass

    @property
    @abc.abstractmethod
    def state(self):
        """
        Returns the factory method of the named tuple that represents this Simulator's state input
        """
        pass

    @property
    @abc.abstractmethod
    def control(self):
        """
        Returns the factory method of the named tuple that represents this Simulator's control input
        """
        pass

    @property
    @abc.abstractmethod
    def env(self):
        """
        Returns the factory method of the named tuple that represents this Simulator's environment input
        """
        pass
