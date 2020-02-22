from importlib import import_module
import json
from pi.helmsman import Helmsman, SailController, RudderController
import sim.sim_runner as sim_runner
from pi.server import flask_server
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver
from sim.sim_interface import SimulatorInterface
from sim.simulator import Simulator
from pi.navigator import AbstractNavigator

config = None
# Singletons should be accessed through the corresponding getters
driver = None
helmsman = None
sim_interface = None
navigator = None
sail_controller = None

instances = {
}


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


def get_config():
    """
    Returns a dictionary representation of the config file.
    Returns None if no config file has been loaded yet.
    """
    return config


def cached(instance_type: type):
    """
    Returns a decorator that caches singletons in instances[type].
    An exception will be raised if no config has been loaded.
    """
    def decorator(getter):
        def wrapper():
            global config, instances
            if not config:
                raise Exception(
                    'No configuration file loaded. Use the load_config function before using any getters.')

            if instance_type in instances:
                return instances[instance_type]

            instances[instance_type] = getter(config)
            return instances[instance_type]

        return wrapper
    return decorator


def get_driver() -> AbstractBoatDriver:
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
    BoatDriver = import_module(
        'pi.boat_driver.'+driver_config['type']).BoatDriver
    # driver insta
    driver = BoatDriver(**driver_config['kwargs'])
    if driver_config['type'] == 'sim_driver':
        driver.get_frame = get_sim_interface().current_frame
    return driver


@cached(SailController)
def get_sail_controller(config=None) -> SailController:
    """
    Returns the (singleton) SailController instance
    """
    sail_controller_config = config['helmsman']['sail_controller']
    return SailController.create(sail_controller_config)


@cached(SailController)
def get_helmsman(config=None) -> Helmsman:
    """
    Returns the (singleton) Helmsman instance.
    A new instance of the helmsman will be created only if one has not yet been instantiated.
    The driver used by the helmsman will be accessed with get_driver
    """
    helmsman_config = config['helmsman']['kwargs']
    return Helmsman.create(helmsman_config)


@cached(RudderController)
def get_rudder_controller(config=None) -> RudderController:
    """
    Returns the (singleton) RudderController instance.
    The driver used will be accessed with get_driver
    """
    rudder_controller_config = config['helmsman']['rudder_controller']
    return RudderController.create(rudder_controller_config)

def get_server_runnable():
    """
    Returns a method that can be called to start a server instance.
    The driver and helmsman will be accessed with get_driver and get_helmsman.
    """
    global config
    server_config = config['server']
    driver = get_driver()
    helmsman = get_helmsman()
    server = flask_server.create_app(
        driver, helmsman=helmsman, **server_config['kwargs'])

    def run():
        server.run(host=server_config['host'])

    return run


def get_sim_interface(**kwargs) -> SimulatorInterface:
    """
    Returns the (singleton) SimulatorInterface instance.
    """
    global config, sim_interface, simulator

    if sim_interface:
        return sim_interface

    sim_interface, simulator = sim_runner.load_sim(**kwargs)
    return sim_interface


def get_simulator() -> Simulator:
    """
    Returns the (singleton) Simulator instance.
    """
    global config, sim_interface, simulator

    if simulator:
        return simulator

    sim_interface, simulator = sim_runner.load_sim()
    return simulator


def get_navigator() -> AbstractNavigator:
    """
    Returns the (singleton) Navigator instance
    """
    global navigator, config

    if navigator:
        return navigator

    nav_config = config['navigator']
    module = import_module('pi.navigator')
    Navigator = getattr(module, nav_config['type'])

    navigator = Navigator(get_driver(), get_helmsman(), **nav_config['kwargs'])
    return navigator


def close_resources():
    """
    Closes any resources that may have been opened (such as the boat driver).
    Should be called at program end.
    """
    if driver:
        driver.close()
