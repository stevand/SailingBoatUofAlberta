import threading
from time import sleep


def start(driver, is_enabled=lambda: False, go_fast=lambda: True, interval=0.1):
    """Starts a sail controller on a seperate thread that attempts to maximize or minimize speed. The thread will close if the program exits."""
    control_thread = threading.Thread(target=sail_controller, daemon=True, args=(
        driver, is_enabled, go_fast, interval))
    control_thread.start()


def sail_controller(driver, is_enabled, go_fast, interval):
    while True:
        if is_enabled():
            try:
                if go_fast():
                    maximize_speed(driver)
                else:
                    minimize_speed(driver)
            except Exception:
                print('Disabling sail_controller as it could not read from driver.')
                # break
        sleep(interval)


def maximize_speed(driver):
    #print('Reading wind direction as ', driver.get_wind_dir())
    #print('Relative wind ', driver.get_wind_dir_rel())
    #print('setting sail to ', min(abs(driver.get_wind_dir_rel()), 75))
    driver.set_sail(min(abs(driver.get_wind_dir_rel()), 75))
    # driver.set_sail(90)


def minimize_speed(driver):
    driver.set_sail(0)
