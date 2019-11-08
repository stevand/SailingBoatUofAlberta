# uAlberta Autonomous Sailing Vehicle
This is the github for the ASV team at the University of Alberta. We are developing an autonomous sailboat in order to compete at the [World Robotic Sailing Championship](https://github.com/WRSC).

## Set up
There are a few dependencies for this project, but they are not strictly necessary unless you wish to run the project on your device or you are working on the corresponding component.

1. The easiest way to upload code to the Arduino i with the [Arduino IDE](https://www.arduino.cc/en/Guide/HomePage). The code itself can be edited in whatever environment you prefer, so long as you have the software that comes bundled with the IDE.


## Running
The main point of entry for our program is through `manager.py`, which should be run from inside /pi. The default configuration, which can be changed by editing the `config.json` file, will start up the flask server on localhost:5000 with the helmsman enabled. Check in /pi/server/flask_server.py for detailed information about the available endpoints.

For debugging purposes, changing the `goal` in `config.json` to 'debug' will allow you to import the instances of BoatDriver and Helmsman that were constructed. In a python session, running `from manager import driver, helmsman` will suffice. Changing the `type` under `driver` in the config file to 'test_driver' will allow you to run the program on a machine that is not actually wired up.
