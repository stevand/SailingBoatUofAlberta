import socketio
from typing import List

sio = socketio.Client()
subscribers = []


def begin(url='http://localhost:5001'):
    """This will connect to the socket at the given url"""
    sio.connect(url, namespaces=['/boat'])

def close():
    """Disconnect the socket"""
    sio.disconnect()

def subscribe(callback, depends_on: List[str] = []):
    """
    Adds a callback with optional dependencies to the list of subscribers.
    The callback should be a function that takes a client_data dict as a parameter.
    It will be called whenever client data is recieved that contains relevant information (always by default).

    depends_on is sequence of keywords that must be in the client_data in order for the callback to work.
    The callback is only run if client_data[depends_on[0]][depends_on[1]]... is present.

    This is what a client_data dict looks like:
    {
        driver: {
            rudder: [-45, 45],
            sail: [0, 90],
        },
        helmsman: {
            rudder_controller_enabled: bool,
            sail_controller_enabled: bool,
            desired_heading: [0, 359],
        },
        navigator: {
            waypoints: List of waypoints,
            enabled: bool,
        },
    }
    """
    subscribers.append((callback, depends_on))


def send_data(boat_data):
    """Sends out the given dict through sockets"""
    sio.emit('boat_data', boat_data, namespace='/boat')


def should_call(depends_on, client_data):
    """Checks if the nested keys in depends_on are present in client_data"""
    data = client_data
    for dependency in depends_on:
        if depends_on not in client_data:
            return False
        data = data[dependency]
    return True


@sio.event
def connect():
    print('socket connection established')


@sio.event(namespace='/boat')
def client_data(data):
    for callback, depends_on in subscribers:
        if should_call(depends_on, data):
            callback(data)
