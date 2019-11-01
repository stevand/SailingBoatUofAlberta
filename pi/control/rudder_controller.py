from simple_pid import PID
from time import sleep
import threading

def start_controller(driver, get_desired_heading, is_enabled, interval=0.1, p=0.05, i=0.01, d=0):
    """Starts a PID in a seperate thread that attempts to always reach a desired heading"""
    pid = PID(p, i, d, sample_time=interval, output_limits=(-45, 45))
    control_thread = threading.Thread(target=rudder_controller, daemon=True, args=(driver, pid, interval, get_desired_heading))
    control_thread.start()

# TODO ensure the boat never tries to reach the desired_heading by passing through the no-go zone
# Note that we only read the desired heading, and the interval is small, so for our purposes this is threadsafe
def rudder_controller(driver, pid, interval, get_desired_heading, is_enabled):
    while True:
        if pid.setpoint != get_desired_heading():
            pid.setpoint = get_desired_heading()

        if is_enabled():
            output = pid(driver.get_heading())
            driver.set_rudder(output)
        sleep(interval)