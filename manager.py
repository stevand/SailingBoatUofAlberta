import sys
from importlib import import_module
import json
from pi.control import Helmsman
import sim.sim_runner as sim_runner
from pi.server import flask_server

with open('configs/config.json') as config_file:
    config = json.loads(
        ''.join(config_file.readlines())
    )

# we import the specified type of BoatDriver
BoatDriver = import_module('pi.boat_driver.'+config['driver']['type']).BoatDriver

driver = BoatDriver(**config['driver']['kwargs'])
helmsman = Helmsman(driver, **config['helmsman']['kwargs'])

# starts up the server
if config['goal']=='run':
    server = flask_server.create_app(driver, helmsman, **config['server']['kwargs'])
    server.run(host=config['server']['host'])

# starts up the simulator
if config['goal'] =='simulate':
    sim_interface, _ = sim_runner.load_sim()
    driver.get_frame = sim_interface.current_frame
    if config['simulation']['run']:
        get_control = sim_runner.make_control_getter(driver)
        if config['simulation']['display']:
            sim_runner.display_run(sim_interface, get_control=get_control)
        else:
            sim_runner.run_sim(sim_interface, get_control=get_control)

