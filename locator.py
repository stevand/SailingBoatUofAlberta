from importlib import import_module
import json
from pi.control import Helmsman
import sim.sim_runner as sim_runner
from pi.server import flask_server

config = None
# Singletons should be accessed through the corresponding getters
driver = None
helmsman = None
sim_interface = None

def load_config(config_path):
    """
    Loads the config file at the given path. 
    Must be called before singletons can be accessed
    """
    global config
    with open(config_path) as config_file:
        config = json.loads(
            ''.join(config_file.readlines())
        )
    
def get_driver():
    """
    Returns the (singleton) instance of BoatDriver. 
    A new instance of the driver will be created only if one has not yet been instantiated.
    """
    global driver, config

    if not config:
        raise Exception('No configuration file loaded. Use ')
    if driver:
        return driver

    driver_config = config['driver']
    # imports the type of BoatDriver specified in config file
    BoatDriver = import_module('pi.boat_driver.'+driver_config['type']).BoatDriver
    # driver insta
    driver = BoatDriver(**driver_config['kwargs'])
    return driver

def get_helmsman():
    """
    Returns the (singleton) Helsman instance.
    A new instance of the helmsman will be created only if one has not yet been instantiated.
    The driver used by the helmsman will be accessed with get_driver
    """
    global config, helmsman
    if helmsman:
        return helmsman

    helmsman_config = config['helmsman']
    driver = get_driver()
    helmsman = Helmsman(driver, **config['helmsman']['kwargs'])
    return helmsman

def get_server_runnable():
    """
    Returns a method that can be called to start a server instance.
    The driver and helmsman will be accessed with get_driver and get_helmsman.
    """
    global config
    server_config = config['server']
    driver = get_driver()
    helmsman = get_helmsman
    server = flask_server.create_app(driver, helmsman=helmsman, **server_config['kwargs'])

    def run():
        server.run(host=server_config['host'])

    return run

def get_sim_interface():
    """
    Returns the (singleton) SimulatorInterface instance.
    """
    global config, sim_interface, simulator
    
    if sim_interface:
        return sim_interface

    sim_interface, simulator = sim_runner.load_sim()
    return sim_interface

def get_simulator():
    """
    Returns the (singleton) Simulator instance.
    """
    global config, sim_interface, simulator
    
    if simulator:
        return simulator

    sim_interface, simulator = sim_runner.load_sim()
    return simulator