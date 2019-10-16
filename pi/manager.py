from importlib import import_module
import json
from control.helmsman import Helmsman

with open('config.json') as config_file:
    config = json.loads(
        ''.join(config_file.readlines())
    )

BoatDriver = import_module('boat_driver.'+config['driver']['type']).BoatDriver
print(config['driver']['kwargs'])
driver = BoatDriver(**config['driver']['kwargs'])
helmsman = Helmsman(driver, **config['helmsman']['kwargs'])
