from simple_pid import PID
from time import sleep
import threading


def start(driver, get_desired_heading, is_enabled, interval=2, p=5, i=0.01, d=0):
    """
    Starts a PID in a seperate thread that attempts to always reach a desired heading. The thread will close if the program exits.

    Parameters:
        driver: An instance of an AbstractBoatDriver
        get_desired_heading; A method that returns the desired heading
        interval: The time between pid adjustments in seconds. Default is 0.1 seconds
        p: Proportional coefficeint of PID
        i: Integral coefficient of PID
        d: Differential coefficient of PID
    """
    pid = PID(p, i, d, sample_time=interval, output_limits=(-45, 45))
    pid.setpoint = 0
    # thread is created as a daemon so that it will close if the program exits
    control_thread = threading.Thread(target=rudder_controller, daemon=True, args=(
        driver, pid, interval, get_desired_heading, is_enabled))
    control_thread.start()


# TODO ensure the boat never tries to reach the desired_heading by passing through the no-go zone
# Note that we only read the desired heading, and the interval is small, so for our purposes this is threadsafe


def rudder_controller(driver, pid, interval, get_desired_heading, is_enabled):
    while True:
        if is_enabled():
            try:
                output = pid(shortest_path(get_desired_heading(), driver.get_heading()))
                #print('setting rudder to', output)
                driver.set_rudder(output)
            except Exception:
                print('rudder_controller could not read from driver')
        sleep(interval)


def shortest_path(desired, current):
    """
    Returns the shortest distance to the desired angle from the current angle

    Parameters:
        desired: Angle to reach [0,359]
        current: Current angle [0, 359]

    Returns:
        The shortest distance in degrees between the two angles.
        Negative values imply counter clockwise rotation
    """
    if desired >= current:
        if desired - current <= 180:
            return desired - current
        else:
            return -1 * (current + 360 - desired)
    else:
        if current - desired <= 180:
            return desired - current
        else:
            return desired + 360 - current