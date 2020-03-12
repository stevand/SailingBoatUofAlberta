import socketio
from typing import List

sio = socketio.Client()
subscribers = []


def begin(url='http://localhost:5001'):
    """This will connect to the socket at the given url"""
    print("Attempting to connect to", url)
    sio.connect(url, namespaces=['/boat'])


def close():
    """Disconnect the socket"""
    sio.disconnect()
    print('socket connection closed')


def subscribe(callback, dependency: List[str] = []):
    """
    Adds a callback with optional dependencies to the list of subscribers.
    The callback should be a function that takes a subset of client_data dict as a parameter.
    It will be called whenever client data is recieved that contains relevant information (always by default).

    dependency is sequence of keywords that must be in the client_data in order for the callback to work.
    The callback is only run if client_data[dependency[0]][dependency[1]]... is present.

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
    subscribers.append((callback, dependency))


def send_data(boat_data):
    """Sends out the given dict through sockets"""
    sio.emit('boat_data', boat_data, namespace='/boat')


def get_relevant_data(dependency, client_data):
    """
    Finds the subset of client_data that is relevant given the dependency list.
    Returns None if the sequence of keys in dependency is not present.
    """
    if not client_data:
        return None
    data = client_data
    for dependency in dependency:
        if dependency not in client_data:
            return None
        data = data[dependency]
    return data


@sio.event
def connect():
    print('socket connection established')


@sio.event(namespace='/boat')
def client_data(data):
    for callback, dependency in subscribers:
        relevant_data = get_relevant_data(dependency, data)
        if relevant_data is not None:
            callback(relevant_data)
