# uAlberta Autonomous Sailing Vehicle
This is the github for the ASV team at the University of Alberta. We are developing an autonomous sailboat in order to compete at the [World Robotic Sailing Championship](https://github.com/WRSC).

## Set up
There are a few dependencies for this project, but they are not strictly necessary unless you wish to run the project on your device or you are working on the corresponding component.

1. The easiest way to upload code to the Arduino is with the [Arduino IDE](https://www.arduino.cc/en/Guide/HomePage). The code itself can be edited in whatever environment you prefer, so long as you have the software that comes bundled with the IDE.


## Running
The main point of entry for our program is through `manager.py`, which should be run from the project's top level directory. You can run it with the command `python manager.py <path_to_config_file>`. Our configuration files are stored in the configs directory. 

To run the flask server using a test driver, run `python manager.py configs/server_test.json`. To use a driver for the real ASV, open the config file and change the "type" under "driver" from "test_driver" to "boat_driver", or use the config file "configs/server_real.json". A web interface is available with [Remote-Boat](https://github.com/Yash-Bhandari/Remote-Boat). 

## Configs and Routines
Config files are used to specify:
*which routines should be run
*how the service locator should construct instances of the driver, helmsman, simulator and more
*miscellaneous information that can be used by routines

Routines are executed in the order that they are listed. For more information about writing routines, see routines/sample_routine.py.

## Locator
`locator.py` is a service locator that can be used to access instances of the boat driver, helmsman, simulator, simulator interface or server. Some of these (like the boat driver) will be singletons. To use the service locator, `import locator` and then use it's getter methods. If your code is not being run through the manager, make sure to call `locator.load_configs(path_to_config_file)` once.

# Testing
Our automated tests use the built-in unittest module and can be run with the command `python -m unittest discover -s tests`. Our service locator `locator.py` can be used to quickly construct instances needed for testing. Configuration files for testing should be saved in under tests/configs.
