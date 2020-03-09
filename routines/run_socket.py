import locator
from threading import Thread
from time import sleep
from pi.external_io import socket, driver_subscription


def get_boat_data():
    to_send = {
        'driver': locator.get_driver().status()
    }
    return to_send

def send_data_runnable(sleep_time = 0.1):
    while True:
        socket.send_data(get_boat_data())
        sleep(sleep_time)

def get_config():
    config = locator.get_config()
    if 'socket' in config:
        return config['socket']
    return {}

def exec():
    config = get_config()
    socket.subscribe(*driver_subscription)

    try:
        socket.begin(config['url'])
    except KeyError:
        socket.begin()

    thread = Thread(target = send_data_runnable, daemon=True)
    thread.start()

    blocking = False
    def is_done(): return False
    def cleanup():
        socket.close()

    return blocking, is_done, cleanup
