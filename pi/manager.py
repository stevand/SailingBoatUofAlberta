from importlib import import_module
import json
from control.helmsman import Helmsman
from server import flask_server

with open('config.json') as config_file:
    config = json.loads(
        ''.join(config_file.readlines())
    )

BoatDriver = import_module('boat_driver.'+config['driver']['type']).BoatDriver
#driver = BoatDriver()
driver = BoatDriver(**config['driver']['kwargs'])
server_params = [driver]
if (config['helmsman']['enabled']):
    helmsman = Helmsman(driver)
    server_params.append(driver)

server = flask_server.create_app(*server_params)
server.run()