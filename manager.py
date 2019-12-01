import sys
from importlib import import_module
import json
from pi.control import Helmsman
import sim.sim_runner as sim_runner
from pi.server import flask_server
from time import sleep

config_path = sys.argv[1]

with open(config_path) as config_file:
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
    sim_config = config['simulation']
    sim_interface, _ = sim_runner.load_sim()
    driver.get_frame = sim_interface.current_frame

    if sim_config['run']:
        get_control = sim_runner.make_control_getter(driver)
        if sim_config['display']:
            root = sim_runner.display_run(sim_interface, get_control=get_control, verbose=sim_config['verbose'], log_file=sim_config['log_file'])
        else:
            sim_runner.run_sim(sim_interface, get_control=get_control, verbose=sim_config['verbose'], log_file=sim_config['log_file'])

    elif sim_config['display']:
        with open(sim_config['log_file']) as log_file:
            data = ''.join(log_file.readlines())
        sim_interface.import_frames(data)
        sim_runner.display(sim_interface)

    def show_status():
        print(driver.status())
        root.after(1000, show_status)

    if sim_config['display']:
        root.after(1000, show_status)
        root.mainloop()


