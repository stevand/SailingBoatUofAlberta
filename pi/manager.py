from importlib import import_module
import json
from control.helmsman import Helmsman
from server import flask_server

with open('config.json') as config_file:
    config = json.loads(
        ''.join(config_file.readlines())
    )

BoatDriver = import_module('boat_driver.'+config['driver']['type']).BoatDriver

driver = BoatDriver(**config['driver']['kwargs'])
helmsman = Helmsman(driver, **config['helmsman']['kwargs'])

if config['goal']=='run':
    server = flask_server.create_app(driver, helmsman, **config['server']['kwargs'])
    server.run(host=config['server']['host'])
