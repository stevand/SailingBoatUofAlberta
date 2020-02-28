import abc
from threading import Thread
from time import sleep


class IntervalRepeater(abc.ABC):
    """
    Mixin that repeats process at regualar intervals in a seperate thread. Derived classes need only implement the _interval_process method, which will be repeatedly executed whenever the IntervalRepeater is enabled. The IntervalRepeater can be enabled/disabled by changing the enabled property.

    To start the interval repeater after instantiation, call self._start_interval_repeater
    """

    def __init__(self, interval: float = 1, enabled: bool = True, **kwargs):
        """
        Args:
            interval: the time in seconds between consecutive calls to self._interval_process
            enabled: the initial status
        """
        super().__init__(**kwargs)
        self.__enabled = enabled
        self.__interval = interval
        self.__started = False
        pass

    def _start_interval_repeater(self):
        """
        Will start a thread that repeats the _interval_process at regular intervals.
        Only the first call will start a thread.
        """
        if self.__started:
            return
        self.__started = True
        Thread(target=self.__loop, daemon=True).start()

    def __loop(self):
        while True:
            if self.enabled:
                self._interval_process()
            sleep(self.__interval)

    @abc.abstractmethod
    def _interval_process(self):
        """
        The process to be repeated in intervals whenever self.enabled is true
        """
        pass

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, new_val: bool):
        self.__enabled = new_val
